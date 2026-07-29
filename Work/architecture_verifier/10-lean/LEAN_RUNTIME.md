# Lean Formalization Runtime (System 3)

**Artifact ID:** `ART-LEAN-RUNTIME`  
**Normative status:** `ACTIVE_IMPLEMENTATION`  
**Depends on:** ART-10b · ART-CRP · ART-INT-00

## Purpose

Executable Lean formalization path owned by System B. Implements ART-10b manifests via a **filesystem surrogate** until ART-06b Commit EventLog exists.

## Trust

- Statement authority: handwritten `def …Prop` regions between `STATEMENT_BEGIN/END` markers.
- Proof authority: Lean kernel (`lake build`) plus `#print axioms` capture.
- Status: `derived_lean_status(manifest, toolchain_head)` only — never a writable label. On-disk `status_recomputed.json` is informational; `verify_certificate` re-checks digests.
- LLM: optional Phase-5 proof-body splice only; **disabled by default** (raises if enabled).
- Domain: operator proofs are on **Mathlib ℝ** (`REAL_MATHLIB`), derived from each profile's `score_encoding`.

## Surrogate limitations

- `LEAN_MANIFEST_WITHOUT_COMMIT`
- `DEFINITION_PINS_SURROGATE` (operator `math.py` + prop file digests)

## Entry

```bash
cd implementation
PYTHONPATH=src .venv/bin/python -m system_b.lean.workflow path/to/bundle.json
```

Bundle export: `run_argmax_margin_workflow(export_lean_bundle=True)`.

`--skip-lake` is diagnostic only and **cannot** produce `LEAN_FULL`.

## Accepted certificates

Roster lives in `lean/certificates/` (one directory per operator/theorem) and is indexed by
`research-results/primitive-library/index.json`. Do not maintain a hand list here.
All accepted certificates are evidence-backed after workflow + axiom capture and recompute to
`REAL_MATHLIB` / `LEAN_FULL`; that includes both thresholding theorems.

## Layout

See repo `lean/` (Lake package `Research`) and `implementation/src/system_b/lean/`.
