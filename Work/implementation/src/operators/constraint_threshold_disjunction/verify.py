from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Any
from operators.constraint_threshold_disjunction.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.multi_threshold.math import adversarial_flip, multi_stable, multi_threshold_count

@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

def claim_is_constraint_threshold_disjunction_preservation(claim):
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )

def verify_constraint_threshold_disjunction_preservation(claim):
    if not claim_is_constraint_threshold_disjunction_preservation(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_mismatch")
    rng = random.Random(13)
    failures = []
    for _ in range(250):
        x = rng.uniform(-4, 4)
        Ts = tuple(sorted(rng.uniform(-3, 3) for _ in range(rng.randint(1, 4))))
        eps = rng.uniform(0, 1.5)
        c0 = multi_threshold_count(x, Ts)
        if multi_stable(x, Ts, eps):
            for xp in (x - eps, x, x + eps):
                if multi_threshold_count(xp, Ts) != c0:
                    failures.append({"kind": "count"})
        else:
            _ = adversarial_flip(x, Ts, eps)
    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "ok")
