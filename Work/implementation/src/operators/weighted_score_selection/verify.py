from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Any
from operators.weighted_score_selection.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.argmax.math import adversarial_break, invariance_holds

@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

def claim_is_weighted_score_selection_margin(claim):
    return (
        claim.get("operator")==OPERATOR
        and claim.get("theorem_id")==THEOREM_ID
        and claim.get("evaluation")==EVALUATION_METHOD
    )

def verify_weighted_score_selection_margin(claim):
    if not claim_is_weighted_score_selection_margin(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_mismatch")
    rng = random.Random(19)
    failures = []
    for _ in range(250):
        m = rng.randint(2, 7)
        scores = tuple(float(v) for v in rng.sample(range(-20, 21), m))
        if len(set(scores)) < m:
            continue
        top = max(scores)
        if scores.count(top) != 1:
            continue
        gamma = top - max(v for v in scores if v != top)
        eps_ok = max(0.0, gamma / 2 - 1e-9)
        if invariance_holds(scores, eps_ok) is False:
            failures.append({"kind": "inv"})
        br = adversarial_break(scores, gamma / 2)
        if br is None:
            failures.append({"kind": "miss"})
            continue
        news = tuple(scores[t] + br[t] for t in range(m))
        if news.count(max(news)) == 1 and news.index(max(news)) == scores.index(top):
            failures.append({"kind": "nobreak"})
    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "ok")
