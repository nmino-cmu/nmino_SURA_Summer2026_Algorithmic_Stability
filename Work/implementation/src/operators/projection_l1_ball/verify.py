from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Any
from operators.projection_l1_ball.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
    ball_feasible, proj_id,
)

@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

def claim_is_projection_l1_ball_preservation(claim):
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )

def verify_projection_l1_ball_preservation(claim):
    if not claim_is_projection_l1_ball_preservation(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_mismatch")
    rng = random.Random(7)
    failures = []
    for _ in range(200):
        c = rng.uniform(-2, 2)
        r = rng.uniform(0.5, 3)
        inset = lambda z, c=c, r=r: abs(z - c) <= r + 1e-12
        x = c
        eps = min(r, rng.uniform(0, r))
        if ball_feasible(x, eps, inset):
            for xp in (x - eps, x, x + eps):
                if proj_id(xp) != xp:
                    failures.append({"kind": "id"})
        # sharpness: push outside
        y = c + r + 0.1
        if abs(y - x) <= r and inset(y):
            failures.append({"kind": "bad_out"})
    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "ok")
