from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Any
from operators.projection_interval.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
    clamp, nonexpansive,
)

@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

def claim_is_projection_interval_preservation(claim):
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )

def verify_projection_interval_preservation(claim):
    if not claim_is_projection_interval_preservation(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_mismatch")
    rng = random.Random(7)
    failures = []
    for _ in range(400):
        a, b = rng.uniform(-5, 5), rng.uniform(-5, 5)
        lo, hi = (a, b) if a <= b else (b, a)
        x, y = rng.uniform(-6, 6), rng.uniform(-6, 6)
        if not nonexpansive(x, y, lo, hi):
            failures.append({"kind": "lip"})
    # sharpness witness for eps=3
    if abs(clamp(3, 0, 3) - clamp(0, 0, 3)) != 3:
        failures.append({"kind": "sharp"})
    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "ok")
