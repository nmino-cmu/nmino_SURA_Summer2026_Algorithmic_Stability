"""Milestone 3 — System B intake/feedback adapters."""

from __future__ import annotations

import pytest

from art_int.crp import CandidateResearchPackage, CrpPayload, compute_crp_digest
from art_int.enums import AuditVerdict, AuthorKind, CrpProfile, IntakeStatus
from art_int.envelope import SubmissionEnvelope
from art_int.errors import IdempotencyConflict, ProvenanceError, ValidationError
from art_int.feedback import validate_feedback_for_prior
from art_int.receipt import compute_receipt_digest
from system_b.feedback import build_feedback_export
from system_b.intake import VerificationIntake


SCOPE = "a" * 64
PRINCIPAL = "b" * 64


def make_crp(
    *,
    profile: CrpProfile = CrpProfile.PHASE_A_CHARACTERIZATION,
    claims: list | None = None,
    mechanisms: list | None = None,
    bridges: list | None = None,
    schema_version: str = "ARTCRP.v1",
) -> CandidateResearchPackage:
    payload = CrpPayload(
        claims=claims
        if claims is not None
        else [{"statement": "1+1=2", "chain_segment": "characterization"}],
        mechanism_proposals=list(mechanisms or []),
        bridge_proposals=list(bridges or []),
    )
    crp = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest=PRINCIPAL,
        profile=profile,
        math_scope_pin_digest=SCOPE,
        payload=payload,
        sealed_at="2026-07-25T12:00:00Z",
        schema_version=schema_version,
    )
    crp.crp_digest = compute_crp_digest(crp)
    return crp


def test_accepted_package():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out = b.submit_package(make_crp())
    assert out.status == IntakeStatus.ACCEPTED_DRAFT
    assert out.receipt and out.receipt.receipt_digest
    assert out.obligations
    assert all(o.crp_digest == out.receipt.crp_digest for o in out.obligations)


def test_rejected_unsupported_profile_content():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out = b.submit_package(make_crp(profile=CrpProfile.BRIDGE_ONLY, bridges=[]))
    assert out.status == IntakeStatus.REJECTED
    assert "UNSUPPORTED_CANDIDATE_TYPE" in out.reason_codes


def test_mixed_batch():
    b = VerificationIntake(live_scope_pin=SCOPE)
    ok = make_crp()
    bad = make_crp(profile=CrpProfile.PHASE_B_STABILIZATION, mechanisms=[])
    results = b.submit_batch_packages([ok, bad])
    assert results[0].status == IntakeStatus.ACCEPTED_DRAFT
    assert results[1].status == IntakeStatus.REJECTED


def test_characterization_only_and_theorem():
    b = VerificationIntake(live_scope_pin=SCOPE)
    char = make_crp(claims=[])
    thm = make_crp(claims=[{"statement": "T", "chain_segment": "inference"}])
    assert b.submit_package(char).status == IntakeStatus.ACCEPTED_DRAFT
    assert b.submit_package(thm).status == IntakeStatus.ACCEPTED_DRAFT


def test_mechanism_optional_and_present():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out1 = b.submit_package(make_crp(), perturbation_mechanism_id=None)
    assert out1.status == IntakeStatus.ACCEPTED_DRAFT
    out2 = b.submit_package(
        make_crp(mechanisms=[{"local_id": "m1"}]),
        perturbation_mechanism_id="m1",
    )
    assert out2.status == IntakeStatus.ACCEPTED_DRAFT
    # unresolved alias (not projected by A) rejected without mutating CRP
    out3 = b.submit_package(make_crp(), perturbation_mechanism_id="missing")
    assert out3.status == IntakeStatus.REJECTED


def test_stale_digest_tamper_rejected():
    b = VerificationIntake(live_scope_pin=SCOPE)
    crp = make_crp()
    b.submit_package(crp)
    # tamper payload but keep stale digest + key
    crp.payload.claims[0]["statement"] = "tampered"
    env = SubmissionEnvelope(crp=crp, idempotency_key=crp.crp_digest)
    with pytest.raises(ValidationError):
        b.submit_envelope(env)


def test_phase_b_requires_mechanism():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out = b.submit_package(make_crp(profile=CrpProfile.PHASE_B_STABILIZATION))
    assert out.status == IntakeStatus.REJECTED


def test_phase_b_requires_claim_mechanism_binding():
    b = VerificationIntake(live_scope_pin=SCOPE)
    unbound = make_crp(
        profile=CrpProfile.PHASE_B_STABILIZATION,
        mechanisms=[{"local_id": "m1"}],
    )
    out = b.submit_package(unbound)
    assert out.status == IntakeStatus.REJECTED
    assert "MECHANISM_ALIAS_UNRESOLVED" in out.reason_codes

    mismatched = make_crp(
        profile=CrpProfile.PHASE_B_STABILIZATION,
        claims=[
            {
                "statement": "T",
                "chain_segment": "selection_stability",
                "perturbation_mechanism_id": "other",
            }
        ],
        mechanisms=[{"local_id": "m1"}],
    )
    out2 = b.submit_package(mismatched)
    assert out2.status == IntakeStatus.REJECTED
    assert "MECHANISM_ALIAS_UNRESOLVED" in out2.reason_codes

    ok = make_crp(
        profile=CrpProfile.PHASE_B_STABILIZATION,
        claims=[
            {
                "statement": "T",
                "chain_segment": "selection_stability",
                "perturbation_mechanism_id": "m1",
            }
        ],
        mechanisms=[{"local_id": "m1"}],
    )
    out3 = b.submit_package(ok)
    assert out3.status == IntakeStatus.ACCEPTED_DRAFT


