# Operator: argmax

## Operator

\[
\operatorname*{arg\,max}_{i \in [m]} s_i
\]

Finite deterministic scores \(s \in \mathbb{R}^m\) (\(m \ge 2\)). Indices are \(0..m-1\) in code (paper uses \([m]\)).

## Notation

| Symbol | Meaning |
|--------|---------|
| \(s\) | score vector |
| \(i^\star\) | unique maximizer when it exists |
| \(\gamma(s)\) | margin \(s_{i^\star} - \max_{j \ne i^\star} s_j\) |
| \(\varepsilon\) | perturbation budget |
| \(\delta\) | score perturbation with \(\|\delta\|_\infty \le \varepsilon\) |

## Primitive decomposition

1. Score map (here: abstract \(s\); data-dependent \(s_i(D)\) deferred).
2. Selection: unique maximizer or set-valued ties.
3. Instability: near-ties / ties under score noise.

## Instability

When \(\gamma(s)\) is small, an \(\ell_\infty\) ball of radius \(\varepsilon \ge \gamma(s)/2\) can force a tie or change the winner (sharp adversarial construction: \(-\varepsilon\) on \(i^\star\), \(+\varepsilon\) on a second-place index).

## Theorem (bounded perturbation margin)

**Assumptions.** Unique maximizer \(i^\star\); \(\gamma(s) > 0\); \(\|\delta\|_\infty \le \varepsilon\).

**Claim.** If \(\gamma(s) > 2\varepsilon\), then \(i^\star\) is the unique maximizer of \(s+\delta\).

**Sharpness.** If \(\gamma(s) \le 2\varepsilon\), some admissible \(\delta\) destroys uniqueness of \(i^\star\).

Treat statements as conjectures until Verification discharges them.

## Proof intuition

Worst-case: \(s_{i^\star}+\delta_{i^\star} \ge s_{i^\star}-\varepsilon\) and \(s_j+\delta_j \le s_j+\varepsilon\), so the gap shrinks by at most \(2\varepsilon\). Strict positivity of \(\gamma-2\varepsilon\) preserves uniqueness.

## Phase B: selection stability (charter hop)

Advances Area-1 chain packaging without new math:

\[
Q_\psi\ (\ell_\infty\ \text{score ball}) \to \operatorname{argmax} \to \texttt{selection\_stability}
\]

| Piece | Value |
|-------|-------|
| Profile | `PHASE_B_STABILIZATION` |
| `chain_segment` | `selection_stability` |
| Mechanism | `qpsi-linf-score-ball` (adversarial closed \(\ell_\infty\) ball; `KNOWN_MECHANISM`) |
| Theorem id / statement | Same as Phase A (`bounded-perturbation-margin`) so Lean profile still matches |
| Workflow | `run_argmax_selection_stability_workflow` |

Honest non-claims on the mechanism: not DP, not post-hoc inference, not policy validity. Stochastic \(Q_\psi\) (e.g. Laplace RNM) is a separate future cycle.

## Implementation

| Piece | Path |
|-------|------|
| Math | `implementation/src/operators/argmax/math.py` |
| Discovery IR | `…/discovery.py` (Phase A); `…/phase_b.py` (Phase B) |
| Verifier | `…/verify.py` (+ hook in `system_b/engines.py`) |
| E2E | `…/workflow.py` |
| Tests | `implementation/tests/test_argmax_operator.py`, `test_argmax_phase_b.py` |

## Verification status

- Method: `ARGMAX_MARGIN_COMPUTATIONAL_V1` (algebraic fixtures + adversarial sharpness + randomized property trials).
- **Computational** discharge remains primary System 2 evidence (`COMPUTATIONAL_VERIFICATION_NOT_LEAN`).
- **Lean (System 3):** `Research.Operators.Argmax.Margin` — `MarginInvarianceProp` / `MarginSharpnessProp` with handwritten proofs; certificate under `lean/certificates/argmax/bounded-perturbation-margin/` (`LEAN_FULL` when recomputed). Score encoding in Lean is Mathlib `ℝ` (`REAL_MATHLIB`). Phase B reuses this certificate under `selection_stability` packaging.

## Limitations

- Finite score vectors only; no data-dependent \(s_i(D)\) yet.
- \(\ell_\infty\) perturbation model only (deterministic adversarial ball; not Laplace / DP).
- Ties excluded from the invariance hypothesis (no unique \(i^\star\)).
- Computational certification ≠ interactive theorem prover (separate Lean certificate).
- Phase B does not claim utility certificates, composition, selected-object binding, or post-hoc inference.
