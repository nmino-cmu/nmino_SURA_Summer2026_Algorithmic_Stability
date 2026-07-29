# Algorithmic Stability for Optimization-Selected UQ

**Nicholas Mino · Wenbin Zhou · Shixiang Zhu**  
Carnegie Mellon University

## Start here

Read these two documents in order. The remaining repository can wait.

1. **[Problem Writeup](Formulation/writeup/Problem_Writeup.pdf)**  
   The research problem: Part I studies stability of optimization-based hyperparameter selection; Part II studies coverage after data-dependent selection of \(\theta\), while retaining the existing fixed-\(\theta\) uncertainty-set construction.

2. **[Primitive Library — Final Verdict](Work/research-results/primitive-library/FINAL-VERDICT.md)**  
   The verified deliverable: **50** completed operators and **53** theorem packages, all certified as `LEAN_FULL` over Mathlib’s \(\mathbb{R}\).

Afterward, optionally inspect:

- **[Example theorem paper](Work/research-results/median/median-margin/median_paper.pdf)** (median)
- **[Lean formalization](Work/lean/)** and its **[README](Work/lean/README.md)**

> **Skip on a first read:** `Work/architecture-discovery/`, `Work/architecture_verifier/`, `Work/architecture-integration/`, `Work/implementation/`, and `Work/docs/superpowers/`. These contain supporting infrastructure rather than the primary mathematical materials.

## Repository layout

| Path | Role |
|---|---|
| `Formulation/` | Problem formulation and archive |
| `Formulation/writeup/` | Authoritative project writeup |
| `Formulation/research/` | Working notes and experiments |
| `Formulation/context/` | Emails, transcripts, and reading materials |
| `Work/` | Lean certificates and theorem papers |
| `Work/research-results/` | Operator-level results |
| `Work/lean/` | Lean 4 formalization and certificates |

## Scope

The problem writeup states the proposed research program; the complete Part I–II theorem chain has not yet been Lean-certified.

The operator library certifies a finite collection of selection-stability primitives intended to support that program. It does not, by itself, establish the full Part I–II result.

## Optional verification

```bash
cd Work/lean
lake build

cd ..
python3 research-results/primitive-library/validation/validate_index.py
python3 research-results/primitive-library/validation/validate_metadata.py
```
