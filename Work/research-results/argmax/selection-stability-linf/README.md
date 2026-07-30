# Argmax selection stability under ℓ∞ score ball (Phase B packaging)

## Charter hop

\[
Q_\psi\ (\ell_\infty\ \text{adversarial score ball})
\to
\operatorname{argmax}
\to
\texttt{selection\_stability}
\]

This advances Area-1 Phase B (`PHASE_B_STABILIZATION`) without inventing new mathematics.
The discharged theorem is the same Lean-certified margin statement as
[`../bounded-perturbation-margin/`](../bounded-perturbation-margin/).

## Mechanism \(Q_\psi\)

| Field | Value |
|-------|-------|
| `local_id` | `qpsi-linf-score-ball` |
| Family | additive score perturbation |
| Norm / law | \(\ell_\infty\) / adversarial closed ball of radius \(\varepsilon\) |
| Novelty ladder | `KNOWN_MECHANISM` |

**Non-claims:** not differential privacy; not post-hoc inference; not policy validity.
Stochastic mechanisms (e.g. Laplace RNM) are separate cycles.

## Runtime packaging

| Field | Value |
|-------|-------|
| Profile | `PHASE_B_STABILIZATION` |
| `chain_segment` | `selection_stability` |
| Theorem id | `bounded-perturbation-margin` (unchanged) |
| Workflow | `run_argmax_selection_stability_workflow` |
| Discovery | `implementation/src/operators/argmax/phase_b.py` |

## Lean verification (required for publication authority)

- Status: **`LEAN_FULL`** (same certificate as Phase A margin)
- Modules: `Research.Operators.Argmax.Margin`
- Certificate: `lean/certificates/argmax/bounded-perturbation-margin/`
- Domain: Mathlib Real (`REAL_MATHLIB`)

Publication text for the mathematics lives under
`research-results/argmax/bounded-perturbation-margin/`.
This directory records the Phase B packaging hop only.
