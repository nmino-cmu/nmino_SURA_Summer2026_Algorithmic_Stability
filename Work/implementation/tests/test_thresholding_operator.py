"""Thresholding operator — math, verification, e2e, edge cases."""

from __future__ import annotations

import math

import pytest

from art_int.crp import CandidateResearchPackage, CrpPayload, compute_crp_digest
from art_int.enums import AuditVerdict, AuthorKind, CrpProfile, IntakeStatus, ObligationStatus
from operators.thresholding.math import (
    EVALUATION_METHOD_DET,
    EVALUATION_METHOD_NOISY,
    LEVEL_STATUS,
    SHARPNESS_STATEMENT_DET,
    THEOREM_STATEMENT_DET,
    THEOREM_STATEMENT_NOISY,
    SequentialLevel,
    ThresholdInstance,
    abstaining_threshold,
    above_threshold,
    adversarial_break_fail,
    adversarial_break_pass,
    certified_set,
    fail_preserved,
    first_crossing,
    laplace_pass_probability,
    noisy_both,
    noisy_first_crossing,
    noisy_query_only,
    noisy_threshold_only,
    pass_preserved,
    unstable_region,
)
from operators.thresholding.verify import (
    verify_bounded_noise_threshold,
    verify_threshold_preservation,
)
from operators.thresholding.workflow import (
    run_bounded_noise_threshold_workflow,
    run_threshold_preservation_workflow,
)
from system_b.engines import VerificationEngine
from system_b.intake import VerificationIntake

SCOPE = "a" * 64

FORMAL_DET = {
    "equality_convention": "x >= T passes",
    "perturbation": "|x'-x| <= epsilon",
    "pass_condition": "x >= T + epsilon",
    "fail_condition": "x < T - epsilon",
    "unstable_region": "[T - epsilon, T + epsilon)",
    "signed_margin": "m = x - T",
    "distance": "d = |x - T|",
}

FORMAL_NOISY = {
    "noise_model": "almost_sure_bounded |xi| <= eta",
    "mechanism": "1{x + xi >= T}",
    "pass_condition": "x >= T + eta",
    "fail_condition": "x < T - eta",
    "unstable_region": "[T - eta, T + eta)",
    "not_claimed": "full_sparse_vector_privacy",
}


def _det_claim(**extra):
    c = {
        "statement": THEOREM_STATEMENT_DET,
        "chain_segment": "inference",
        "operator": "thresholding",
        "theorem_id": "threshold-output-preservation",
        "evaluation": EVALUATION_METHOD_DET,
        "sharpness_statement": SHARPNESS_STATEMENT_DET,
        "formal": dict(FORMAL_DET),
    }
    c.update(extra)
    return c


def _noisy_claim(**extra):
    c = {
        "statement": THEOREM_STATEMENT_NOISY,
        "chain_segment": "inference",
        "operator": "thresholding",
        "theorem_id": "bounded-noise-threshold",
        "evaluation": EVALUATION_METHOD_NOISY,
        "formal": dict(FORMAL_NOISY),
    }
    c.update(extra)
    return c


# --- Phase 1 / edge math ---


def test_equality_convention():
    assert above_threshold(1.0, 1.0) == 1
    assert above_threshold(0.999, 1.0) == 0
    assert ThresholdInstance(0.0, 0.0).signed_margin() == 0.0
    assert ThresholdInstance(2.0, 5.0).distance() == 3.0


@pytest.mark.parametrize(
    "x,expect_pass,expect_fail,expect_unstable",
    [
        (2.0, True, False, False),   # 1. x > T+ε
        (1.0, True, False, False),   # 2. x = T+ε
        (0.5, False, False, True),   # 3. x ∈ (T, T+ε)
        (0.0, False, False, True),   # 4. x = T
        (-0.5, False, False, True),  # 5. x ∈ (T-ε, T)
        (-1.0, False, False, True),  # 6. x = T-ε
        (-2.0, False, True, False),  # 7. x < T-ε
    ],
)
def test_regions_T0_eps1(x, expect_pass, expect_fail, expect_unstable):
    T, eps = 0.0, 1.0
    assert pass_preserved(x, T, eps) is expect_pass
    assert fail_preserved(x, T, eps) is expect_fail
    assert unstable_region(x, T, eps) is expect_unstable


