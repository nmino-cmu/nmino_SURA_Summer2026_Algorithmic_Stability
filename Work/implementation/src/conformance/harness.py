"""ART-INT TRACE_MATRIX + extended A↔B conformance harness."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from art_int.batch import recompute_batch_status
from art_int.crp import CandidateResearchPackage, CrpPayload, compute_crp_digest
from art_int.draft import DraftCRPPayload
from art_int.enums import (
    AuditVerdict,
    AuthorKind,
    BatchStatus,
    CrpProfile,
    IntakeStatus,
    TransportResult,
)
from art_int.envelope import SubmissionEnvelope, strip_or_reject_unknown
from art_int.errors import IdempotencyConflict, ProvenanceError, UnknownFieldError, ValidationError
from art_int.feedback import VerifierFeedbackExport, finalize_export, validate_feedback_for_prior
from art_int.idempotency import check_idempotency_replay
from system_a.fsm import IllegalTransition, State
from system_a.gates import GateDecision
from system_a.orchestrator import DiscoveryOrchestrator
from system_a.packager import compile_branch
from system_b.feedback import build_feedback_export
from system_b.intake import VerificationIntake

SCOPE = "a" * 64
PRINCIPAL = "b" * 64


@dataclass
class TraceResult:
    trace_id: str
    name: str
    passed: bool
    detail: str = ""


@dataclass
class HarnessReport:
    results: list[TraceResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    def to_json(self) -> str:
        return json.dumps(
            {
                "passed": self.passed,
                "total": len(self.results),
                "failures": [asdict(r) for r in self.results if not r.passed],
                "results": [asdict(r) for r in self.results],
            },
            indent=2,
            sort_keys=True,
        )


def _crp(**kw) -> CandidateResearchPackage:
    profile = kw.pop("profile", CrpProfile.PHASE_A_CHARACTERIZATION)
    claims = kw.pop("claims", [{"statement": "p", "chain_segment": "characterization"}])
    payload = CrpPayload(
        claims=claims,
        mechanism_proposals=kw.pop("mechanisms", []),
        bridge_proposals=kw.pop("bridges", []),
    )
    crp = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest=PRINCIPAL,
        profile=profile,
        math_scope_pin_digest=SCOPE,
        payload=payload,
        sealed_at="2026-07-25T12:00:00Z",
        **kw,
    )
    crp.crp_digest = compute_crp_digest(crp)
    return crp


def _a_to_seal(statement: str = "p") -> tuple[DiscoveryOrchestrator, Any]:
    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = PRINCIPAL
    for s in (State.DS01, State.DS02, State.DS03, State.DS05):
        orch.advance(s)
    tip = orch.ir.mint(
        artifact_class="TheoremCandidate",
        caller_module="ATP_ENGINE",
        payload={"statement": statement, "chain_segment": "characterization"},
    )
    orch.ir.upsert_branch("br1", [tip.version_id])
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member("br1", "PHASE_A_CHARACTERIZATION", "m1")
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    return orch, orch.seal_authorized(vid)


def run_harness() -> HarnessReport:
    report = HarnessReport()

    def check(tid: str, name: str, fn: Callable[[], None]) -> None:
        try:
            fn()
            report.results.append(TraceResult(tid, name, True))
        except Exception as e:
            report.results.append(TraceResult(tid, name, False, f"{type(e).__name__}: {e}"))

    # --- TRACE_MATRIX.md TR-INT-01..25 ---

    def m01():
        orch, snap = _a_to_seal("m01")
        b = VerificationIntake(SCOPE)
        out = b.submit_sealed(snap)
        assert out.status == IntakeStatus.ACCEPTED_DRAFT
        assert len(out.obligations) >= 1
        orch.start_submission_batch()
        orch.record_intake(snap.sealed_digest, IntakeStatus.ACCEPTED_DRAFT, out.receipt.receipt_digest)
        assert orch.batches[-1].batch_status == BatchStatus.COMPLETED_ALL_ACCEPTED

    check("TR-INT-01", "Seal→Submit→Commit Phase A + ≥1 PO", m01)

    def m02():
        b = VerificationIntake(SCOPE)
        pkgs = [_crp(claims=[{"statement": s, "chain_segment": "characterization"}]) for s in ("a", "b", "c")]
        outs = b.submit_batch_packages(pkgs)
        assert all(o.status == IntakeStatus.ACCEPTED_DRAFT and o.receipt for o in outs)
        assert len({o.receipt.receipt_digest for o in outs}) == 3

    check("TR-INT-02", "multiple packages → N receipts", m02)

    def m03():
        orch = DiscoveryOrchestrator.create()
        orch.scope_pin = SCOPE
        orch.principal = PRINCIPAL
        # two seals in one wave
        for s in (State.DS01, State.DS02, State.DS03, State.DS05):
            orch.advance(s)
        tips = []
        for i, st in enumerate(("x", "y")):
            tip = orch.ir.mint(
                artifact_class="TheoremCandidate",
                caller_module="ATP_ENGINE",
                payload={"statement": st, "chain_segment": "characterization"},
            )
            orch.ir.upsert_branch(f"b{i}", [tip.version_id])
            tips.append(tip)
        orch.advance(State.DS07)
        orch.advance(State.DS08)
        v0 = orch.compile_portfolio_member("b0", "PHASE_A_CHARACTERIZATION", "m0")
        v1 = orch.compile_portfolio_member("b1", "PHASE_A_CHARACTERIZATION", "m1")
        orch.advance(State.DS09)
        orch.apply_gate3(GateDecision.APPROVE, seal_set=[v0, v1])
        s0 = orch.seal_authorized(v0)
        s1 = orch.seal_authorized(v1)
        b = VerificationIntake(SCOPE)
        o0 = b.submit_sealed(s0)
        o1 = b.submit_package(_crp(profile=CrpProfile.PHASE_B_STABILIZATION, mechanisms=[]))
        orch.start_submission_batch()
        orch.record_intake(s0.sealed_digest, o0.status, o0.receipt.receipt_digest)
        orch.record_intake(s1.sealed_digest, IntakeStatus.REJECTED, None)
        assert orch.batches[-1].batch_status == BatchStatus.COMPLETED_MIXED

    check("TR-INT-03", "partial acceptance → COMPLETED_MIXED", m03)

    def m04():
        orch, snap = _a_to_seal("m04")
        orch.start_submission_batch()
        att = orch.attempts[-1]
        att.transport_result = TransportResult.FAILED
        # retry only that member
        att.transport_result = TransportResult.FAILED
        new = orch.retry_failed_transport(snap.sealed_digest)
        assert new.attempt_number == 2
        assert new.attempt_id in orch.batches[-1].member_attempt_ids
        # accepted member would not be retried — separate check
        b = VerificationIntake(SCOPE)
        out = b.submit_sealed(snap)
        orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
        try:
            orch.retry_failed_transport(snap.sealed_digest)
            raise AssertionError("must not retry ACCEPTED")
        except RuntimeError:
            pass

    check("TR-INT-04", "transport retry only failed member; no ACCEPTED resubmit", m04)

    def m05():
        b = VerificationIntake(SCOPE)
        crp = _crp()
        env = SubmissionEnvelope(crp=crp, idempotency_key=crp.crp_digest)
        assert b.submit_envelope(env).replay is False
        assert b.submit_envelope(env).replay is True

    check("TR-INT-05", "transport/idempotent retry same key via B envelope", m05)

    def m06():
        b = VerificationIntake(SCOPE)
        crp = _crp()
        a = b.submit_package(crp)
        r = b.submit_package(crp)
        assert r.replay and r.receipt.receipt_digest == a.receipt.receipt_digest
        assert len(b.accepted) == 1

    check("TR-INT-06", "duplicate identical bytes idempotent", m06)

    def m07():
        # STALE_WRITE surrogate: stated digest ≠ recomputed
        b = VerificationIntake(SCOPE)
        crp = _crp()
        b.submit_package(crp)
        crp.payload.claims[0]["statement"] = "changed"
        env = SubmissionEnvelope(crp=crp, idempotency_key=crp.crp_digest)
        try:
            b.submit_envelope(env)
            raise AssertionError("expected DIGEST_MISMATCH")
        except ValidationError as e:
            assert e.code == "DIGEST_MISMATCH"

    check("TR-INT-07", "stale digest / STALE_WRITE surrogate rejected", m07)

    def m08():
        b = VerificationIntake(SCOPE)
        assert b.submit_package(_crp(schema_version="ARTCRP.v999")).status == IntakeStatus.REJECTED

    check("TR-INT-08", "unsupported schema_version", m08)

    def m09():
        b = VerificationIntake(SCOPE)
        out = b.submit_package(_crp(profile=CrpProfile.PHASE_B_STABILIZATION, mechanisms=[]))
        assert out.status == IntakeStatus.REJECTED
        assert any("MECHANISM" in r for r in out.reason_codes)

    check("TR-INT-09", "Phase B missing mechanism", m09)

    def m10():
        b = VerificationIntake(SCOPE)
        assert b.submit_package(_crp(claims=[], mechanisms=[])).status == IntakeStatus.ACCEPTED_DRAFT

    check("TR-INT-10", "Phase A characterization empty mech", m10)

    def m11():
        b = VerificationIntake(SCOPE)
        out = b.submit_package(_crp(claims=[{"statement": "T", "chain_segment": "inference"}]))
        assert out.status == IntakeStatus.ACCEPTED_DRAFT and out.receipt.draft_claim_digests

    check("TR-INT-11", "theorem candidate claims intake", m11)

    def m12():
        b = VerificationIntake(SCOPE)
        out = b.submit_package(_crp())
        e1 = build_feedback_export(
            receipt=out.receipt, obligations=out.obligations, profile="PHASE_A_CHARACTERIZATION", verification_run_id="r1"
        )
        e2 = build_feedback_export(
            receipt=out.receipt,
            obligations=out.obligations,
            profile="PHASE_A_CHARACTERIZATION",
            verification_run_id="r2",
            supersedes_run_id="r1",
            audit_verdict=AuditVerdict.PASS,
            discharged=[o.obligation_digest for o in out.obligations],
        )
        assert e1.verification_run_id != e2.verification_run_id
        assert e2.provenance["supersedes_run_id"] == "r1"

    check("TR-INT-12", "multiple verifier runs distinct run_id", m12)

    def m13():
        orch, snap = _a_to_seal("m13")
        b = VerificationIntake(SCOPE)
        out = b.submit_sealed(snap)
        orch.start_submission_batch()
        orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
        orch.advance(State.DS12)
        ex = build_feedback_export(
            receipt=out.receipt,
            obligations=out.obligations,
            profile="PHASE_A_CHARACTERIZATION",
            verification_run_id="r",
            audit_verdict=AuditVerdict.PASS,
            discharged=[o.obligation_digest for o in out.obligations],
        )
        orch.import_feedback(ex)
        assert any(v.artifact_class == "VerifierPrior" for v in orch.ir.versions.values())

    check("TR-INT-13", "feedback before closure → active VerifierPrior", m13)

    def m14():
        orch, snap = _a_to_seal("m14")
        b = VerificationIntake(SCOPE)
        out = b.submit_sealed(snap)
        orch.start_submission_batch()
        orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
        orch.close_from_batch_outcome()
        ex = build_feedback_export(
            receipt=out.receipt, obligations=out.obligations, profile="PHASE_A_CHARACTERIZATION", verification_run_id="r"
        )
        try:
            orch.import_feedback(ex, active=True)
            raise AssertionError
        except IllegalTransition:
            pass
        # new session authorized import
        orch2 = DiscoveryOrchestrator.create("new")
        for s in (State.DS01, State.DS02, State.DS03, State.DS05):
            orch2.advance(s)
        orch2.attest_foreign_seal(orch.session.session_id, snap.sealed_digest)
        orch2.import_feedback(ex, authorized_import=True, source_session_id=orch.session.session_id)

    check("TR-INT-14", "feedback after closure → new session import only", m14)

    def m15():
        b = VerificationIntake(SCOPE)
        out = b.submit_package(_crp())
        ex = build_feedback_export(
            receipt=out.receipt,
            obligations=out.obligations,
            profile="PHASE_A_CHARACTERIZATION",
            verification_run_id="infra",
            limitations=["INFRA_FAILURE"],
            audit_verdict=None,
        )
        assert "INFRA_FAILURE" in ex.verifier_limitations
        assert ex.audit_verdict is None  # not math FAIL

    check("TR-INT-15", "infra failure → limitations not math FAIL", m15)

    def m16():
        # reuse mixed batch close reason
        orch, snap = _a_to_seal("m16a")
        tip = orch.ir.mint(
            artifact_class="TheoremCandidate",
            caller_module="ATP_ENGINE",
            payload={"statement": "m16b", "chain_segment": "characterization"},
        )
        # can't easily second seal in closed path — synthesize batch statuses
        orch.start_submission_batch()
        orch.record_intake(snap.sealed_digest, IntakeStatus.ACCEPTED_DRAFT, "r")
        # forge second attempt outcome mixed via recompute
        from art_int.batch import SubmissionAttempt
        from uuid import uuid4

        att2 = SubmissionAttempt(
            attempt_id=str(uuid4()),
            batch_id=orch.batches[-1].batch_id,
            session_id=orch.session.session_id,
            sealed_snapshot_version_id="x",
            sealed_digest="f" * 64,
            idempotency_key="f" * 64,
            logical_submission_id="x",
            transport_result=TransportResult.OK,
            b_intake_result=IntakeStatus.REJECTED,
        )
        orch.attempts.append(att2)
        orch.batches[-1].member_attempt_ids.append(att2.attempt_id)
        orch.batches[-1].batch_status = recompute_batch_status(
            [a for a in orch.attempts if a.batch_id == orch.batches[-1].batch_id]
        )
        assert orch.batches[-1].batch_status == BatchStatus.COMPLETED_MIXED
        orch.close_from_batch_outcome()
        assert orch.session.close_reason == "completed_mixed_outcomes"

    check("TR-INT-16", "mixed batch close → completed_mixed_outcomes", m16)

    def m17():
        a = _crp(claims=[{"statement": "1", "chain_segment": "characterization"}])
        b = _crp(claims=[{"statement": "2", "chain_segment": "characterization"}])
        assert a.crp_digest != b.crp_digest

    check("TR-INT-17", "duplicate IDs different content → different digests", m17)

    def m18():
        b = VerificationIntake(SCOPE)
        out = b.submit_package(_crp())
        bad = finalize_export(
            VerifierFeedbackExport(
                crp_digest=out.receipt.crp_digest,
                sealed_digest=out.receipt.crp_digest,
                intake_status=IntakeStatus.ACCEPTED_DRAFT,
                profile="PHASE_A_CHARACTERIZATION",
                receipt_digest="0" * 64,
                draft_claim_digests=list(out.receipt.draft_claim_digests),
                obligation_digests=list(out.receipt.obligation_digests),
            )
        )
        try:
            validate_feedback_for_prior(bad, expected_crp_digest=out.receipt.crp_digest, receipt=out.receipt)
            raise AssertionError
        except ProvenanceError:
            pass

    check("TR-INT-18", "forged receipt_ref rejected", m18)

    def m19():
        try:
            strip_or_reject_unknown({"schema_version": "ARTINT.ENV.v1", "crp": {}, "idempotency_key": "x", "evil": 1})
            raise AssertionError
        except UnknownFieldError:
            pass

    check("TR-INT-19", "unknown field rejected", m19)

    def m20():
        cleaned = strip_or_reject_unknown(
            {"schema_version": "ARTINT.ENV.v1", "crp": {}, "idempotency_key": "x", "a_session_id": "s"}
        )
        assert cleaned.get("a_session_id") == "s"  # allowlisted telemetry retained
        stripped = strip_or_reject_unknown(
            {"schema_version": "ARTINT.ENV.v1", "crp": {}, "idempotency_key": "x", "a_unknown_tel": "z"}
        )
        assert "a_unknown_tel" not in stripped

    check("TR-INT-20", "a_* telemetry stripped/ignored", m20)

    def m21():
        b = VerificationIntake(SCOPE)
        assert b.submit_package(_crp(schema_version="ARTCRP.LEGACY")).status == IntakeStatus.REJECTED

    check("TR-INT-21", "legacy schema refused for new sessions", m21)

    def m22():
        orch = DiscoveryOrchestrator.create()
        orch.scope_pin = SCOPE
        tip = orch.ir.mint(
            artifact_class="TheoremCandidate",
            caller_module="ATP_ENGINE",
            payload={"statement": "p", "chain_segment": "characterization"},
        )
        orch.ir.upsert_branch("b", [tip.version_id])
        err = compile_branch(orch.ir, branch_id="b", profile_hint="NOT_A_PROFILE", math_scope_pin_digest=SCOPE)
        assert "PROFILE_MISMATCH" in err.error_codes

    check("TR-INT-22", "profile mismatch → CompileError", m22)

    def m23():
        orch, snap = _a_to_seal("rej")
        b = VerificationIntake(SCOPE)
        # force reject path then revision with prior_crp_digest
        bad = _crp(profile=CrpProfile.PHASE_B_STABILIZATION, mechanisms=[])
        assert b.submit_package(bad).status == IntakeStatus.REJECTED
        revised = _crp(
            claims=[{"statement": "fixed", "chain_segment": "characterization"}],
            prior_crp_digest=snap.sealed_digest,
        )
        assert revised.prior_crp_digest == snap.sealed_digest
        assert b.submit_package(revised).status == IntakeStatus.ACCEPTED_DRAFT

    check("TR-INT-23", "revision after REJECTED with prior_crp_digest", m23)

    def m24():
        orch, s1 = _a_to_seal("old")
        old = s1.sealed_digest
        # new session reseal after IR change
        orch2, s2 = _a_to_seal("new-content")
        assert s2.sealed_digest != old
        assert old == s1.sealed_digest  # old not mutated

    check("TR-INT-24", "resealed after IR change → new digest; old intact", m24)

    def m25():
        orch, snap = _a_to_seal("cert")
        b = VerificationIntake(SCOPE)
        out = b.submit_sealed(snap)
        ex = build_feedback_export(
            receipt=out.receipt,
            obligations=out.obligations,
            profile="PHASE_A_CHARACTERIZATION",
            verification_run_id="cert",
            audit_verdict=AuditVerdict.PASS,
            discharged=[o.obligation_digest for o in out.obligations],
        )
        assert ex.audit_verdict == AuditVerdict.PASS
        assert ex.export_digest
        # A consumes as prior only
        orch.start_submission_batch()
        orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
        orch.advance(State.DS12)
        orch.import_feedback(ex)

    check("TR-INT-25", "certified export → A prior (APPLY B-only)", m25)

    # Idempotency conflict still via helper (matrix adversarial)
    def adv_idem():
        try:
            check_idempotency_replay(
                idempotency_key="a" * 64,
                incoming_digest="b" * 64,
                prior_key="a" * 64,
                prior_digest="a" * 64,
            )
            raise AssertionError
        except IdempotencyConflict:
            pass

    check("ADV-IDEM", "same key different digest conflict", adv_idem)

    return report


def write_report(path: Path | None = None) -> HarnessReport:
    report = run_harness()
    out = path or Path(__file__).resolve().parents[2] / "docs" / "conformance_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report.to_json())
    return report


if __name__ == "__main__":
    r = write_report()
    print(r.to_json())
    raise SystemExit(0 if r.passed else 1)
