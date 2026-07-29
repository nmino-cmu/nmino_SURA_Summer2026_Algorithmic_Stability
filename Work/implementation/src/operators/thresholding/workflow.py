"""End-to-end Discovery → Verification for thresholding theorems."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from art_int.enums import IntakeStatus
from operators.thresholding.discovery import discover_thresholding
from system_a import engines as a_engines
from system_a.fsm import State
from system_a.gates import GateDecision
from system_a.orchestrator import DiscoveryOrchestrator
from system_b.engines import VerificationEngine
from system_b.intake import VerificationIntake
from system_b.lean.bundle import export_bundle, verification_run_to_dicts, write_bundle

SCOPE = "a" * 64
PRINCIPAL = "b" * 64


@dataclass
class ThresholdResearchResult:
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
    which: str
    lean_bundle_path: str | None = None


def _run_one(
    branch: str,
    theorem_key: str,
    local_id: str,
    which: str,
    *,
    noisy: bool = False,
    export_lean_bundle: bool = False,
) -> ThresholdResearchResult:
    orch = DiscoveryOrchestrator.create()
    orch.scope_pin = SCOPE
    orch.principal = PRINCIPAL
    for s in (State.DS01, State.DS02, State.DS03):
        orch.advance(s)
    tips = discover_thresholding(orch.ir)
    th = tips[theorem_key]
    orch.advance(State.DS05)
    orch.ir.upsert_branch(branch, [th])
    if noisy:
        assum = a_engines.run_assumptions(
            orch.ir,
            "Finite x,T; η≥0; |ξ|≤η a.s.; Ã=1{x+ξ≥T}; equality x≥T passes; "
            "full Sparse Vector privacy not assumed.",
        )
        sketch = a_engines.run_proof_strategy(orch.ir, th)
        orch.ir.add_dep(th, assum.version_ids[0], "depends")
        orch.ir.add_dep(th, sketch.version_ids[0], "depends")
    else:
        orch.ir.add_dep(th, tips["assumptions"], "depends")
        orch.ir.add_dep(th, tips["proof_sketch"], "depends")
    orch.advance(State.DS07)
    orch.advance(State.DS08)
    vid = orch.compile_portfolio_member(branch, "PHASE_A_CHARACTERIZATION", local_id)
    orch.advance(State.DS09)
    orch.apply_gate3(GateDecision.APPROVE, seal_set=[vid])
    snap = orch.seal_authorized(vid)
    assert snap.sealed_digest == snap.crp.crp_digest

    b = VerificationIntake(SCOPE)
    out = b.submit_sealed(snap)
    eng = VerificationEngine()
    run = eng.run_from_package(crp=snap.crp, receipt=out.receipt, obligations=out.obligations)
    export = eng.export(out.receipt, out.obligations, run)

    lean_bundle_path = None
    if export_lean_bundle and out.status == IntakeStatus.ACCEPTED_DRAFT:
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
        lean_bundle_path = str(dest)

    orch.start_submission_batch()
    orch.record_intake(snap.sealed_digest, out.status, out.receipt.receipt_digest)
    if out.status == IntakeStatus.ACCEPTED_DRAFT:
        orch.advance(State.DS12)
        orch.import_feedback(export)
        orch.close_from_batch_outcome()

    unresolved = tuple(r.obligation_digest for r in run.results if r.status.value == "OPEN")
    return ThresholdResearchResult(
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
        which,
        lean_bundle_path,
    )


def run_threshold_preservation_workflow(*, export_lean_bundle: bool = False) -> ThresholdResearchResult:
    return _run_one(
        "thresholding",
        "theorem",
        "threshold-preservation",
        "deterministic",
        export_lean_bundle=export_lean_bundle,
    )


def run_bounded_noise_threshold_workflow(*, export_lean_bundle: bool = False) -> ThresholdResearchResult:
    return _run_one(
        "thresholding-noisy",
        "theorem_noisy",
        "threshold-bounded-noise",
        "noisy",
        noisy=True,
        export_lean_bundle=export_lean_bundle,
    )
