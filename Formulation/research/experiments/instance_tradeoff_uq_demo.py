#!/usr/bin/env python3
"""Self-check: tradeoff-UQ instance — hard θ̂ non-degenerate; ĝ concentrates.

Instance (research/formal/instance_tradeoff_uq.tex):
  min_θ  f̂(θ)=θ  s.t.  ĝ(θ)=empirical_miscoverage(θ)-α0 ≤ 0
  ⇒ θ̂ = empirical (1-α0)-quantile of scores (varies with D).

Asserts:
  1) Hard θ̂ takes multiple distinct values across datasets (not always 1).
  2) Monte Carlo: P(‖ĝ-g*‖_∞ ≤ ε(n,ν)) ≳ 1-ν  (DKW Ass. conc on ĝ).

ponytail: Uniform scores; upgrade = real conformal scores on data.
Ceiling: θ̂ selection only; does not touch C's fixed-θ map.
"""
from __future__ import annotations

import math
import random


def eps_dkw(n: int, nu: float) -> float:
    return math.sqrt(math.log(2.0 / nu) / (2.0 * n))


def empiric_quantile(scores: list[float], alpha0: float) -> float:
    """θ̂ = s_{(k)}, k=ceil(n(1-α0)) — leftmost feasible under (2_trade)."""
    n = len(scores)
    k = max(1, min(n, math.ceil(n * (1.0 - alpha0))))
    return sorted(scores)[k - 1]


def ghat_sup_dev(scores: list[float], alpha0: float, grid: list[float]) -> float:
    """‖ĝ-g*‖_∞ on grid; Uniform ⇒ F(θ)=θ, g*=(1-θ)-α0."""
    n = len(scores)
    sorted_s = sorted(scores)

    def ghat_minus_gstar(theta: float) -> float:
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if sorted_s[mid] <= theta:
                lo = mid + 1
            else:
                hi = mid
        ghat = (1.0 - lo / n) - alpha0
        gstar = (1.0 - theta) - alpha0
        return abs(ghat - gstar)

    return max(ghat_minus_gstar(t) for t in grid)


def self_check() -> None:
    n = 400
    alpha0 = 0.10
    nu = 0.10
    eps = eps_dkw(n, nu)
    grid = [i / 500.0 for i in range(501)]
    n_trials = 400
    rng = random.Random(0)

    # (1) Hard θ̂ varies with data — not degenerate at 1
    thetas: list[float] = []
    for _ in range(n_trials):
        scores = [rng.random() for _ in range(n)]
        thetas.append(empiric_quantile(scores, alpha0))

    # Population quantile for Uniform: 1-α0 = 0.9
    mean_th = sum(thetas) / len(thetas)
    # Round to 3 decimals to count distinct realizations
    distinct = {round(t, 3) for t in thetas}
    assert max(thetas) < 0.999, (max(thetas), "degenerate-at-1?")
    assert min(thetas) > 0.01, min(thetas)
    assert abs(mean_th - (1.0 - alpha0)) < 0.05, mean_th
    assert len(distinct) >= 10, (len(distinct), "θ̂ did not vary enough")

    # (2) DKW good-event frequency for ĝ
    n_good = 0
    for _ in range(n_trials):
        scores = [rng.random() for _ in range(n)]
        if ghat_sup_dev(scores, alpha0, grid) <= eps:
            n_good += 1
    rate = n_good / n_trials
    assert rate >= 1.0 - 2.0 * nu, (rate, 1.0 - nu, eps)
    assert rate >= 0.85, rate

    print(
        "instance_tradeoff_uq_demo: OK",
        {
            "n": n,
            "alpha0": alpha0,
            "nu": nu,
            "eps": round(eps, 4),
            "theta_mean": round(mean_th, 4),
            "theta_min": round(min(thetas), 4),
            "theta_max": round(max(thetas), 4),
            "n_distinct_theta": len(distinct),
            "g_good_rate": round(rate, 3),
        },
    )


if __name__ == "__main__":
    self_check()
