"""Milestone 2 — System A core runtime (adversarial + conformance)."""

from __future__ import annotations

import pytest

from art_int.enums import IntakeStatus, TransportResult
from art_int.errors import ProvenanceError
from art_int.feedback import VerifierFeedbackExport, finalize_export
from system_a.fsm import IllegalTransition, SessionEvent, State, replay_control
from system_a.gates import GateDecision
from system_a.ir import DiscoveryIR, ImmutableError, OwnershipError
from system_a.orchestrator import DiscoveryOrchestrator
from system_a.ownership import CLASS_OWNER
from system_a.packager import compile_branch


def _mint_theorem(orch: DiscoveryOrchestrator, statement: str = "1+1=2"):
    return orch.ir.mint(
        artifact_class="TheoremCandidate",
        caller_module="ATP_ENGINE",
        payload={"statement": statement, "chain_segment": "characterization"},
    )


def happy_to_ds03(orch: DiscoveryOrchestrator) -> None:
    orch.advance(State.DS01)
    orch.advance(State.DS02)
    orch.advance(State.DS03)


def happy_to_gate3(orch: DiscoveryOrchestrator) -> str:
    happy_to_ds03(orch)
    orch.set_gate1_required(False)
    orch.set_gate2_required(False)
    orch.advance(State.DS05, reason="no_gate1")
    orch.skip_gate(1)
    tip = _mint_theorem(orch)
    orch.ir.upsert_branch("br1", [tip.version_id], label="main")
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member("br1", "PHASE_A_CHARACTERIZATION", "m1")
    orch.advance(State.DS09)
    return vid


def _export(crp_digest: str) -> VerifierFeedbackExport:
    return finalize_export(
        VerifierFeedbackExport(
            crp_digest=crp_digest,
            sealed_digest=crp_digest,
            intake_status=IntakeStatus.ACCEPTED_DRAFT,
            profile="PHASE_A_CHARACTERIZATION",
            draft_claim_digests=["c1"],
            obligation_digests=["o1"],
            obligations=[{"obligation_digest": "o1", "draft_claim_digest": "c1"}],
        )
    )


def test_legal_happy_path_to_close():
    orch = DiscoveryOrchestrator.create("s1")
    vid = happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    orch.start_submission_batch()
    orch.record_intake(snap.sealed_digest, IntakeStatus.ACCEPTED_DRAFT, receipt_ref="r1")
    orch.close_from_batch_outcome()
    assert orch.session.state == State.DS13
    assert orch.session.close_reason == "completed_submitted"
    assert orch.ir.closed


def test_foreign_cannot_commit_fsm():
    orch = DiscoveryOrchestrator.create("x")
    other = DiscoveryOrchestrator.create("y")
    with pytest.raises(IllegalTransition):
        orch.session._commit(other, State.DS01)
    # integer spoof no longer applicable; owner is weakref identity
    assert orch.session._owner_ref() is orch


def test_cannot_bypass_gate1_without_decision():
    orch = DiscoveryOrchestrator.create()
    happy_to_ds03(orch)
    orch.set_gate1_required(True)
    orch.advance(State.DS04)
    with pytest.raises(IllegalTransition, match="gate"):
        orch.advance(State.DS05)


def test_duplicate_seal_set_rejected():
    orch = DiscoveryOrchestrator.create()
    vid = happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid, vid])
    assert orch.session.state == State.DS09


def test_close_rejects_open_batch():
    orch = DiscoveryOrchestrator.create()
    vid = happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    orch.seal_authorized(vid)
    orch.start_submission_batch()
    with pytest.raises(IllegalTransition):
        orch.close()


def test_nested_payload_compiles_to_wire():
    ir = DiscoveryIR("s")
    tip = ir.mint(
        artifact_class="TheoremCandidate",
        caller_module="ATP_ENGINE",
        payload={"statement": "p", "chain_segment": "characterization", "metadata": {"nested": 1}},
    )
    ir.upsert_branch("b", [tip.version_id])
    draft = compile_branch(
        ir, branch_id="b", profile_hint="PHASE_A_CHARACTERIZATION", math_scope_pin_digest="a" * 64
    )
    wire = draft.to_wire()  # type: ignore
    assert wire["payload"]["claims"][0]["metadata"]["nested"] == 1


def test_gate3_exit_requires_decision():
    orch = DiscoveryOrchestrator.create()
    happy_to_gate3(orch)
    with pytest.raises(IllegalTransition, match="gate"):
        orch.advance(State.DS13, reason="gate3_rejected")


def test_gate3_revise_mints_ir_gate_record():
    orch = DiscoveryOrchestrator.create()
    happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.REVISE)
    assert orch.session.state == State.DS07
    assert any(
        v.artifact_class == "GateRecord" and v.payload.get("decision") == "revise"
        for v in orch.ir.versions.values()
    )


