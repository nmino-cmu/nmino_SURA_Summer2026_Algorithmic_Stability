#!/usr/bin/env python3
"""Self-check: set-valued stability transfer bound shape.

ponytail: discrete Θ toy with max-divergence e^η; not a full proof of Thm set-valued.
Asserts: empirical post-selection failure ≤ e^η * q + τ + ν (+ Monte Carlo slack).
"""
from __future__ import annotations

import math
import random


def self_check(n: int = 5000, eta: float = 0.2, seed: int = 0) -> None:
    rng = random.Random(seed)
    # Two θ values; oracle Q0 = Bern(0.5); on good event, K is e^η-tilted toward θ=1
    # Failure sets: θ=0 fails w.p. q0, θ=1 fails w.p. q1; take q = max
    q0, q1 = 0.05, 0.08
    q = max(q0, q1)
    e_eta = math.exp(eta)
    # Simulate: with prob 1-ν good event; on good event sample from tilted K
    nu, tau = 0.02, 0.01
    fails = 0
    for _ in range(n):
        good = rng.random() >= nu
        if not good:
            # worst case fail
            fails += 1
            continue
        # tilted toward θ=1: P(θ=1) = min(1, e^η * 0.5) roughly via rejection-style
        p1 = min(1.0, e_eta * 0.5)
        # renormalize simply: use p1' = p1 / (p1 + 0.5) * something — keep simple mixture
        theta = 1 if rng.random() < min(0.99, 0.5 * e_eta / (0.5 * e_eta + 0.5)) else 0
        fail_p = q1 if theta == 1 else q0
        # add tau mass as adversarial fail (upper bound ingredient)
        if rng.random() < tau:
            fails += 1
        elif rng.random() < fail_p:
            fails += 1
    emp = fails / n
    bound = e_eta * q + tau + nu
    assert emp <= bound + 0.05, (emp, bound)  # MC slack
    print("setvalued_transfer_demo: OK", {"emp": emp, "bound": bound, "q": q, "eta": eta})


if __name__ == "__main__":
    self_check()
