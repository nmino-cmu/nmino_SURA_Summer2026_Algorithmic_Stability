"""Milestone 6 — System B verification engines."""

from art_int.crp import CandidateResearchPackage, CrpPayload, compute_crp_digest
from art_int.enums import AuditVerdict, AuthorKind, CrpProfile, ObligationStatus
from system_b.engines import OutcomeKind, VerificationEngine
from system_b.intake import VerificationIntake

SCOPE = "a" * 64


def _admit(statement: str, evaluation: str | None = None):
    claim = {"statement": statement, "chain_segment": "characterization"}
    if evaluation:
        claim["evaluation"] = evaluation
    crp = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(claims=[claim]),
        sealed_at="t",
    )
    crp.crp_digest = compute_crp_digest(crp)
    b = VerificationIntake(SCOPE)
    out = b.submit_package(crp)
    return crp, out


def test_true_and_false_proposition():
    eng = VerificationEngine()
    crp, ok = _admit("1+1=2", "DEMO_TAUTOLOGY")
    run = eng.run_from_package(crp=crp, receipt=ok.receipt, obligations=ok.obligations)
    assert run.audit_verdict == AuditVerdict.PASS
    crp2, bad = _admit("false", "DEMO_COUNTEREXAMPLE")
    run2 = eng.run_from_package(crp=crp2, receipt=bad.receipt, obligations=bad.obligations)
    assert run2.audit_verdict == AuditVerdict.FAIL
    assert run2.counterexamples


def test_unmarked_string_never_pass():
    eng = VerificationEngine()
    crp, out = _admit("1+1=2", evaluation=None)
    run = eng.run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    assert run.audit_verdict != AuditVerdict.PASS
    assert all(r.kind == OutcomeKind.PROOF_INCOMPLETE for r in run.results)


def test_incomplete_and_assumptions():
    eng = VerificationEngine()
    crp, out = _admit("incomplete", "DEMO_INCOMPLETE")
    run = eng.run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    assert run.audit_verdict == AuditVerdict.ESCALATE_HUMAN
    crp2, out2 = _admit("true", "DEMO_TAUTOLOGY")
    run2 = eng.run_from_package(
        crp=crp2,
        receipt=out2.receipt,
        obligations=out2.obligations,
        assumptions=[{"contradictory": True}],
    )
    assert run2.audit_verdict == AuditVerdict.FAIL
    assert run2.results[0].kind == OutcomeKind.INVALID_ASSUMPTIONS


def test_multi_claim_no_cross_discharge():
    eng = VerificationEngine()
    crp = CandidateResearchPackage(
        author_kind=AuthorKind.HUMAN,
        author_principal_digest="b" * 64,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION,
        math_scope_pin_digest=SCOPE,
        payload=CrpPayload(
            claims=[
                {"statement": "true", "chain_segment": "characterization", "evaluation": "DEMO_TAUTOLOGY"},
                {"statement": "incomplete", "chain_segment": "characterization", "evaluation": "DEMO_INCOMPLETE"},
            ]
        ),
        sealed_at="t",
    )
    crp.crp_digest = compute_crp_digest(crp)
    out = VerificationIntake(SCOPE).submit_package(crp)
    run = eng.run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    assert run.audit_verdict != AuditVerdict.PASS
    assert any(r.kind == OutcomeKind.PROOF_INCOMPLETE for r in run.results)


def test_infra_and_supersession_immutable():
    eng = VerificationEngine()
    crp, out = _admit("true", "DEMO_TAUTOLOGY")
    r1 = eng.run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations, force_infra=True)
    assert "INFRA_FAILURE" in r1.limitations
    assert r1.audit_verdict is None
    r2 = eng.run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    eng.supersede(r1.run_id, r2)
    assert eng.runs[r1.run_id].superseded_by == r2.run_id
    assert eng.runs[r1.run_id]._frozen


def test_feedback_export_status_aligned():
    eng = VerificationEngine()
    crp, out = _admit("1+1=2", "DEMO_TAUTOLOGY")
    run = eng.run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    ex = eng.export(out.receipt, out.obligations, run)
    assert ex.crp_digest == out.receipt.crp_digest
    assert all(o.get("status") == ObligationStatus.DISCHARGED.value for o in ex.obligations)
    assert set(ex.discharged_obligations) == {o["obligation_digest"] for o in ex.obligations}


def test_demo_limitations_surface_on_export():
    eng = VerificationEngine()
    crp, out = _admit("1+1=2", "DEMO_TAUTOLOGY")
    run = eng.run_from_package(crp=crp, receipt=out.receipt, obligations=out.obligations)
    ex = eng.export(out.receipt, out.obligations, run)
    assert any(x.startswith("DEMO_EVALUATION:") for x in ex.verifier_limitations)