def test_gate1_blocks_and_approve_mints_scope():
    orch = DiscoveryOrchestrator.create()
    happy_to_ds03(orch)
    orch.set_gate1_required(True)
    with pytest.raises(IllegalTransition):
        orch.advance(State.DS05)
    orch.advance(State.DS04)
    orch.apply_gate1(GateDecision.APPROVE)
    assert orch.session.scope_binding_version == 1
    assert any(v.artifact_class == "ScopeBinding" for v in orch.ir.versions.values())


def test_cannot_skip_required_gate1():
    orch = DiscoveryOrchestrator.create()
    happy_to_ds03(orch)
    orch.set_gate1_required(True)
    with pytest.raises(IllegalTransition):
        orch.skip_gate(1)


def test_gate2_path():
    orch = DiscoveryOrchestrator.create()
    happy_to_ds03(orch)
    orch.advance(State.DS05)
    orch.set_gate2_required(True)
    with pytest.raises(IllegalTransition):
        orch.advance(State.DS07)
    orch.advance(State.DS06)
    orch.apply_gate2(GateDecision.APPROVE)
    assert orch.session.state == State.DS07


def test_gate3_no_silent_narrowing():
    orch = DiscoveryOrchestrator.create()
    vid = happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid, "forged"])
    assert orch.session.state == State.DS09
    assert orch.session.seal_set == ()


def test_gate3_waiver_requires_preinstalled_policy():
    orch = DiscoveryOrchestrator.create()
    tip = _mint_theorem(orch)
    orch.ir.upsert_branch("br1", [tip.version_id])
    happy_to_ds03(orch)
    orch.advance(State.DS05)
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member("br1", "PHASE_A_CHARACTERIZATION", "m1")
    orch.install_gate3_waiver_policy([vid])
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.WAIVE, seal_set=None)
    assert orch.session.state == State.DS10


def test_gate3_waiver_without_policy_incomplete():
    orch = DiscoveryOrchestrator.create()
    happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.WAIVE, seal_set=None)
    assert orch.session.state == State.DS09


def test_duplicate_seal_rejected_and_bijection():
    orch = DiscoveryOrchestrator.create()
    happy_to_ds03(orch)
    orch.advance(State.DS05)
    t1 = _mint_theorem(orch, "a")
    t2 = _mint_theorem(orch, "b")
    orch.ir.upsert_branch("b1", [t1.version_id])
    orch.ir.upsert_branch("b2", [t2.version_id])
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    v1 = orch.compile_portfolio_member("b1", "PHASE_A_CHARACTERIZATION", "m1")
    v2 = orch.compile_portfolio_member("b2", "PHASE_A_CHARACTERIZATION", "m2")
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[v1, v2])
    orch.seal_authorized(v1)
    with pytest.raises(RuntimeError):
        orch.seal_authorized(v1)
    with pytest.raises(IllegalTransition):
        orch.advance(State.DS11)
    orch.seal_authorized(v2)
    orch.advance(State.DS11)


def test_one_batch_per_wave():
    orch = DiscoveryOrchestrator.create()
    vid = happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    b1 = orch.start_submission_batch()
    b2 = orch.start_submission_batch()
    assert b1.batch_id == b2.batch_id
    assert any(v.artifact_class == "SubmissionBatch" for v in orch.ir.versions.values())
    orch.record_intake(snap.sealed_digest, IntakeStatus.ACCEPTED_DRAFT, receipt_ref="r1")
    with pytest.raises(RuntimeError):
        orch.retry_failed_transport(snap.sealed_digest)


def test_cannot_close_pending_batch():
    orch = DiscoveryOrchestrator.create()
    vid = happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    orch.seal_authorized(vid)
    orch.start_submission_batch()
    with pytest.raises(IllegalTransition):
        orch.close_from_batch_outcome()


def test_ds91_from_active_for_corruption():
    orch = DiscoveryOrchestrator.create()
    happy_to_ds03(orch)
    orch.advance(State.DS05)
    orch.advance(State.DS91, reason="corrupted_event_history")
    assert orch.session.state == State.DS91


def test_ds91_rejects_empty_frontier_reason():
    orch = DiscoveryOrchestrator.create()
    orch.advance(State.DS01)
    with pytest.raises(IllegalTransition):
        orch.advance(State.DS91, reason="empty_frontier")


def test_ownership_registry_frozen_and_enforced():
    with pytest.raises(TypeError):
        CLASS_OWNER["TheoremCandidate"] = "SOFT_ATTACK"  # type: ignore
    ir = DiscoveryIR("s")
    with pytest.raises(OwnershipError):
        ir.mint(artifact_class="TheoremCandidate", caller_module="SOFT_ATTACK", payload={})


