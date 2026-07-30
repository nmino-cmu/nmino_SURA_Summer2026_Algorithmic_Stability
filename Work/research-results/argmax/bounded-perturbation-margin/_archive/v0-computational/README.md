# Bounded perturbation margin for argmax

## What this proves

If scores \(s\in\mathbb{R}^m\) (\(m\ge 2\)) have a unique maximizer \(i^\star\) with
margin \(\gamma(s)>2\varepsilon\), then every perturbation with
\(\|\delta\|_\infty\le\varepsilon\) preserves \(i^\star\) as unique maximizer.
The bound is sharp.

## Where the proof lives

- Mathematical write-up: `paper.tex` / `paper.pdf`
- Outline: `proof-outline.md`
- Executable math + discharger: `implementation/src/operators/argmax/`

## Implementation that produced it

Discovery IR → sealed CRP → System B `ARGMAX_MARGIN_COMPUTATIONAL_V1`
(`operators.argmax.workflow.run_argmax_margin_workflow`).

## How to regenerate

```bash
cd research-results/argmax/bounded-perturbation-margin
pdflatex paper.tex
pdflatex paper.tex
```

## Limitations / verification status

- **Computational certification** via `ARGMAX_MARGIN_COMPUTATIONAL_V1`.
- **Lean formalization:** `lean/Research/Operators/Argmax/Margin.lean` with ART-10b surrogate certificate (`LEAN_FULL` on `Int` ordered-group core; `MATHLIB_REAL_PENDING`).
- Feedback limitations still include `COMPUTATIONAL_VERIFICATION_NOT_LEAN` as the System 2 evidence kind; Lean evidence is via `lean_manifest_digest`.
- Independent audits (math + implementation): PASS WITH MINOR ITEMS (B0/M0) on `feature/argmax`.
