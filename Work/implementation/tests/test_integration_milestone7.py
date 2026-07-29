"""Milestone 7 — full system integration workflows."""

from integration.workflows import run_characterization_workflow, run_gate1_path
from system_a.fsm import State
from system_a.orchestrator import DiscoveryOrchestrator


def test_e2e_argmax_characterization_pass():
    r = run_characterization_workflow("1+1=2", evaluation="DEMO_TAUTOLOGY")
    assert r.intake_status == "ACCEPTED_DRAFT"
    assert r.audit_verdict == "PASS"
    assert r.sealed_digest == r.crp_digest
    assert r.prior_minted is True
    assert r.receipt_digest
    assert r.close_reason == "completed_submitted"


def test_e2e_unmarked_statement_not_pass():
    r = run_characterization_workflow("1+1=2", evaluation=None)
    assert r.audit_verdict == "ESCALATE_HUMAN"


def test_e2e_fail_revision_loop():
    r = run_characterization_workflow("false", evaluation="DEMO_COUNTEREXAMPLE")
    assert r.audit_verdict == "FAIL"
    assert r.prior_minted is True
    assert r.close_reason == "policy_directed_closure"


def test_e2e_partial_incomplete():
    r = run_characterization_workflow("incomplete", evaluation="DEMO_INCOMPLETE")
    assert r.audit_verdict == "ESCALATE_HUMAN"
    assert r.prior_minted is True


def test_e2e_gate1_and_replay():
    assert run_gate1_path() == "DS05"
    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = "a" * 64
    for s in (State.DS01, State.DS02, State.DS03, State.DS05):
        orch.advance(s)
    assert orch.replay_state() == State.DS05
