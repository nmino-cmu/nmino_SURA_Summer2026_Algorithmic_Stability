# Part I proof sketches

## Lemma loo-sc (strong convexity → LOO bound)
**Claim:** Under μ-strong convexity of f̂ in θ + stable active set, Δ_LOO ≤ (2/μ) L_LOO.

**Sketch:**
1. Write first-order optimality for θ̂(D) and θ̂(D^{(i)}).
2. Subtract; use strong convexity inner-product inequality.
3. Bound RHS by LOO change of gradients / constraints (L_LOO).
4. Gap: need explicit form of f̂,ĝ (OPEN — depends on specialization of (2)).

**Status:** STUB — waiting on lit pattern card + concrete (f̂,ĝ) instance.

## Lemma rand-loo (randomize selection → smaller LOO)
**Claim:** ∃ θ̃(D;ξ) with E[Δ_LOO(θ̃)] ≤ E[Δ_LOO(θ̂)] without touching C's fixed-θ map.

**Sketch:**
1. Import noise⇒stability pattern from Winner's Curse defense digest.
2. Apply noise to objective/constraints of (2), not to C scores.
3. Gap: choose structured vs isotropic noise (inverse-opt pattern card).

**Status:** STUB.
