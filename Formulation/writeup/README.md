# Problem writeup

**Open:** [Problem_Writeup.pdf](Problem_Writeup.pdf) · source [Problem_Writeup.tex](Problem_Writeup.tex)

**Title:** Algorithmic Stability for Optimization-Selected Uncertainty Quantification  
**Authors:** Nicholas Mino, Wenbin Zhou, Shixiang Zhu (CMU)

## Contents

- **Part I** — How the constrained selection map changes when one calibration point is replaced, and what structure on objective/constraints controls that change.
- **Part II** — When coverage survives data-dependent hyperparameter selection; how far miscoverage can inflate; how to restore a guarantee by randomizing selection **without** recalibrating \(\mathcal{C}\).

Rebuild: `latexmk -pdf Problem_Writeup.tex`

## Related (not substitutes)

| Link | Role |
|------|------|
| [RESULTS.md](../research/RESULTS.md) | Working theorem-chain status (not frozen) |
| [mentor one-pager](../research/notes/2026-07-27_mentor_onepager.pdf) | One-page summary of the live chain |
| [Annotated PDF](../annotated_writeup/Problem_Writeup_Annotated.pdf) | Annotated draft; prefer this folder’s PDF |
| [FINAL-VERDICT.md](../../Work/research-results/primitive-library/FINAL-VERDICT.md) | Certified operator library — **next read** |
| [Package map](../../README.md) | Top-level entry |