def test_deep_freeze_nested_payload():
    ir = DiscoveryIR("s")
    v = ir.mint(
        artifact_class="AssumptionDraft",
        caller_module="RESEARCH_DISCOVERY_ASSISTANT",
        payload={"nested": {"x": 1}, "arr": [1, 2]},
    )
    with pytest.raises(TypeError):
        v.payload["nested"]["x"] = 99  # type: ignore
    with pytest.raises(TypeError):
        v.payload["arr"][0] = 9  # type: ignore


def test_replay_rejects_illegal_edge_and_mixed_session():
    orch = DiscoveryOrchestrator.create("replay")
    happy_to_ds03(orch)
    assert orch.replay_state() == State.DS03
    bad = (
        SessionEvent("e1", "sA", "SessionOpened", 1, "t1", {"session_id": "sA"}),
        SessionEvent("e2", "sA", "Transition", 2, "t2", {"from": "DS00", "to": "DS12", "reason": ""}),
    )
    with pytest.raises(IllegalTransition):
        replay_control(bad)


def test_packager_projects_closure_mechanisms():
    ir = DiscoveryIR("s")
    claim = ir.mint(
        artifact_class="TheoremCandidate",
        caller_module="ATP_ENGINE",
        payload={"statement": "p", "chain_segment": "characterization"},
    )
    mech = ir.mint(
        artifact_class="MechanismProposal",
        caller_module="MECHANISM_DESIGNER",
        payload={"id": "m1"},
    )
    ir.add_dep(claim.version_id, mech.version_id, "mechanism_for")
    ir.upsert_branch("b", [claim.version_id])
    draft = compile_branch(
        ir, branch_id="b", profile_hint="PHASE_B_STABILIZATION", math_scope_pin_digest="a" * 64
    )
    assert isinstance(draft, type(draft)) and hasattr(draft, "payload")
    assert draft.payload.mechanism_proposals  # type: ignore
    d1 = draft.dep_closure_digest  # type: ignore
    ir.add_dep(mech.version_id, claim.version_id, "uses_def")  # will create cycle on next compile
    # new edge changes digest even before cycle fail — recompile tips-only branch without cycle edge from tips
    ir2 = DiscoveryIR("s2")
    c2 = ir2.mint(
        artifact_class="TheoremCandidate",
        caller_module="ATP_ENGINE",
        payload={"statement": "p", "chain_segment": "characterization"},
    )
    m2 = ir2.mint(
        artifact_class="MechanismProposal",
        caller_module="MECHANISM_DESIGNER",
        payload={"id": "m1"},
    )
    ir2.add_dep(c2.version_id, m2.version_id, "mechanism_for")
    ir2.upsert_branch("b", [c2.version_id])
    d_a = compile_branch(
        ir2, branch_id="b", profile_hint="PHASE_B_STABILIZATION", math_scope_pin_digest="a" * 64
    ).dep_closure_digest  # type: ignore
    ir2.add_dep(c2.version_id, m2.version_id, "sketches")
    d_b = compile_branch(
        ir2, branch_id="b", profile_hint="PHASE_B_STABILIZATION", math_scope_pin_digest="a" * 64
    ).dep_closure_digest  # type: ignore
    assert d_a != d_b


def test_feedback_and_cross_session_import():
    orch = DiscoveryOrchestrator.create("src")
    vid = happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    orch.start_submission_batch()
    orch.record_intake(snap.sealed_digest, IntakeStatus.ACCEPTED_DRAFT, receipt_ref="r1")
    orch.advance(State.DS12)
    orch.import_feedback(_export(snap.sealed_digest))
    orch.close_from_batch_outcome()

    orch2 = DiscoveryOrchestrator.create("dst")
    happy_to_ds03(orch2)
    orch2.advance(State.DS05)
    orch2.attest_foreign_seal("src", snap.sealed_digest)
    prior = orch2.import_feedback(
        _export(snap.sealed_digest),
        authorized_import=True,
        source_session_id="src",
    )
    assert prior["active"] is True
    assert prior["source_session_id"] == "src"


def test_feedback_after_close_archival():
    orch = DiscoveryOrchestrator.create()
    vid = happy_to_gate3(orch)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    orch.start_submission_batch()
    orch.record_intake(snap.sealed_digest, IntakeStatus.ACCEPTED_DRAFT, receipt_ref="r1")
    orch.close_from_batch_outcome()
    with pytest.raises(IllegalTransition):
        orch.import_feedback(_export(snap.sealed_digest), active=True)
    orch.import_feedback(_export(snap.sealed_digest), active=False)


def test_terminal_closes_ir():
    orch = DiscoveryOrchestrator.create()
    orch.advance(State.DS90)
    assert orch.ir.closed
    with pytest.raises(ImmutableError):
        _mint_theorem(orch)
