# Formal verification report

- operator: `bucket-assignment`
- theorem_id: `bucket-assignment-margin`
- candidate_digest: `dd2bb66e2842db02a8cb74c3f98bdc5fae7c018b9f2dee2ede2ffa2e0393d69b`
- bundle_digest: `a6b5f486cc4d8e63568ad7e5b1a901ec3530d1a3c52747917b9a0a2892365b28`
- crp_digest: `90acd5902f0e660a4ab8fa393b7efebebe6d92027d5db2e48d4f24bd1b9526b0`
- verification_run_id: `3f3ec539-7b2c-4b52-9ead-e7d4d7a1f3cf`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Bucket assignment uses this ranking core.)

## Lean propositions

- `bucket_assignment_margin_invariance` : `Research.Operators.BucketAssignment.Preservation.BucketAssignmentMarginInvarianceProp`
- `bucket_assignment_margin_sharpness` : `Research.Operators.BucketAssignment.Preservation.BucketAssignmentMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.bucket_assignment_margin.v1"
}
```

- conclusion_digest: `5b36f8465954342f85c2bd42f8b3a41d087ea2f793cb32122efab0ad88e9342b`
- semantic_freeze_digest: `3f689044c0ab99027482bff74f4726ac2784b2ec345f53281250b3864f50aec6`
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
