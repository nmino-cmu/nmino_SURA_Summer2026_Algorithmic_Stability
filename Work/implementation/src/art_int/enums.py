"""Shared enums (ART-INT status-map / ART-CRP)."""

from __future__ import annotations

from enum import Enum


class AuthorKind(str, Enum):
    HUMAN = "HUMAN"
    RESEARCH_DISCOVERY_ASSISTANT = "RESEARCH_DISCOVERY_ASSISTANT"


class CrpProfile(str, Enum):
    PHASE_A_CHARACTERIZATION = "PHASE_A_CHARACTERIZATION"
    PHASE_B_STABILIZATION = "PHASE_B_STABILIZATION"
    MIXED = "MIXED"
    OBLIGATION_ONLY = "OBLIGATION_ONLY"
    BRIDGE_ONLY = "BRIDGE_ONLY"


class IntakeStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED_DRAFT = "ACCEPTED_DRAFT"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


class TransportResult(str, Enum):
    OK = "OK"
    FAILED = "FAILED"
    EXHAUSTED = "EXHAUSTED"


class AuditVerdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    IRRELEVANT = "IRRELEVANT"
    ESCALATE_HUMAN = "ESCALATE_HUMAN"
    NONE = "NONE"


class BatchStatus(str, Enum):
    OPEN = "OPEN"
    COMPLETED_ALL_ACCEPTED = "COMPLETED_ALL_ACCEPTED"
    COMPLETED_MIXED = "COMPLETED_MIXED"
    COMPLETED_ALL_REJECTED = "COMPLETED_ALL_REJECTED"
    ABORTED = "ABORTED"


class ObligationStatus(str, Enum):
    OPEN = "OPEN"
    DISCHARGED = "DISCHARGED"
    WAIVED_HUMAN = "WAIVED_HUMAN"
    FAILED = "FAILED"
    SUPERSEDED = "SUPERSEDED"


# Chain segments admitted by ART-07b (subset used on wire)
CHAIN_SEGMENTS = frozenset(
    {
        "data_regime",
        "score_construction",
        "perturbation_law",
        "selection_application",
        "selection_stability",
        "perturbation",
        "composition",
        "selected_object",
        "bridge",
        "inference",
        "characterization",
    }
)