def test_eps_zero():
    T = 0.0
    for x in (-1.0, 0.0, 1.0):
        assert not unstable_region(x, T, 0.0)
        if x >= T:
            assert pass_preserved(x, T, 0.0)
        else:
            assert fail_preserved(x, T, 0.0)


def test_negative_threshold_and_large_values():
    assert pass_preserved(10.0, -100.0, 1.0)
    assert fail_preserved(-1e12, 0.0, 10.0)
    assert above_threshold(1e12, 1e12) == 1


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_nonfinite_rejected(bad):
    with pytest.raises(ValueError):
        ThresholdInstance(bad, 0.0)
    with pytest.raises(ValueError):
        ThresholdInstance(0.0, bad)
    with pytest.raises(ValueError):
        pass_preserved(bad, 0.0, 1.0)


def test_malformed_eps_and_threshold():
    with pytest.raises(ValueError):
        pass_preserved(0.0, 0.0, -0.1)
    with pytest.raises(ValueError):
        fail_preserved(0.0, math.nan, 1.0)


def test_sharpness_asymmetry():
    T, eps = 0.0, 1.0
    # passing-side: in [T, T+ε) can flip to 0
    br = adversarial_break_pass(0.5, T, eps)
    assert br is not None and above_threshold(br, T) == 0
    # at T+ε cannot flip
    assert adversarial_break_pass(1.0, T, eps) is None
    # failing-side: in [T-ε, T) can flip to 1
    br2 = adversarial_break_fail(-0.5, T, eps)
    assert br2 is not None and above_threshold(br2, T) == 1
    # at T-ε can flip (equality on pass)
    br3 = adversarial_break_fail(-1.0, T, eps)
    assert br3 is not None and above_threshold(br3, T) == 1


def test_perturbation_invariance_math():
    T, eps, x = 0.0, 1.0, 2.0
    assert pass_preserved(x, T, eps)
    for xp in (x - eps, x, x + eps):
        assert above_threshold(xp, T) == 1


# --- Mechanisms ---


def test_noisy_mechanisms_and_abstention():
    assert noisy_query_only(0.0, 1.0, 1.5) == 1
    assert noisy_threshold_only(0.0, 0.0, 0.5) == 0
    assert noisy_both(1.0, 0.0, 0.2, 0.5) == 1  # 1+0.2-0.5=0.7≥0? wait 0.7>=0 yes
    assert abstaining_threshold(5.0, 0.0, 1.0) == 1
    assert abstaining_threshold(-5.0, 0.0, 1.0) == 0
    assert abstaining_threshold(0.5, 0.0, 1.0) is None
    # fail-side boundary is abstention (strict), not a certified 0
    assert abstaining_threshold(-1.0, 0.0, 1.0) is None
    assert certified_set(5.0, 0.0, 1.0) == frozenset({1})
    assert certified_set(-5.0, 0.0, 1.0) == frozenset({0})
    assert certified_set(0.0, 0.0, 1.0) == frozenset({0, 1})


def test_sequential_crossing():
    assert first_crossing((0.0, 0.5, 2.0), 1.0) == 2  # first crossing
    assert first_crossing((0.0, 0.5), 1.0) is None  # no-crossing
    assert first_crossing((2.0, 3.0), 1.0) == 0  # first query
    assert first_crossing((0.5, 1.0, 1.5), 1.0) == 1  # multiple possible; first wins
    # adaptive order is caller-supplied sequence — order matters
    assert first_crossing((1.5, 0.0), 1.0) == 0
    assert first_crossing((0.0, 1.5), 1.0) == 1
    assert noisy_first_crossing((0.0, 0.5), 1.0, (0.0, 0.6), 0.0) == 1
    with pytest.raises(ValueError):
        noisy_first_crossing((0.0,), 1.0, (0.0, 0.1), 0.0)
    assert LEVEL_STATUS[SequentialLevel.FULL_SPARSE_VECTOR] == "NOT_VERIFIED"


