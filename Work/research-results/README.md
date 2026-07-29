# Research results

Publication-quality write-ups **only after** System 3 reports `LEAN_FULL`
(see `.cursor/rules/research-results-publication.mdc`).

## Operator papers (operator-stability-v1)

Each live theorem package ships:

- `paper.tex` — classification (Primitive/Derived/Reduction) + 10 sections including a **complete** Proof
- `<operator>_paper.pdf` — published PDF (`-` → `_` in the operator id)
- `metadata.json` → `paper_card`
- Lean citation in **Formal statement**

```bash
python3 scripts/build_family_sections.py [<operator> <theorem>]
python3 scripts/generate_operator_paper.py <operator> <theorem> \
  --sections research-results/<operator>/<theorem>/sections.v1.json
python3 scripts/regenerate_all_operator_papers.py   # bulk
```

Prompts: `prompts/operator-paper/`. Template: `research-results/paper-templates/operator-stability-v1.tex`.

## Primitive Operator Library

[`primitive-library/`](primitive-library/). Do not hand-edit `primitive-library/index.json`.

## Current Lean-gated papers

See [`primitive-library/index.json`](primitive-library/index.json) and
[`primitive-library/FINAL-VERDICT.md`](primitive-library/FINAL-VERDICT.md).
Every accepted certificate is `LEAN_FULL` on Mathlib ℝ (`REAL_MATHLIB`).

`argmax/selection-stability-linf/` is Phase B packaging of `bounded-perturbation-margin`.

Computational-only drafts live under `_archive/v0-computational/` and are not publication-authoritative.
