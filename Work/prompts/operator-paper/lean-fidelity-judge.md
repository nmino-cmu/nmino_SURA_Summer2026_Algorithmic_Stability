# Lean fidelity judge

## Pass iff ALL hold

1. Theorem statement in the paper matches Lean `*Prop` hypotheses and conclusion (no strengthening).
2. Formal statement cites the correct `lean_entry_module`, theorem names from metadata, and certificate path.
3. Limitations / residual gaps named in the certificate (if any) are not contradicted by the prose.
4. Fundamentality label matches Lean structure (alias/`:=` → Reduction; core statement site → Primitive).

## Fail examples

- Claims full Euclidean projection when Lean is feasible-ball identity
- Omits sharpness hypothesis or invents DP from pathwise surrogate
- Wrong module path or theorem names

## Output

`PASS` or `FAIL` with bullet reasons. No prose rewrite.