def test_laplace_and_malformed_noise():
    assert abs(laplace_pass_probability(0.0, 0.0, 1.0) - 0.5) < 1e-12
    assert laplace_pass_probability(10.0, 0.0, 1.0) > 0.99
    with pytest.raises(ValueError):
        laplace_pass_probability(0.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        laplace_pass_probability(0.0, 0.0, -1.0)


# --- Verification ---


def test_verify_canonical_det():
    assert verify_threshold_preservation(_det_claim()).ok


def test_verify_rejects_statement_smuggling():
    bad = _det_claim(statement=THEOREM_STATEMENT_DET + " AND false")
    r = verify_threshold_preservation(bad)
    assert r.ok is False and r.detail == "statement_mismatch"


def test_verify_noisy_and_rejects_svt_smuggling():
    assert verify_bounded_noise_threshold(_noisy_claim()).ok
    formal = dict(FORMAL_NOISY)
    formal["not_claimed"] = "nothing"
    r = verify_bounded_noise_threshold(_noisy_claim(formal=formal))
    assert r.ok is False


def test_engine_rejects_crp_receipt_laundering():
    """MAJOR Sol finding: cannot evaluate CRP B under receipt/obligations from CRP A."""
    claim = _det_claim()
    crp_a = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(claims=[claim]),
        sealed_at="t",
    )
    crp_a.crp_digest = compute_crp_digest(crp_a)
    out_a = VerificationIntake(SCOPE).submit_package(crp_a)

    # Same claim content (same claim digests), different CRP digest via extra payload
    crp_b = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(claims=[claim], examples=[{"marker": "B"}]),
        sealed_at="t",
    )
    crp_b.crp_digest = compute_crp_digest(crp_b)
    assert crp_b.crp_digest != out_a.receipt.crp_digest

    run = VerificationEngine().run_from_package(
        crp=crp_b, receipt=out_a.receipt, obligations=out_a.obligations
    )
    assert run.audit_verdict != AuditVerdict.PASS
    assert "PROVENANCE_BINDING_MISMATCH" in run.limitations
    assert all(r.kind.value == "INFRA_FAILURE" for r in run.results)


def test_verify_rejects_malformed_formal():
    bad = _det_claim(formal=[])
    assert verify_threshold_preservation(bad).ok is False
    assert verify_threshold_preservation(bad).detail == "bad_formal_type"
    bad_n = _noisy_claim(formal="nope")
    assert verify_bounded_noise_threshold(bad_n).ok is False
    crp = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(claims=[_det_claim()]),
        sealed_at="t",
    )
    crp.crp_digest = compute_crp_digest(crp)
    out = VerificationIntake(SCOPE).submit_package(crp)
    run = VerificationEngine().run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    assert run.audit_verdict == AuditVerdict.PASS
    assert all(r.status == ObligationStatus.DISCHARGED for r in run.results)
    assert "COMPUTATIONAL_VERIFICATION_NOT_LEAN" in run.limitations
    assert not any(x.startswith("DEMO_") for x in run.limitations)


def test_engine_discharges_noisy():
    crp = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(claims=[_noisy_claim()]),
        sealed_at="t",
    )
    crp.crp_digest = compute_crp_digest(crp)
    out = VerificationIntake(SCOPE).submit_package(crp)
    run = VerificationEngine().run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    assert run.audit_verdict == AuditVerdict.PASS
    assert "BOUNDED_NOISE_NOT_FULL_SVT" in run.limitations


def test_e2e_workflows():
    r1 = run_threshold_preservation_workflow()
    assert r1.audit_verdict == "PASS"
    assert not r1.unresolved
    assert "THRESHOLD_PRESERVATION_COMPUTATIONAL_V1" in r1.limitations

    r2 = run_bounded_noise_threshold_workflow()
    assert r2.audit_verdict == "PASS"
    assert not r2.unresolved
    assert "BOUNDED_NOISE_NOT_FULL_SVT" in r2.limitations
    assert "LAPLACE_CDF_IDENTITY_NOT_DP_PROOF" in r2.limitations


