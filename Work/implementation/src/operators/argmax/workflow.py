"""End-to-end Discovery → Verification for argmax margin theorem."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from art_int.enums import IntakeStatus
from operators.argmax.discovery import discover_argmax
from operators.argmax.phase_b import discover_argmax_selection_stability
from system_a.fsm import State
from system_a.gates import GateDecision
from system_a.orchestrator import DiscoveryOrchestrator
from system_b.engines import VerificationEngine
from system_b.intake import VerificationIntake
from system_b.lean.bundle import export_bundle, verification_run_to_dicts, write_bundle

SCOPE = "a" * 64
PRINCIPAL = "b" * 64


@dataclass
class ArgmaxResearchResult:
    session_id: str
    theorem_version_id: str
    sealed_digest: str
    crp_digest: str
    intake_status: str
    audit_verdict: str | None
    limitations: tuple[str, ...]
    obligation_statuses: tuple[str, ...]
    unresolved: tuple[str, ...]
    close_reason: str | None
    lean_bundle_path: str | None = None
    profile: str = "PHASE_A_CHARACTERIZATION"
    chain_segment: str | None = None
    mechanism_local_id: str | None = None


def _finish(
    orch: DiscoveryOrchestrator,
    *,
    th: str,
    snap,
    out,
    run,
    export,
    lean_bundle_path: str | None,
    profile: str,
    chain_segment: str | None,
    mechanism_local_id: str | None,
) -> ArgmaxResearchResult:
    orch.start_submission_batch()
    orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
    if out.status == IntakeStatus.ACCEPTED_DRAFT:
        orch.advance(State.DS12)
        orch.import_feedback(export)
        orch.close_from_batch_outcome()

    unresolved = tuple(r.obligation_digest for r in run.results if r.status.value == "OPEN")
    return ArgmaxResearchResult(
        orch.session.session_id,
        th,
        snap.sealed_digest,
        snap.crp.crp_digest,
        out.status.value,
        run.audit_verdict.value if run.audit_verdict else None,
        tuple(run.limitations),
        tuple(r.status.value for r in run.results),
        unresolved,
        orch.session.close_reason,
        lean_bundle_path,
        profile,
        chain_segment,
        mechanism_local_id,
    )


def _maybe_export_lean(snap, out, run, export) -> str | None:
    if out.status != IntakeStatus.ACCEPTED_DRAFT:
        return None
    bundle = export_bundle(
        crp=snap.crp,
        receipt=out.receipt,
        run_id=run.run_id,
        results=verification_run_to_dicts(run),
        audit_verdict=run.audit_verdict.value if run.audit_verdict else None,
        limitations=list(run.limitations),
        counterexamples=list(run.counterexamples),
        feedback_export_digest=export.export_digest,
    )
    dest = (
        Path(__file__).resolve().parents[3]
        / "artifacts"
        / "lean"
        / "bundles"
        / snap.crp.crp_digest
        / f"{run.run_id}.json"
    )
    write_bundle(bundle, dest)
    return str(dest)


def run_argmax_margin_workflow(*, export_lean_bundle: bool = False) -> ArgmaxResearchResult:
    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = PRINCIPAL
    for s in (State.DS01, State.DS02, State.DS03):
        orch.advance(s)
    tips = discover_argmax(orch.ir)
    th = tips["theorem"]
    orch.advance(State.DS05)
    orch.ir.upsert_branch("argmax", [th])
    orch.ir.add_dep(th, tips["assumptions"], "depends")
    orch.ir.add_dep(th, tips["proof_sketch"], "depends")
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member("argmax", "PHASE_A_CHARACTERIZATION", "argmax-margin")
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    assert snap.sealed_digest == snap.crp.crp_digest

    b = VerificationIntake(SCOPE)
    out = b.submit_sealed(snap)
    eng = VerificationEngine()
    run = eng.run_from_package(crp=snap.crp, receipt=out.receipt, obligations=out.obligations)
    export = eng.export(out.receipt, out.obligations, run)
    lean_bundle_path = _maybe_export_lean(snap, out, run, export) if export_lean_bundle else None
    return _finish(
        orch,
        th=th,
        snap=snap,
        out=out,
        run=run,
        export=export,
        lean_bundle_path=lean_bundle_path,
        profile="PHASE_A_CHARACTERIZATION",
        chain_segment="inference",
        mechanism_local_id=None,
    )


def run_argmax_selection_stability_workflow(*, export_lean_bundle: bool = False) -> ArgmaxResearchResult:
    """Phase B charter hop: Q_ψ ℓ∞ ball + argmax → selection_stability CRP."""
    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = PRINCIPAL
    for s in (State.DS01, State.DS02, State.DS03):
        orch.advance(s)
    tips = discover_argmax_selection_stability(orch.ir)
    th = tips["theorem"]
    mech_id = tips["mechanism"]
    orch.advance(State.DS05)
    orch.ir.upsert_branch("argmax-stability", [th])
    orch.ir.add_dep(th, mech_id, "mechanism_for")
    orch.ir.add_dep(th, tips["assumptions"], "depends")
    orch.ir.add_dep(th, tips["proof_sketch"], "depends")
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member(
        "argmax-stability", "PHASE_B_STABILIZATION", "argmax-selection-stability"
    )
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    assert snap.sealed_digest == snap.crp.crp_digest
    assert snap.crp.payload.mechanism_proposals, "Phase B requires mechanisms"
    assert any(
        m.get("local_id") == tips["mechanism_body"]["local_id"] for m in snap.crp.payload.mechanism_proposals
    )

    b = VerificationIntake(SCOPE)
    out = b.submit_sealed(snap)
    assert out.status == IntakeStatus.ACCEPTED_DRAFT, out.status
    eng = VerificationEngine()
    run = eng.run_from_package(crp=snap.crp, receipt=out.receipt, obligations=out.obligations)
    export = eng.export(out.receipt, out.obligations, run)
    lean_bundle_path = _maybe_export_lean(snap, out, run, export) if export_lean_bundle else None
    return _finish(
        orch,
        th=th,
        snap=snap,
        out=out,
        run=run,
        export=export,
        lean_bundle_path=lean_bundle_path,
        profile="PHASE_B_STABILIZATION",
        chain_segment="selection_stability",
        mechanism_local_id=tips["mechanism_body"]["local_id"],
    )
