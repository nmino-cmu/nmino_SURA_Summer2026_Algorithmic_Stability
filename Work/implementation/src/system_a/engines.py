"""System A mathematical engines — typed Discovery IR only; no seal/submit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from system_a.ir import DiscoveryIR, OwnershipError
from system_a.ownership import CLASS_OWNER


@dataclass
class EngineResult:
    engine: str
    version_ids: list[str]
    speculative: bool
    error: str | None = None


def _mint(ir: DiscoveryIR, cls: str, payload: dict[str, Any], *, speculative: bool = False) -> str:
    owner = CLASS_OWNER[cls]
    body = dict(payload)
    if speculative:
        body["speculative"] = True
        body["speculation_label"] = "SPECULATIVE"
    return ir.mint(artifact_class=cls, caller_module=owner, payload=body).version_id


def run_operator_analyzer(ir: DiscoveryIR, operator_spec: dict[str, Any]) -> EngineResult:
    vid = _mint(ir, "OperatorAnalysis", {"operator": operator_spec})
    return EngineResult("OPERATOR_ANALYZER", [vid], False)


def run_instability_characterization(ir: DiscoveryIR, analysis_ref: str) -> EngineResult:
    vid = _mint(
        ir,
        "ExampleCard",
        {"kind": "instability", "analysis_ref": analysis_ref, "chain_segment": "characterization"},
        speculative=True,
    )
    return EngineResult("CONJECTURE_ENGINE", [vid], True)


def run_structural_quantity(ir: DiscoveryIR, tip_ref: str) -> EngineResult:
    vid = _mint(ir, "StructuralQuantity", {"of": tip_ref, "quantity": "stability_margin"})
    return EngineResult("STRUCTURAL_QUANTITY", [vid], False)


def run_mechanism(ir: DiscoveryIR, tip_ref: str) -> EngineResult:
    vid = _mint(ir, "MechanismProposal", {"local_id": "mech-1", "of": tip_ref}, speculative=True)
    return EngineResult("MECHANISM_DESIGNER", [vid], True)


def run_psi_construction(ir: DiscoveryIR, tip_ref: str) -> EngineResult:
    vid = _mint(ir, "DefinitionDraft", {"name": "psi", "of": tip_ref}, speculative=True)
    return EngineResult("RESEARCH_DISCOVERY_ASSISTANT", [vid], True)


def run_theorem(ir: DiscoveryIR, statement: str, *, evaluation: str | None = None) -> EngineResult:
    payload: dict[str, Any] = {"statement": statement, "chain_segment": "inference"}
    if evaluation:
        payload["evaluation"] = evaluation
    vid = _mint(ir, "TheoremCandidate", payload, speculative=False)
    return EngineResult("ATP_ENGINE", [vid], False)


def run_conjecture(ir: DiscoveryIR, statement: str) -> EngineResult:
    vid = _mint(
        ir,
        "ConjectureCandidate",
        {"statement": statement, "chain_segment": "characterization"},
        speculative=True,
    )
    return EngineResult("CONJECTURE_ENGINE", [vid], True)


def run_bridge(ir: DiscoveryIR, left: str, right: str) -> EngineResult:
    vid = _mint(ir, "BridgeProposalDraft", {"left": left, "right": right}, speculative=True)
    return EngineResult("RESEARCH_DISCOVERY_ASSISTANT", [vid], True)


def run_proof_strategy(ir: DiscoveryIR, claim_ref: str) -> EngineResult:
    vid = _mint(ir, "ProofSketch", {"claim_ref": claim_ref, "steps": ["expand", "bound"]}, speculative=True)
    return EngineResult("PROOF_SKETCHER", [vid], True)


def run_assumptions(ir: DiscoveryIR, text: str) -> EngineResult:
    vid = _mint(ir, "AssumptionDraft", {"text": text})
    return EngineResult("RESEARCH_DISCOVERY_ASSISTANT", [vid], False)


def run_utility_tradeoff(ir: DiscoveryIR, members: list[str]) -> EngineResult:
    vid = _mint(ir, "PortfolioMember", {"member_refs": members, "utility": {"novelty": "medium", "tractability": "medium"}})
    return EngineResult("PORTFOLIO_MANAGER", [vid], False)


def run_open_questions(ir: DiscoveryIR, text: str) -> EngineResult:
    vid = _mint(ir, "FalsificationTarget", {"question": text}, speculative=True)
    return EngineResult("CONJECTURE_ENGINE", [vid], True)


def run_pareto_portfolio(ir: DiscoveryIR, member_ids: list[str]) -> EngineResult:
    """Diversity-aware portfolio frontier (non-dominated by declared utilities)."""
    vid = _mint(
        ir,
        "PortfolioFrontier",
        {"members": member_ids, "rule": "pareto_nondominated", "diverse": True},
    )
    return EngineResult("PORTFOLIO_MANAGER", [vid], False)


def run_soft_attack(ir: DiscoveryIR, target_ref: str) -> EngineResult:
    """Non-authoritative attack log + rewrite proposal; cannot seal/submit."""
    log = _mint(ir, "SoftAttackLog", {"target": target_ref, "outcome": "pressure", "authoritative": False})
    rw = _mint(ir, "RewriteProposal", {"target": target_ref, "suggestion": "strengthen assumptions"}, speculative=True)
    return EngineResult("SOFT_ATTACK", [log, rw], True)


def run_literature(ir: DiscoveryIR, cite: str) -> EngineResult:
    node = _mint(ir, "LiteratureNode", {"cite": cite})
    nov = _mint(ir, "NoveltyAssessment", {"cite": cite, "overlap": "low"}, speculative=True)
    return EngineResult("NOVELTY_LITERATURE", [node, nov], True)


def consume_verifier_prior(ir: DiscoveryIR, prior_payload: dict[str, Any]) -> EngineResult:
    """Read-only influence: mint AssumptionDraft informed by prior; does not mutate sealed artifacts."""
    vid = _mint(
        ir,
        "AssumptionDraft",
        {"text": "informed_by_verifier_prior", "prior_ref": prior_payload.get("export_ref"), "speculative": False},
    )
    return EngineResult("RESEARCH_DISCOVERY_ASSISTANT", [vid], False)


def assert_no_seal_submit_authority(module_name: str) -> None:
    if module_name in ("SOFT_ATTACK", "ATP_ENGINE", "CONJECTURE_ENGINE", "MECHANISM_DESIGNER"):
        # engines must not own SealedCRPSnapshot / SubmissionAttempt
        assert CLASS_OWNER["SealedCRPSnapshot"] == "RESEARCH_DISCOVERY_ASSISTANT"
        assert CLASS_OWNER["SubmissionAttempt"] == "DISCOVERY_ORCHESTRATOR"


def run_engine_safe(fn, ir: DiscoveryIR, *args, **kwargs) -> EngineResult:
    try:
        return fn(ir, *args, **kwargs)
    except Exception as e:
        return EngineResult(getattr(fn, "__name__", "engine"), [], False, error=str(e))
