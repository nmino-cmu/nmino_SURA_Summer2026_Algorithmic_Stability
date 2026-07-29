"""Frozen artifact class → owner module registry (ART-A-02 §1.4)."""

from __future__ import annotations

from types import MappingProxyType

_CLASS_OWNER_RAW: dict[str, str] = {
    "SessionRecord": "DISCOVERY_ORCHESTRATOR",
    "ScopeBinding": "DISCOVERY_ORCHESTRATOR",
    "GateRecord": "DISCOVERY_ORCHESTRATOR",
    "ScheduleEvent": "DISCOVERY_ORCHESTRATOR",
    "SessionEvent": "DISCOVERY_ORCHESTRATOR",
    "SessionPolicy": "DISCOVERY_ORCHESTRATOR",
    "SubmissionAttempt": "DISCOVERY_ORCHESTRATOR",
    "SubmissionBatch": "DISCOVERY_ORCHESTRATOR",
    "VerifierPrior": "DISCOVERY_ORCHESTRATOR",
    "ConflictRecord": "DISCOVERY_ORCHESTRATOR",
    "RevisionProposal": "DISCOVERY_ORCHESTRATOR",
    "Branch": "DISCOVERY_IR",
    "DepLink": "DISCOVERY_IR",
    "ArtifactLifecycleRecord": "DISCOVERY_IR",
    "FrontierState": "FRONTIER_SCHEDULER",
    "QuestionLock": "FRONTIER_SCHEDULER",
    "QuarantineRow": "FRONTIER_SCHEDULER",
    "OperatorAnalysis": "OPERATOR_ANALYZER",
    "LiteratureNode": "NOVELTY_LITERATURE",
    "LiteratureEdge": "NOVELTY_LITERATURE",
    "NoveltyAssessment": "NOVELTY_LITERATURE",
    "ExampleCard": "CONJECTURE_ENGINE",
    "ConjectureCandidate": "CONJECTURE_ENGINE",
    "FalsificationTarget": "CONJECTURE_ENGINE",
    "TheoremCandidate": "ATP_ENGINE",
    "DefinitionDraft": "RESEARCH_DISCOVERY_ASSISTANT",
    "AssumptionDraft": "RESEARCH_DISCOVERY_ASSISTANT",
    "BridgeProposalDraft": "RESEARCH_DISCOVERY_ASSISTANT",
    "CertificateDraft": "RESEARCH_DISCOVERY_ASSISTANT",
    "StructuralQuantity": "STRUCTURAL_QUANTITY",
    "MechanismProposal": "MECHANISM_DESIGNER",
    "ProofSketch": "PROOF_SKETCHER",
    "SoftAttackLog": "SOFT_ATTACK",
    "SoftFalsifierDraft": "SOFT_ATTACK",
    "RewriteProposal": "SOFT_ATTACK",
    "PortfolioFrontier": "PORTFOLIO_MANAGER",
    "PortfolioMember": "PORTFOLIO_MANAGER",
    "DraftCRP": "CRP_PACKAGER",
    "CompileError": "CRP_PACKAGER",
    "SealedCRPSnapshot": "RESEARCH_DISCOVERY_ASSISTANT",
}

CLASS_OWNER: MappingProxyType[str, str] = MappingProxyType(dict(_CLASS_OWNER_RAW))
del _CLASS_OWNER_RAW

CLOSE_REASONS = frozenset(
    {
        "completed_submitted",
        "completed_b_intake_rejected",
        "completed_mixed_outcomes",
        "completed_without_submission",
        "gate1_rejected",
        "gate2_rejected",
        "gate3_rejected",
        "no_viable_branch",
        "policy_directed_closure",
    }
)

DS91_REASONS = frozenset(
    {
        "store_init_failure",
        "corrupted_event_history",
        "unrecoverable_referential_integrity",
        "irrecoverable_illegal_forced_transition",
        "unrecoverable_transport",
    }
)
