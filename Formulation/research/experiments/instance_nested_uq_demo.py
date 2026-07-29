#!/usr/bin/env python3
"""Self-check: nested-UQ instance — DKW ε(n,ν) holds; Infl shrinks as η↓.

Instance (research/formal/instance_nested_uq.tex):
  Θ=[0,1], θ = score threshold, C_θ = {y: s≤θ},
  f̂(θ)=empirical miscoverage=1-F̂_n(θ), ĝ = box (Θ₀=[0,1]).

Asserts:
  1) Monte Carlo: P(‖f̂-f*‖_∞ ≤ ε(n,ν)) ≳ 1-ν  (DKW Ass. conc).
  2) Optional: Infl_bound=(e^η-1)α+ν decreases as η↓.

ponytail: synthetic Uniform scores for DKW; upgrade = real conformal scores on data.
Ceiling: randomizes / concentrates SELECTION scores only; does not touch C's fixed-θ map.
"""
from __future__ import annotations

import math
import random


def eps_dkw(n: int, nu: float) -> float:
    """ε(n,ν) = √(log(2/ν)/(2n)) from Lemma dkw-conc."""
    return math.sqrt(math.log(2.0 / nu) / (2.0 * n))


def empiric_sup_dev(scores: list[float], grid: list[float]) -> float:
    """‖F̂-F‖_∞ proxy on a fine grid; F = Uniform[0,1] ⇒ F(θ)=θ."""
    n = len(scores)
    sorted_s = sorted(scores)
    # F̂(θ) = (# scores ≤ θ)/n; f̂=1-F̂, f*=1-θ ⇒ |f̂-f*|=|F̂-θ|
    def fhat_minus_fstar(theta: float) -> float:
        # binary count
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if sorted_s[mid] <= theta:
                lo = mid + 1
            else:
                hi = mid
        fhat = 1.0 - lo / n
        fstar = 1.0 - theta
        return abs(fhat - fstar)

    return max(fhat_minus_fstar(t) for t in grid)


def self_check() -> None:
    n = 400
    nu = 0.10
    eps = eps_dkw(n, nu)
    grid = [i / 500.0 for i in range(501)]
    n_trials = 400
    rng = random.Random(0)

    # (1) DKW good-event frequency
    n_good = 0
    for _ in range(n_trials):
        scores = [rng.random() for _ in range(n)]
        if empiric_sup_dev(scores, grid) <= eps:
            n_good += 1
    rate = n_good / n_trials
    # Theory: ≥ 1-ν; allow MC slack below 1-ν but stay clearly above 1-2ν
    assert rate >= 1.0 - 2.0 * nu, (rate, 1.0 - nu, eps)
    assert rate >= 0.85, rate  # with ν=0.1, expect ~≥0.9

    # (2) Infl upper bound shrinks as η↓ (Part II shape; fixed α,ν)
    alpha = 0.10
    eta_hi, eta_lo = 1.0, 0.05

    def infl(eta: float) -> float:
        return (math.exp(eta) - 1.0) * alpha + nu

    assert infl(eta_lo) < infl(eta_hi) - 0.05, (infl(eta_lo), infl(eta_hi))
    assert infl(eta_lo) < nu + 0.02  # η→0 ⇒ Infl → ν

    print(
        "instance_nested_uq_demo: OK",
        {
            "n": n,
            "nu": nu,
            "eps": round(eps, 4),
            "good_rate": round(rate, 3),
            "infl_eta_hi": round(infl(eta_hi), 4),
            "infl_eta_lo": round(infl(eta_lo), 4),
        },
    )


if __name__ == "__main__":
    self_check()
