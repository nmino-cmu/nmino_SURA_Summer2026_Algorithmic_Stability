"""Full A↔B integration workflows — sealed CRP is sole verification input."""

from __future__ import annotations

from dataclasses import dataclass

from art_int.enums import IntakeStatus
from system_a import engines as a_engines
from system_a.fsm import State
from system_a.gates import GateDecision
from system_a.orchestrator import DiscoveryOrchestrator
from system_b.engines import VerificationEngine
from system_b.intake import VerificationIntake

SCOPE = "a" * 64
PRINCIPAL = "b" * 64


@dataclass
class IntegrationResult:
    session_id: str
    sealed_digest: str
    crp_digest: str
    intake_status: str
    audit_verdict: str | None
    close_reason: str | None
    prior_minted: bool
    receipt_digest: str | None


def run_characterization_workflow(
    statement: str = "1+1=2",
    *,
    evaluation: str | None = "DEMO_TAUTOLOGY",
) -> IntegrationResult:
    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = PRINCIPAL
    for s in (State.DS01, State.DS02, State.DS03):
        orch.advance(s)
    op = a_engines.run_operator_analyzer(orch.ir, {"name": "argmax"})
    a_engines.run_instability_characterization(orch.ir, op.version_ids[0])
    th = a_engines.run_theorem(orch.ir, statement, evaluation=evaluation)
    a_engines.run_soft_attack(orch.ir, th.version_ids[0])
    a_engines.run_pareto_portfolio(orch.ir, th.version_ids)
    orch.advance(State.DS05)
    orch.ir.upsert_branch("main", th.version_ids)
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member("main", "PHASE_A_CHARACTERIZATION", "m1")
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    assert snap.sealed_digest == snap.crp.crp_digest

    b = VerificationIntake(SCOPE)
    out = b.submit_sealed(snap)
    eng = VerificationEngine()
    run = eng.run_from_package(crp=snap.crp, receipt=out.receipt, obligations=out.obligations)
    export = eng.export(out.receipt, out.obligations, run)

    orch.start_submission_batch()
    orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
    prior = False
    if out.status == IntakeStatus.ACCEPTED_DRAFT:
        orch.advance(State.DS12)
        orch.import_feedback(export)
        prior = any(v.artifact_class == "VerifierPrior" for v in orch.ir.versions.values())
        # revision loop after PARTIAL/FAIL: continue to DS05 for repair
        if run.audit_verdict and run.audit_verdict.value in ("FAIL", "ESCALATE_HUMAN"):
            orch.advance(State.DS05, reason="revise_after_feedback")
            a_engines.consume_verifier_prior(orch.ir, {"export_ref": export.export_digest})
            orch.close(reason="policy_directed_closure")
        else:
            orch.close_from_batch_outcome()

    return IntegrationResult(
        orch.session.session_id,
        snap.sealed_digest,
        snap.crp.crp_digest,
        out.status.value,
        run.audit_verdict.value if run.audit_verdict else None,
        orch.session.close_reason,
        prior,
        out.receipt.receipt_digest if out.receipt else None,
    )


def run_gate1_path() -> str:
    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = PRINCIPAL
    for s in (State.DS01, State.DS02, State.DS03):
        orch.advance(s)
    orch.set_gate1_required(True)
    orch.advance(State.DS04)
    orch.apply_gate1(GateDecision.APPROVE)
    return orch.session.state.value
