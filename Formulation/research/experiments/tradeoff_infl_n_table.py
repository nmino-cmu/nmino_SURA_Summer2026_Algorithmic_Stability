#!/usr/bin/env python3
"""End-to-end Infl(n) on (2_trade): ε→η→bound, plus MC soft selection.

Theory (W5, fixed C^(α)): Infl ≤ (e^η-1)α + ν.
Design: soft-argmin β=η/(2ε) on grid of θ with f̂=θ, feasibility via ĝ≤ε slack
(proxy for noisy feasible selection; ponytail: upgrade = exact RNM on discrete Θ).

Asserts: theoretical bound ↓ in n; MC soft miscoverage ≤ α + bound + slack.
"""
from __future__ import annotations

import math
import random


def eps_dkw(n: int, nu: float) -> float:
    return math.sqrt(math.log(2.0 / nu) / (2.0 * n))


def infl_bound(eta: float, alpha: float, nu: float) -> float:
    return (math.exp(eta) - 1.0) * alpha + nu


def soft_theta(scores: list[float], alpha0: float, eta: float, eps: float, rng: random.Random) -> float:
    """Soft-argmin of f̂=θ over conservative feasible grid (ĝ(θ)≤ -eps)."""
    n = len(scores)
    sorted_s = sorted(scores)
    beta = eta / (2.0 * eps) if eps > 0 else 1e9
    grid = [i / 200.0 for i in range(201)]
    feas = []
    for th in grid:
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if sorted_s[mid] <= th:
                lo = mid + 1
            else:
                hi = mid
        misc = 1.0 - lo / n
        # Θ₀^ε = {ĝ ≤ -eps} ⊆ {g* ≤ 0} on DKW good event
        if misc - alpha0 <= -eps:
            feas.append(th)
    if not feas:
        # fallback: leftmost empirically feasible (may exit valid domain)
        for th in grid:
            lo, hi = 0, n
            while lo < hi:
                mid = (lo + hi) // 2
                if sorted_s[mid] <= th:
                    lo = mid + 1
                else:
                    hi = mid
            if (1.0 - lo / n) - alpha0 <= 0:
                feas.append(th)
                break
        if not feas:
            feas = [1.0]
    best, best_s = feas[0], -1e300
    for th in feas:
        g = -math.log(-math.log(max(rng.random(), 1e-12)))
        sc = -beta * th + g
        if sc > best_s:
            best_s, best = sc, th
    return best


def row(n: int, alpha: float, nu: float, n_mc: int, rng: random.Random) -> dict:
    eps = eps_dkw(n, nu)
    # η→0 with ε so bound→ν then can send ν↓ separately; here η=ε
    eta = eps
    bound = infl_bound(eta, alpha, nu)
    # MC: Uniform scores ⇒ true misc at θ is 1-θ; target α=alpha0
    misc_sum = 0.0
    for _ in range(n_mc):
        scores = [rng.random() for _ in range(n)]
        th = soft_theta(scores, alpha, eta, eps, rng)
        misc_sum += 1.0 - th  # E[misc | θ̃] for Uniform
    misc = misc_sum / n_mc
    infl_hat = misc - alpha
    return {
        "n": n,
        "eps": round(eps, 4),
        "eta": round(eta, 4),
        "bound": round(bound, 4),
        "misc_mc": round(misc, 4),
        "infl_hat": round(infl_hat, 4),
    }


def self_check() -> None:
    alpha = 0.10
    nu = 0.05
    rng = random.Random(0)
    ns = [100, 400, 1600, 6400]
    rows = [row(n, alpha, nu, n_mc=200, rng=rng) for n in ns]

    # Bound must decrease in n under η=ε(n)
    for a, b in zip(rows, rows[1:]):
        assert b["bound"] < a["bound"], (a, b)

    # MC soft miscoverage within α + bound + 0.05 Monte Carlo slack
    for r in rows:
        assert r["misc_mc"] <= alpha + r["bound"] + 0.05, r

    # asymptotic: largest-n bound small-ish
    assert rows[-1]["bound"] < 0.15, rows[-1]

    print("tradeoff_infl_n_table: OK")
    print("n\teps\teta\tbound\tmisc_mc\tinfl_hat")
    for r in rows:
        print(f"{r['n']}\t{r['eps']}\t{r['eta']}\t{r['bound']}\t{r['misc_mc']}\t{r['infl_hat']}")


if __name__ == "__main__":
    self_check()
