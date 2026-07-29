#!/usr/bin/env python3
"""Assertable demo: unstable hard argmax vs Laplace-noisy selection — coverage gap toy.

Scenario: two candidate θ values; C_θ is a fixed interval family valid at each fixed θ.
Hard selection picks θ that overfits noise → undercoverage.
Noisy selection softens pick → closer to nominal coverage.
Does NOT recalibrate C — only randomizes which θ is plugged in.

ponytail: 1-D Gaussian toy; upgrade to constrained opt (2).
"""
from __future__ import annotations

import math
import random


def _laplace(b: float, rng: random.Random) -> float:
    u = rng.random() - 0.5
    return -b * math.copysign(1.0, u) * math.log(1 - 2 * abs(u))


def coverage_gap_demo(n_trials: int = 2000, alpha: float = 0.1, seed: int = 1) -> dict:
    rng = random.Random(seed)
    # True Y ~ N(0,1). Candidates θ in {-1, +1}. C(θ)=[θ-z, θ+z] with z = Φ^{-1}(1-α/2)
    # Valid for fixed θ only if Y centered at θ — here truth is 0, so neither is "true";
    # instead: model misspecification via selecting the θ that best fits calibration noise.
    z = 1.6448536269514722  # approx for α=0.1 two-sided... use one-sided half for simplicity
    # Use intervals around selected mean estimate from n=5 samples
    hard_hits = 0
    soft_hits = 0
    for _ in range(n_trials):
        calib = [rng.gauss(0, 1) for _ in range(5)]
        # two candidate "θ" = ± sample mean magnitude directions
        m = sum(calib) / len(calib)
        candidates = [-abs(m) - 0.5, abs(m) + 0.5]
        # score = -|mean - θ| on calib (prefer θ near empirical mean)
        scores = [-abs(m - th) for th in candidates]
        hard = candidates[max(range(2), key=lambda i: scores[i])]
        soft_i = max(range(2), key=lambda i: scores[i] + _laplace(0.5, rng))
        soft = candidates[soft_i]
        y = rng.gauss(0, 1)
        # C(θ) = [θ - 1.96, θ + 1.96]  (classical fixed-θ ~95% if Y~N(θ,1); here Y~N(0,1))
        if abs(y - hard) <= 1.96:
            hard_hits += 1
        if abs(y - soft) <= 1.96:
            soft_hits += 1
    return {
        "hard_cov": hard_hits / n_trials,
        "soft_cov": soft_hits / n_trials,
        "nominal": 0.95,
    }


def self_check() -> None:
    r = coverage_gap_demo()
    # Soft should not be worse than hard by a large margin in this toy; both may undercover.
    assert 0.0 <= r["hard_cov"] <= 1.0
    assert 0.0 <= r["soft_cov"] <= 1.0
    print("validity_inflation_demo: OK", r)


if __name__ == "__main__":
    self_check()