def test_intake_replay_idempotency():
    from operators.thresholding.discovery import discover_thresholding
    from system_a.fsm import State
    from system_a.gates import GateDecision
    from system_a.orchestrator import DiscoveryOrchestrator

    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = "b" * 64
    for s in (State.DS01, State.DS02, State.DS03):
        orch.advance(s)
    tips = discover_thresholding(orch.ir)
    orch.advance(State.DS05)
    orch.ir.upsert_branch("thresholding", [tips["theorem"]])
    orch.ir.add_dep(tips["theorem"], tips["assumptions"], "depends")
    orch.ir.add_dep(tips["theorem"], tips["proof_sketch"], "depends")
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member("thresholding", "PHASE_A_CHARACTERIZATION", "threshold-preservation")
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    b = VerificationIntake(SCOPE)
    out1 = b.submit_sealed(snap)
    out2 = b.submit_sealed(snap)
    assert out1.status == IntakeStatus.ACCEPTED_DRAFT
    assert out2.status == IntakeStatus.ACCEPTED_DRAFT
    assert out1.receipt.crp_digest == out2.receipt.crp_digest == snap.crp.crp_digest


def test_idempotency_digest_stale_wrong_package_closed_session():
    """Replay guards: same key/digest; key≠digest conflict; stale digest; wrong-package; closed session."""
    from art_int.envelope import SubmissionEnvelope
    from art_int.errors import IdempotencyConflict, ProvenanceError
    from art_int.feedback import validate_feedback_for_prior
    from art_int.idempotency import check_idempotency_replay
    from operators.thresholding.discovery import discover_thresholding
    from system_a.fsm import State
    from system_a.gates import GateDecision
    from system_a.orchestrator import DiscoveryOrchestrator

    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = "b" * 64
    for s in (State.DS01, State.DS02, State.DS03):
        orch.advance(s)
    tips = discover_thresholding(orch.ir)
    orch.advance(State.DS05)
    orch.ir.upsert_branch("thresholding", [tips["theorem"]])
    orch.ir.add_dep(tips["theorem"], tips["assumptions"], "depends")
    orch.ir.add_dep(tips["theorem"], tips["proof_sketch"], "depends")
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member("thresholding", "PHASE_A_CHARACTERIZATION", "threshold-preservation")
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)

    b = VerificationIntake(SCOPE)
    out = b.submit_sealed(snap)
    eng = VerificationEngine()
    run = eng.run_from_package(crp=snap.crp, receipt=out.receipt, obligations=out.obligations)
    export = eng.export(out.receipt, out.obligations, run)

    # same idempotency key + same digest → replay
    env = SubmissionEnvelope(crp=snap.crp, idempotency_key=snap.crp.crp_digest)
    assert b.submit_envelope(env).replay is True

    # same key + changed digest → conflict
    other = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(claims=[_det_claim(statement=THEOREM_STATEMENT_DET + " X")]),
        sealed_at="t",
    )
    other.crp_digest = compute_crp_digest(other)
    with pytest.raises(IdempotencyConflict):
        check_idempotency_replay(
            idempotency_key=snap.crp.crp_digest,
            incoming_digest=other.crp_digest,
            prior_key=snap.crp.crp_digest,
            prior_digest=snap.crp.crp_digest,
        )

    # stale / DIGEST_MISMATCH: stated digest ≠ recomputed → rejected (not raised)
    stale = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(claims=[_det_claim()]),
        sealed_at="t",
        crp_digest="0" * 64,
    )
    stale_out = b.submit_package(stale)
    assert stale_out.status == IntakeStatus.REJECTED
    assert "DIGEST_MISMATCH" in stale_out.reason_codes

    # wrong-package feedback
    with pytest.raises(ProvenanceError):
        validate_feedback_for_prior(export, expected_crp_digest="f" * 64, receipt=out.receipt)

    # closed-session feedback rejected
    orch.start_submission_batch()
    orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
    orch.advance(State.DS12)
    orch.import_feedback(export)
    orch.close_from_batch_outcome()
    assert orch.session.close_reason is not None
    with pytest.raises(Exception):
        orch.import_feedback(export)
