# Math correctness judge

## Pass iff ALL hold

1. **Proof is complete** (research-paper quality): every case needed for the stated theorem is argued; not a sketch; not deferred to Lean.
2. Definitions of margin/gap/norm match the theorem’s use.
3. Sharpness adversary (if claimed) is explicit and admissible under the stated perturbation class.
4. No gaps, circular steps, or hidden assumptions beyond those listed.

## Fail examples

- “Similar to the core” without a full argument
- Missing uniqueness or count preservation step for order statistics
- Sharpness without constructing δ in the ball

## Output

`PASS` or `FAIL` with bullet reasons. No prose rewrite.
