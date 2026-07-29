#!/usr/bin/env python3
"""Assertable demo: Laplace noise ⇒ (η,0,ν)-style density-ratio control on a score.

ponytail: toy 1-D score, not full constrained opt (2). Upgrade: noisy Frank-Wolfe on (2).
Ceiling: randomizes SELECTION score only; does not recalibrate an uncertainty set C.
"""
from __future__ import annotations

import math
import random


def laplace_stable_argmax(scores: list[float], eta: float, rng: random.Random) -> int:
    """Report-noisy-max with Laplace noise scale b = 2*sensitivity/eta (sensitivity=1 for ±1 scores)."""
    if eta <= 0:
        raise ValueError("eta must be > 0")
    b = 2.0 / eta  # sensitivity 1 for score in [0,1] differences of 1
    noisy = [s + rng.gauss(0, 0) + _laplace(b, rng) for s in scores]
    return max(range(len(scores)), key=lambda i: noisy[i])


def _laplace(b: float, rng: random.Random) -> float:
    u = rng.random() - 0.5
    return -b * math.copysign(1.0, u) * math.log(1 - 2 * abs(u))


def self_check() -> None:
    rng = random.Random(0)
    scores = [0.1, 0.9, 0.2]
    # With large eta (less noise), pick argmax=1 often
    picks = [laplace_stable_argmax(scores, eta=5.0, rng=rng) for _ in range(500)]
    frac_true = sum(p == 1 for p in picks) / len(picks)
    assert frac_true > 0.7, frac_true
    # With tiny eta (huge noise), selection is less concentrated
    rng = random.Random(0)
    picks2 = [laplace_stable_argmax(scores, eta=0.2, rng=rng) for _ in range(500)]
    frac2 = sum(p == 1 for p in picks2) / len(picks2)
    assert frac2 < frac_true, (frac2, frac_true)
    print("loo_stability_demo: OK", {"frac_eta5": frac_true, "frac_eta0.2": frac2})


if __name__ == "__main__":
    self_check()
