# Threshold output preservation

## What this proves

For \(A_T(x)=\mathbf{1}\{x\ge T\}\) and \(\lvert x'-x\rvert\le\varepsilon\):
pass is preserved when \(x\ge T+\varepsilon\); fail when \(x<T-\varepsilon\);
the band \([T-\varepsilon,T+\varepsilon)\) is unstable. Equality asymmetry is sharp.

## Where the proof lives

- `paper.tex` / `paper.pdf`
- `proof-outline.md`
- `implementation/src/operators/thresholding/`

## Implementation

Discovery → sealed CRP → System B `THRESHOLD_PRESERVATION_COMPUTATIONAL_V1`
(`run_threshold_preservation_workflow`).

## Regenerate

```bash
cd research-results/thresholding/threshold-output-preservation
pdflatex paper.tex && pdflatex paper.tex
```

## Limitations / status

Computational PASS (not Lean). Sparse Vector not claimed.
