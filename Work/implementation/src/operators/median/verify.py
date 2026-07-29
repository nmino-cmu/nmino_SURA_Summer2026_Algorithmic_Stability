from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Any
from operators.median.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
    adversarial_tie, invariance_holds, is_strict_kth,
)

@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

def claim_is_median_margin(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )

def verify_median_margin(claim: dict[str, Any]) -> VerifyResult:
    if not claim_is_median_margin(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_mismatch")
    rng = random.Random(17)
    failures: list[dict[str, Any]] = []
    for _ in range(300):
        n = rng.randint(2, 7)
        base = sorted(rng.sample(range(-20, 21), n))
        scores = tuple(float(v) for v in base)
        k = rng.randint(0, n - 1)
        order = sorted(range(n), key=lambda i: scores[i])
        i = order[k]
        assert is_strict_kth(scores, k, i)
        gap = min(abs(scores[a] - scores[b]) for a in range(n) for b in range(a + 1, n))
        eps_ok = gap / 2 - 1e-9
        if eps_ok >= 0 and not invariance_holds(scores, k, i, max(0.0, eps_ok)):
            failures.append({"kind": "invariance"})
        j = order[0] if k > 0 else order[1]
        eps = abs(scores[i] - scores[j]) / 2
        br = adversarial_tie(scores, i, j, eps)
        if br is None:
            failures.append({"kind": "missing_break"})
            continue
        news = tuple(scores[t] + br[t] for t in range(n))
        if is_strict_kth(news, k, i):
            failures.append({"kind": "break_failed"})
    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "ok")
