"""Computational discharge for multi-threshold count preservation."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from operators.multi_threshold.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    adversarial_flip,
    multi_stable,
    multi_threshold_count,
    unstable_index,
)


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    detail: str
    counterexamples: tuple[dict[str, Any], ...] = ()
    limitations: tuple[str, ...] = (
        "COMPUTATIONAL_VERIFICATION_NOT_LEAN",
        "FINITE_THRESHOLD_LISTS_ONLY",
    )


def claim_is_multi_threshold_preservation(claim: dict[str, Any]) -> bool:
    return (
        claim.get("operator") == OPERATOR
        and claim.get("theorem_id") == THEOREM_ID
        and claim.get("evaluation") == EVALUATION_METHOD
    )


def _samples(x: float, eps: float) -> set[float]:
    if eps == 0:
        return {x}
    return {x - eps, x, x + eps, x - eps / 2, x + eps / 2}


def verify_multi_threshold_preservation(claim: dict[str, Any]) -> VerifyResult:
    if not claim_is_multi_threshold_preservation(claim):
        return VerifyResult(False, "claim_mismatch")
    if str(claim.get("statement", "")).strip() != THEOREM_STATEMENT.strip():
        return VerifyResult(False, "statement_mismatch")
    if str(claim.get("sharpness_statement", "")).strip() != SHARPNESS_STATEMENT.strip():
        return VerifyResult(False, "sharpness_statement_mismatch")

    rng = random.Random(20260725)
    failures: list[dict[str, Any]] = []

    # Empty list: always stable, count 0
    for eps in (0.0, 0.5, 2.0):
        if not multi_stable(0.0, (), eps):
            failures.append({"kind": "empty_not_stable", "eps": eps})
        if multi_threshold_count(0.0, ()) != 0:
            failures.append({"kind": "empty_count"})

    # Singleton reduces to thresholding
    for _ in range(200):
        x = rng.uniform(-5, 5)
        t = rng.uniform(-5, 5)
        eps = rng.uniform(0, 3)
        ts = (t,)
        c0 = multi_threshold_count(x, ts)
        if multi_stable(x, ts, eps):
            for xp in _samples(x, eps):
                if multi_threshold_count(xp, ts) != c0:
                    failures.append({"kind": "stable_break", "x": x, "T": ts, "eps": eps, "xp": xp})
                    break
            if adversarial_flip(x, ts, eps) is not None:
                failures.append({"kind": "stable_false_flip", "x": x, "T": ts, "eps": eps})
        else:
            if unstable_index(x, ts, eps) is None:
                failures.append({"kind": "unstable_flag", "x": x, "T": ts, "eps": eps})
            br = adversarial_flip(x, ts, eps)
            if br is None or multi_threshold_count(br, ts) == c0:
                failures.append({"kind": "sharp_fail", "x": x, "T": ts, "eps": eps, "br": br})

    # Multi-cut lists
    for _ in range(200):
        n = rng.randint(2, 5)
        ts = tuple(sorted(rng.uniform(-5, 5) for _ in range(n)))
        # allow duplicates occasionally
        if rng.random() < 0.2:
            ts = ts + (ts[0],)
        x = rng.uniform(-6, 6)
        eps = rng.uniform(0, 2.5)
        c0 = multi_threshold_count(x, ts)
        if multi_stable(x, ts, eps):
            for xp in _samples(x, eps):
                if multi_threshold_count(xp, ts) != c0:
                    failures.append({"kind": "multi_stable_break", "x": x, "T": ts, "eps": eps})
                    break
        else:
            br = adversarial_flip(x, ts, eps)
            if br is None or abs(br - x) > eps + 1e-9:
                failures.append({"kind": "multi_bad_flip", "x": x, "T": ts, "eps": eps, "br": br})
            elif multi_threshold_count(br, ts) == c0:
                failures.append({"kind": "multi_sharp_fail", "x": x, "T": ts, "eps": eps, "br": br})

    # Malformed inputs
    try:
        multi_threshold_count(float("nan"), (0.0,))
        failures.append({"kind": "nan_accepted"})
    except ValueError:
        pass
    try:
        multi_stable(0.0, (0.0,), -1.0)
        failures.append({"kind": "neg_eps_accepted"})
    except ValueError:
        pass

    if failures:
        return VerifyResult(False, f"failures:{len(failures)}", tuple(failures[:8]))
    return VerifyResult(True, "multi_threshold_preservation_ok")
