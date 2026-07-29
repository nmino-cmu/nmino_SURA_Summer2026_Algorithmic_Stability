# Bounded perturbation margin for argmax (Lean-gated)

## What this proves

If scores have a unique maximizer with margin \(\gamma>2\varepsilon\), every
\(\|\delta\|_\infty\le\varepsilon\) preserves that maximizer. The bound is sharp.

## Lean verification (required for publication)

- Status: **`LEAN_FULL`**
- Modules: `Research.Operators.Argmax.Margin` (`margin_invariance`, `margin_sharpness`)
- Certificate: `lean/certificates/argmax/bounded-perturbation-margin/`
- Domain: Mathlib Real (`REAL_MATHLIB`)

## How to regenerate

```bash
# 1) Confirm Lean
cd lean && lake build && python scripts/recompute_status.py
# 2) Only if status_recomputed.json shows LEAN_FULL:
cd ../research-results/argmax/bounded-perturbation-margin
pdflatex paper.tex && pdflatex paper.tex
```

## Archive

Computational-only v0 paper: `_archive/v0-computational/` (not publication-authoritative).
