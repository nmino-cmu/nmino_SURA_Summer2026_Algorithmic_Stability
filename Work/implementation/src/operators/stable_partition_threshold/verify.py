from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Any
from operators.stable_partition_threshold.math import (
    EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT,
)
from operators.top_k.math import adversarial_tie, ranking_preserved

@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = ("COMPUTATIONAL_VERIFICATION_NOT_LEAN",)

def claim_is_stable_partition_threshold_margin(claim):
    return claim.get("operator")==OPERATOR and claim.get("theorem_id")==THEOREM_ID and claim.get("evaluation")==EVALUATION_METHOD

def verify_stable_partition_threshold_margin(claim):
    if not claim_is_stable_partition_threshold_margin(claim): return VerifyResult(False,"claim_mismatch")
    if str(claim.get("statement","")).strip()!=THEOREM_STATEMENT.strip(): return VerifyResult(False,"statement_mismatch")
    if str(claim.get("sharpness_statement","")).strip()!=SHARPNESS_STATEMENT.strip(): return VerifyResult(False,"sharpness_mismatch")
    rng=random.Random(19); failures=[]
    for _ in range(250):
        n=rng.randint(2,7)
        scores=tuple(float(v) for v in sorted(rng.sample(range(-20,21), n)))
        gap=min(abs(scores[a]-scores[b]) for a in range(n) for b in range(a+1,n))
        if ranking_preserved(scores, max(0.0, gap/2-1e-9)) is False: failures.append({"kind":"inv"})
        br=adversarial_tie(scores,0,1,abs(scores[0]-scores[1])/2)
        if br is None: failures.append({"kind":"miss"}); continue
        news=tuple(scores[t]+br[t] for t in range(n))
        if len(set(news))==n: failures.append({"kind":"nocollide"})
    if failures: return VerifyResult(False,f"failures:{len(failures)}",tuple(failures[:8]))
    return VerifyResult(True,"ok")
