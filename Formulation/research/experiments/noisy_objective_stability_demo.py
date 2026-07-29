#!/usr/bin/env python3
"""Self-check: noisy-objective (2_ξ) — more Laplace noise ⇒ less brittle selection.

Toy: finite Θ₀ = {0,...,m-1}, scores = f̂(θ) (lower better), constrained by membership in Θ₀.
Noisy objective ≡ report-noisy-min: argmin_θ (f̂(θ) - Lap(b)), b = 2ε/η.

Asserts:
  1) smaller η (larger b) ⇒ selection less concentrated on hard argmin (less brittle);
  2) on a synthetic good event |f̂-f*|≤ε, empirical max density-ratio ≲ e^η (RNM rate shape).

ponytail: discrete Θ toy for Lemma rnm; upgrade = polytope LMO / soft-argmin Gibbs.
Ceiling: randomizes SELECTION only; does not touch an uncertainty set C.
"""
from __future__ import annotations

import math
import random


def _laplace(b: float, rng: random.Random) -> float:
    u = rng.random() - 0.5
    return -b * math.copysign(1.0, u) * math.log(1.0 - 2.0 * abs(u))


def noisy_argmin(fhat: list[float], b: float, rng: random.Random) -> int:
    """(2_ξ) on finite Θ₀: argmin (f̂(θ) - ξ_θ), ξ~Lap(b)."""
    noisy = [fhat[i] - _laplace(b, rng) for i in range(len(fhat))]
    return min(range(len(fhat)), key=lambda i: noisy[i])


def selection_probs(fhat: list[float], b: float, n: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    m = len(fhat)
    counts = [0] * m
    for _ in range(n):
        counts[noisy_argmin(fhat, b, rng)] += 1
    return [c / n for c in counts]


def self_check() -> None:
    # Near-tie landscape: brittle hard argmin at θ=1, competitors close
    fhat = [0.22, 0.18, 0.25, 0.30]
    hard = min(range(len(fhat)), key=lambda i: fhat[i])
    assert hard == 1

    eta_hi, eta_lo = 2.0, 0.35  # hi η = less noise; lo η = more noise (goal iii: small η)
    eps = 0.08
    b_hi = 2.0 * eps / eta_hi
    b_lo = 2.0 * eps / eta_lo

    n = 6000
    p_hi = selection_probs(fhat, b_hi, n, seed=0)
    p_lo = selection_probs(fhat, b_lo, n, seed=1)

    # More noise ⇒ less mass on hard argmin
    assert p_lo[hard] < p_hi[hard] - 0.05, (p_lo[hard], p_hi[hard])

    # Collision proxy: sum p^2 smaller when flatter (less brittle)
    brittle_hi = sum(p * p for p in p_hi)
    brittle_lo = sum(p * p for p in p_lo)
    assert brittle_lo < brittle_hi, (brittle_lo, brittle_hi)

    # Density-ratio shape on good event: f* within ε of f̂ (Ass. conc)
    fstar = [fhat[i] + (eps if i != hard else -eps) for i in range(len(fhat))]
    assert max(abs(a - b) for a, b in zip(fhat, fstar)) <= eps + 1e-12

    q = selection_probs(fstar, b_hi, n, seed=2)
    # empirical max log-ratio on atoms with enough mass; rate ≤ η (+ MC slack)
    log_ratios = []
    for pi, qi in zip(p_hi, q):
        if min(pi, qi) > 5.0 / n:
            log_ratios.append(abs(math.log(pi / qi)))
    max_div = max(log_ratios) if log_ratios else 0.0
    assert max_div <= eta_hi + 0.85, (max_div, eta_hi)
    assert max_div > 0.02, max_div  # landscape actually moves the law

    print(
        "noisy_objective_stability_demo: OK",
        {
            "p_hard_eta_hi": round(p_hi[hard], 3),
            "p_hard_eta_lo": round(p_lo[hard], 3),
            "brittle_hi": round(brittle_hi, 3),
            "brittle_lo": round(brittle_lo, 3),
            "max_log_ratio": round(max_div, 3),
            "eta_hi": eta_hi,
        },
    )


if __name__ == "__main__":
    self_check()
