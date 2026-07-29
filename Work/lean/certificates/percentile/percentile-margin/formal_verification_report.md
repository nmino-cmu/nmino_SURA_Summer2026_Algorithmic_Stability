# Formal verification report

- operator: `percentile`
- theorem_id: `percentile-margin`
- candidate_digest: `2eaf149c8babf749baa69085b7b258f565665e15f6fcd355292f783e0dd146a6`
- bundle_digest: `6cb6260af20a99c73dd46a6e495a9a4f53c30217cc138ba4647f09dd6cedfbfd`
- crp_digest: `a4c3e2858e13bfcbfd905ab55f9e5b25b28ead99f89da58f41f55bae7d8c97cc`
- verification_run_id: `311a9cd2-bb96-405a-acb2-342d99c56f9b`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, k∈ℕ with k<n, ε≥0, and i a unique strict k-th smallest index (exactly k scores strictly below s_i and no other index shares s_i). If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then i remains the unique strict k-th smallest of s+δ. (Percentile selection uses this k-th order statistic core.)

## Lean propositions

- `percentile_margin_invariance` : `Research.Operators.Percentile.Preservation.PercentileMarginInvarianceProp`
- `percentile_margin_sharpness` : `Research.Operators.Percentile.Preservation.PercentileMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.percentile_margin.v1"
}
```

- conclusion_digest: `a80cb730f8666ff5bb9d52447307dcd908731a074fc37486b7f3a04d9275c756`
- semantic_freeze_digest: `acbdd1f22b3051348dbe0b69993452f301e5bd64e950da4dfdba4ac4c8149ae6`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "DEFAULT",
  "extensionality": "DEFAULT",
  "finiteness": "FINITE_VECTOR",
  "measure_stage": "NONE",
  "score_encoding": "REAL_MATHLIB",
  "tie_break": "UNIQUE_REQUIRED"
}
```

## Build

- build_ok: `True`
- sorry_count: `0`
- admit_count: `0`
- lake_log_digest: `87a6ac2ad9231249eb100f5f4d8fba064c72d8c0db7eea0f4f30060be98c0d1a`
- axiom_closure_captured: `True`

## Axiom closure (`#print axioms`)

- `Classical.choice`
- `Quot.sound`
- `propext`

## Derived status (recomputed; not authoritative storage)

- `LEAN_FULL`

## Known gaps

- `DEFINITION_PINS_SURROGATE`

## Limitations of this certificate

- `LEAN_FULL` here means kernel-checked Mathlib `ℝ` propositions.
- Smoke theorems alone never authorize operator LEAN_FULL.
- PDF / markdown reports are derived views, not proof authority.

## Reuse

- `Research.Operators.Argmax.Basic` / `Margin` shared by argmax-family aliases.
