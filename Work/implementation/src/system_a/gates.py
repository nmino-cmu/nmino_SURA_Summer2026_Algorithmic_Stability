"""Gate helpers (ART-A-03 §4)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GateNumber(int, Enum):
    G1 = 1
    G2 = 2
    G3 = 3


class GateDecision(str, Enum):
    APPROVE = "approve"
    REVISE = "revise"
    REJECT = "reject"
    DEFER = "defer"
    WAIVE = "waive"
    SKIPPED = "skipped"


@dataclass
class GateRecord:
    gate_id: str
    gate_number: GateNumber
    decision: GateDecision
    seal_set: list[str] | None = None
    rationale: str = ""
