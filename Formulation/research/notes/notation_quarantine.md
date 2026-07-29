# Notation quarantine (do not rewrite writeup)

Frozen writeup quirks — preserve and flag:

1. **Third slot of C:** prose may say `C(X;D,α)` while (1) uses `C(X;D,θ)`. Live math follows (1): third argument is hyperparameter `θ`. Miscoverage level remains `α` in `1-α`.
2. **`f̂(y;θ)` vs `Y`:** lowercase `y` in (2) vs random `Y` in (1) unresolved in source. Formal files must state which convention they adopt locally without claiming Wenbin fixed it.
3. **Rule:** never silently “fix” frozen writeup. Any local convention → note here + in assumption ledger.

## Local conventions in `research/` (not writeup fixes)

4. **`C^{(α)}(X;D,θ)`:** Part II / mentor notes index the classical level by a superscript on `C` while keeping `θ` in the third slot. This is *not* Wenbin’s prose `C(…,α)`. Always keep arity `(X; D, θ)`; never drop `D`.
5. **`(2)` instances dropping `y`:** nested/tradeoff write `f̂(θ)` (no `y`). Local: `f̂` is an empirical functional of `D` only; do not claim writeup dropped `y`.
6. **`α` vs `α₀` (tradeoff):** `α` = classical miscoverage level in (1)/Infl; `α₀` = constraint threshold inside `ĝ` for `(2_trade)`. Demos may set `α₀=α`; that is a numerical choice, not an identification of the two roles.
7. **Ass.conc equality vs `(2_trade)`:** Ass.conc’s clause `Θ₀={g*≤0}` does *not* hold pathwise for data-dependent `ĝ`. Use Hausdorff weakening / conservative `Θ₀^ε` / fixed grid — do not claim equality is restored.

## Local aliases used in `research/formal` (mentor dictionary)

| Research symbol | Means in writeup language |
| --- | --- |
| `\mathcal{C}(X;\mathcal{D},\theta)` | Exact writeup (1) set |
| `C^{(q)}(X;D,\theta)` | **Alias only:** same construction as writeup `\mathcal{C}`, but with classical miscoverage level `q` instead of `α`. Third slot is still `θ`. Not a silent rename of α↔θ. |
| `\mathcal{C}_θ(x)` in instances | Score-threshold specialization `{y:s(x,y)≤θ}`; `D`-dependence enters via selection of `θ`, or via calib scores in `f̂,ĝ` |
| `\hat f(θ)` (instances) | Local drop of writeup’s `y` in `\hat f(y;θ)` — treat as empirical functional of `D` (see common_setup remark) |
| `α` | Classical miscoverage in (1) / Infl |
| `α₀` | Constraint level inside `(2_trade)` only; set `α₀=α` when feeding Part II unless stated |
| `D` vs `\mathcal{D}` | Same object; prefer `\mathcal{D}` in mentor-facing text |

## Correctness flags (Jul 27 audit)

8. **(FV) not for all θ∈[0,1] on score-threshold families:** `P(Y∉C_θ)=1-F(θ)`. Valid domain is `θ ≥ F^{-1}(1-α)`. Part II needs (OV) on `supp(A₀)`, not blanket sup over `[0,1]`.
9. **Ass.conc feasible equality:** pathwise `Θ₀={g*≤0}` is special case (box ĝ); tradeoff uses Hausdorff / `Θ₀^ε` bridge. Rate lemmas in `part_i_randomized_design` are still stated under the exact-match special case (or after `Θ₀^ε` restriction) — do not feed raw `Θ₀(D)={ĝ≤0}` into RNM/soft without that bridge.
