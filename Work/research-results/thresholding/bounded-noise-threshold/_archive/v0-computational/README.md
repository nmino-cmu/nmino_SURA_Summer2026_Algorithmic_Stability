# Bounded almost-sure noise for scalar thresholding

## What this proves

Pathwise: \(\lvert\xi\rvert\le\eta\) a.s. implies the deterministic preservation
statement with \(\varepsilon:=\eta\) for \(\widetilde A_T(x)=\mathbf{1}\{x+\xi\ge T\}\).

## Explicitly not proved

Full Sparse Vector / DP accounting; adaptive positive-release bounds.

## Implementation

`THRESHOLD_BOUNDED_NOISE_COMPUTATIONAL_V1` via `run_bounded_noise_threshold_workflow`.

## Regenerate

```bash
cd research-results/thresholding/bounded-noise-threshold
pdflatex paper.tex && pdflatex paper.tex
```
