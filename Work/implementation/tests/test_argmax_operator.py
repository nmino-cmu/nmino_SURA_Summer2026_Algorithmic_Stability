"""Argmax operator — math, verification, e2e."""

from __future__ import annotations

import pytest

from art_int.enums import AuditVerdict, ObligationStatus
from operators.argmax.math import (
    EVALUATION_METHOD,
    THEOREM_STATEMENT,
    ArgmaxInstance,
    adversarial_break,
    apply_perturbation,
    invariance_holds,
)
from operators.argmax.verify import verify_margin_theorem
from operators.argmax.workflow import run_argmax_margin_workflow
from system_b.engines import VerificationEngine
from system_b.intake import VerificationIntake
from art_int.crp import CandidateResearchPackage, CrpPayload, compute_crp_digest
from art_int.enums import AuthorKind, CrpProfile


SCOPE = "a" * 64


def test_unique_winner_and_margin():
    a = ArgmaxInstance((3.0, 1.0, 0.5))
    assert a.unique_maximizer() == 0
    assert a.margin() == pytest.approx(2.0)


def test_ties():
    a = ArgmaxInstance((1.0, 1.0, 0.5))
    assert a.unique_maximizer() is None
    assert a.margin() is None
    assert a.maximizers() == (0, 1)


def test_near_ties_and_boundary():
    scores = (1.0, 0.0)
    assert ArgmaxInstance(scores).margin() == pytest.approx(1.0)
    assert invariance_holds(scores, 0.4)  # 1 > 0.8
    assert not invariance_holds(scores, 0.5)  # 1 ≯ 1


def test_perturbation_invariance():
    scores = (5.0, 1.0, 0.0)
    eps = 1.5  # γ=4 > 3
    assert invariance_holds(scores, eps)
    delta = (-eps, eps, eps)
    after = ArgmaxInstance(apply_perturbation(scores, delta))
    assert after.unique_maximizer() == 0


def test_counterexample_sharpness():
    scores = (3.0, 1.0)
    eps = 1.0  # γ=2 ≯ 2
    br = adversarial_break(scores, eps)
    assert br is not None
    after = ArgmaxInstance(apply_perturbation(scores, br))
    assert after.unique_maximizer() is None or after.unique_maximizer() != 0


def test_malformed_empty():
    with pytest.raises(ValueError):
        ArgmaxInstance(())
    with pytest.raises(ValueError):
        ArgmaxInstance((1.0,))
    with pytest.raises(ValueError):
        invariance_holds((3.0, 1.0), -0.1)


def test_verify_rejects_statement_smuggling():
    claim = {
        "statement": THEOREM_STATEMENT + " AND 1=0",
        "operator": "argmax",
        "theorem_id": "bounded-perturbation-margin",
        "evaluation": EVALUATION_METHOD,
        "formal": {
            "perturbation_norm": "linf",
            "margin_definition": "s_i_star - max_{j!=i_star} s_j",
            "invariance_condition": "gamma > 2*epsilon",
        },
    }
    assert verify_margin_theorem(claim).ok is False
    assert verify_margin_theorem(claim).detail == "statement_mismatch"


def test_verify_rejects_bad_claim():
    bad = {"statement": "wrong", "operator": "argmax", "theorem_id": "bounded-perturbation-margin", "evaluation": EVALUATION_METHOD}
    assert verify_margin_theorem(bad).ok is False


def test_verify_canonical_claim():
    claim = {
        "statement": THEOREM_STATEMENT,
        "operator": "argmax",
        "theorem_id": "bounded-perturbation-margin",
        "evaluation": EVALUATION_METHOD,
        "sharpness_statement": (
            "Under the same setup, if γ(s)≤2ε then there exists δ with ||δ||_∞≤ε "
            "such that i* is not the unique maximizer of s+δ."
        ),
        "formal": {
            "perturbation_norm": "linf",
            "margin_definition": "s_i_star - max_{j!=i_star} s_j",
            "invariance_condition": "gamma > 2*epsilon",
        },
    }
    assert verify_margin_theorem(claim).ok


def test_engine_discharges_argmax_not_demo():
    claim = {
        "statement": THEOREM_STATEMENT,
        "chain_segment": "inference",
        "operator": "argmax",
        "theorem_id": "bounded-perturbation-margin",
        "evaluation": EVALUATION_METHOD,
        "formal": {
            "perturbation_norm": "linf",
            "margin_definition": "s_i_star - max_{j!=i_star} s_j",
            "invariance_condition": "gamma > 2*epsilon",
        },
    }
    crp = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(claims=[claim]),
        sealed_at="t",
    )
    crp.crp_digest = compute_crp_digest(crp)
    out = VerificationIntake(SCOPE).submit_package(crp)
    run = VerificationEngine().run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    assert run.audit_verdict == AuditVerdict.PASS
    assert all(r.status == ObligationStatus.DISCHARGED for r in run.results)
    assert "COMPUTATIONAL_VERIFICATION_NOT_LEAN" in run.limitations
    assert not any(x.startswith("DEMO_") for x in run.limitations)


def test_e2e_workflow_and_intake_replay():
    r1 = run_argmax_margin_workflow()
    assert r1.audit_verdict == "PASS"
    assert not r1.unresolved
    assert "COMPUTATIONAL_VERIFICATION_NOT_LEAN" in r1.limitations

    # idempotent intake replay: resubmit same sealed CRP content via digest key
    from operators.argmax.discovery import discover_argmax
    from system_a.fsm import State
    from system_a.gates import GateDecision
    from system_a.orchestrator import DiscoveryOrchestrator
    from system_b.intake import VerificationIntake
    from art_int.enums import IntakeStatus

    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = "b" * 64
    for s in (State.DS01, State.DS02, State.DS03):
        orch.advance(s)
    tips = discover_argmax(orch.ir)
    orch.advance(State.DS05)
    orch.ir.upsert_branch("argmax", [tips["theorem"]])
    orch.ir.add_dep(tips["theorem"], tips["assumptions"], "depends")
    orch.ir.add_dep(tips["theorem"], tips["proof_sketch"], "depends")
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member("argmax", "PHASE_A_CHARACTERIZATION", "argmax-margin")
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    b = VerificationIntake(SCOPE)
    out1 = b.submit_sealed(snap)
    out2 = b.submit_sealed(snap)
    assert out1.status == IntakeStatus.ACCEPTED_DRAFT
    assert out2.status == IntakeStatus.ACCEPTED_DRAFT
    assert out1.receipt.crp_digest == out2.receipt.crp_digest == snap.crp.crp_digest
