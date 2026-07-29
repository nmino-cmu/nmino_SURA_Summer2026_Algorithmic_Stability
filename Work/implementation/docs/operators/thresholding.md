# Operator: thresholding (AboveThreshold)

## Operator

\[
A_T(x)=\mathbf{1}\{x\ge T\}
\]

Scalar finite score \(x\in\mathbb{R}\), fixed threshold \(T\in\mathbb{R}\).
**Equality passes:** \(x=T\) yields output \(1\).

Sequential extension (implemented, privacy not claimed):

\[
\tau=\min\{t:q_t\ge T\}
\qquad
\widetilde\tau=\min\{t:q_t+\xi_t\ge T+\zeta\}.
\]

## Notation

| Symbol | Meaning |
|--------|---------|
| \(x\) | score |
| \(T\) | fixed threshold |
| \(m=x-T\) | signed margin |
| \(d=\lvert x-T\rvert\) | distance to threshold |
| \(\varepsilon\) | perturbation radius (\(\lvert x'-x\rvert\le\varepsilon\)) |
| \(\eta\) | a.s. noise bound for \(\lvert\xi\rvert\le\eta\) |

## Primitive decomposition

1. Score \(x\) (abstract; data map deferred).
2. Threshold retrieval (fixed \(T\)).
3. Comparison \(x\ge T\).
4. Boolean output \(\{0,1\}\).
5. Optional sequential stopping / positive-release counting (candidate levels).

## Decision boundary

Discontinuity at \(x=T\). Preservation uses asymmetric conditions because equality passes.

## Theorems

### Deterministic preservation (`threshold-output-preservation`)

If \(\lvert x'-x\rvert\le\varepsilon\):

1. \(x\ge T+\varepsilon\Rightarrow A_T(x')=1\)
2. \(x<T-\varepsilon\Rightarrow A_T(x')=0\)
3. \(x\in[T-\varepsilon,T+\varepsilon)\) need not be invariant

Sharpness respects the \(\ge\) convention: at \(x=T+\varepsilon\) pass is preserved; at \(x=T-\varepsilon\) fail is not.

### Bounded-noise threshold (`bounded-noise-threshold`)

Pathwise safe regions with \(\varepsilon:=\eta\) for \(\lvert\xi\rvert\le\eta\) a.s.
Part (3)/sharpness is **existential over noise laws**: the two-point law on
\(\{\pm\eta\}\) attains both outputs on \([T-\eta,T+\eta)\).

**Not claimed:** full Sparse Vector / DP accounting.

## Capability ladder status

| Level | Status |
|-------|--------|
| 1 scalar robustness | `VERIFIED_COMPUTATIONAL` |
| 2 noisy scalar (bounded) | `VERIFIED_COMPUTATIONAL_BOUNDED_NOISE` |
| 3 first crossing fixed queries | `IMPLEMENTED_NOT_PRIVACY_THEOREM` |
| 4 adaptive queries | `SPECIFIED_CANDIDATE` |
| 5 limited positive releases | `SPECIFIED_CANDIDATE` |
| 6 full Sparse Vector | `NOT_VERIFIED` |

## Abstention note

Certified abstention uses pass \(x\ge T+\tau\) and fail \(x<T-\tau\) (strict), matching
preservation asymmetry. The literature-style closed rule \(x\le T-\tau\) is **not**
used for certified release at the fail boundary.

## Implementation

| Piece | Path |
|-------|------|
| Math | `implementation/src/operators/thresholding/math.py` |
| Discovery IR | `…/discovery.py` |
| Verifier | `…/verify.py` (+ hook in `system_b/engines.py`) |
| E2E | `…/workflow.py` |
| Tests | `implementation/tests/test_thresholding_operator.py` |

## Verification status

- Methods: `THRESHOLD_PRESERVATION_COMPUTATIONAL_V1`, `THRESHOLD_BOUNDED_NOISE_COMPUTATIONAL_V1`
- **Not** Lean/ITP
- Limitations: `COMPUTATIONAL_VERIFICATION_NOT_LEAN`, `SCALAR_FINITE_SCORES_ONLY`, `BOUNDED_NOISE_NOT_FULL_SVT`

## Limitations

- Scalar finite scores; abstract \(x\), not full \(x(D)\) maps.
- Noisy DP/SVT theorems not verified.
- Bridge candidates recorded but not discharged.