def test_multiple_obligations_per_claim():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out = b.submit_package(
        make_crp(claims=[{"statement": "A", "chain_segment": "characterization"}])
    )
    assert len(out.obligations) >= 2
    assert {o.draft_claim_digest for o in out.obligations}


def test_obligation_provenance():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out = b.submit_package(make_crp())
    for o in out.obligations:
        assert o.crp_digest == out.receipt.crp_digest
        assert o.draft_claim_digest in out.receipt.draft_claim_digests


def test_duplicate_package_replay():
    b = VerificationIntake(live_scope_pin=SCOPE)
    crp = make_crp()
    a = b.submit_package(crp)
    b2 = b.submit_package(crp)
    assert b2.replay is True
    assert b2.receipt.receipt_digest == a.receipt.receipt_digest
    assert len(b.accepted) == 1


def test_envelope_idempotent_and_new_content():
    b = VerificationIntake(live_scope_pin=SCOPE)
    crp = make_crp()
    env = SubmissionEnvelope(crp=crp, idempotency_key=crp.crp_digest)
    assert b.submit_envelope(env).status == IntakeStatus.ACCEPTED_DRAFT
    assert b.submit_envelope(env).replay is True
    other = make_crp(claims=[{"statement": "other", "chain_segment": "characterization"}])
    env2 = SubmissionEnvelope(crp=other, idempotency_key=other.crp_digest)
    out2 = b.submit_envelope(env2)
    assert out2.replay is False
    assert out2.status == IntakeStatus.ACCEPTED_DRAFT
    assert len(b.accepted) == 2
    # same key + different digest is rejected by check_idempotency_replay
    with pytest.raises(IdempotencyConflict):
        from art_int.idempotency import check_idempotency_replay

        check_idempotency_replay(
            idempotency_key=crp.crp_digest,
            incoming_digest=other.crp_digest,
            prior_key=crp.crp_digest,
            prior_digest=crp.crp_digest,
        )


def test_receipt_package_mismatch_feedback():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out = b.submit_package(make_crp())
    ex = build_feedback_export(
        receipt=out.receipt,
        obligations=out.obligations,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION.value,
        audit_verdict=AuditVerdict.PASS,
        verification_run_id="run1",
        discharged=[o.obligation_digest for o in out.obligations],
    )
    validate_feedback_for_prior(ex, expected_crp_digest=out.receipt.crp_digest, receipt=out.receipt)
    # wrong package
    with pytest.raises(ProvenanceError):
        validate_feedback_for_prior(ex, expected_crp_digest="f" * 64, receipt=out.receipt)


def test_forged_receipt_rejected():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out = b.submit_package(make_crp())
    forged = out.receipt
    forged.receipt_digest = "0" * 64
    ex = build_feedback_export(
        receipt=forged,
        obligations=out.obligations,
        profile="PHASE_A_CHARACTERIZATION",
        verification_run_id="r",
    )
    # rebuild receipt digest check via validate with original expected digest but forged receipt object
    good = b.accepted[out.receipt.crp_digest]
    # restore digest mismatch: use export with forged digest field
    from art_int.feedback import VerifierFeedbackExport, finalize_export

    bad = finalize_export(
        VerifierFeedbackExport(
            crp_digest=good.crp_digest,
            sealed_digest=good.crp_digest,
            intake_status=IntakeStatus.ACCEPTED_DRAFT,
            profile="PHASE_A_CHARACTERIZATION",
            receipt_digest="1" * 64,
            draft_claim_digests=list(good.draft_claim_digests),
            obligation_digests=list(good.obligation_digests),
            obligations=[],
        )
    )
    with pytest.raises(ProvenanceError):
        validate_feedback_for_prior(bad, expected_crp_digest=good.crp_digest, receipt=good)


def test_multiple_runs_and_supersession():
    b = VerificationIntake(live_scope_pin=SCOPE)
    out = b.submit_package(make_crp())
    e1 = build_feedback_export(
        receipt=out.receipt,
        obligations=out.obligations,
        profile="PHASE_A_CHARACTERIZATION",
        audit_verdict=AuditVerdict.FAIL,
        verification_run_id="run1",
        failed=[out.obligations[0].obligation_digest],
    )
    e2 = build_feedback_export(
        receipt=out.receipt,
        obligations=out.obligations,
        profile="PHASE_A_CHARACTERIZATION",
        audit_verdict=AuditVerdict.PASS,
        verification_run_id="run2",
        discharged=[o.obligation_digest for o in out.obligations],
        supersedes_run_id="run1",
    )
    assert e1.verification_run_id != e2.verification_run_id
    assert e2.provenance.get("supersedes_run_id") == "run1"


def test_unknown_schema_rejected():
    b = VerificationIntake(live_scope_pin=SCOPE)
    crp = make_crp(schema_version="ARTCRP.v999")
    out = b.submit_package(crp)
    assert out.status == IntakeStatus.REJECTED
    assert any("UNSUPPORTED_SCHEMA" in r or "schema" in r.lower() for r in out.reason_codes)


def test_scope_mismatch_rejected():
    b = VerificationIntake(live_scope_pin=SCOPE)
    crp = make_crp()
    crp.math_scope_pin_digest = "c" * 64
    crp.crp_digest = compute_crp_digest(crp)
    out = b.submit_package(crp)
    assert out.status == IntakeStatus.REJECTED


def test_no_system_a_mutation_surface():
    """B adapters must not import system_a (authority boundary)."""
    import system_b.intake as intake_mod
    import system_b.feedback as fb_mod

    assert "system_a" not in intake_mod.__dict__.get("__name__", "")
    src = open(intake_mod.__file__).read() + open(fb_mod.__file__).read()
    assert "import system_a" not in src
    assert "from system_a" not in src
