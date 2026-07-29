# Formal verification report

- operator: `stable-partition-threshold`
- theorem_id: `stable-partition-threshold-margin`
- candidate_digest: `62f3d353424867704c67b4cf40705da07b0e9da4a6fa99173afb6e564e73d771`
- bundle_digest: `1d801b1a7677b454865ce225e86c395f77061b4ba690bbd94f89154d9a9d219a`
- crp_digest: `5933860d829f00252fffbfbd757a2f93ea6b79c0ec3da432bcc6f42cd9c53fca`
- verification_run_id: `c0de92cf-86b8-4a53-831b-3b794a82e8e4`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Stable partition by threshold uses this ranking core.)

## Lean propositions

- `stable_partition_threshold_margin_invariance` : `Research.Operators.StablePartitionThreshold.Preservation.StablePartitionThresholdMarginInvarianceProp`
- `stable_partition_threshold_margin_sharpness` : `Research.Operators.StablePartitionThreshold.Preservation.StablePartitionThresholdMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.stable_partition_threshold_margin.v1"
}
```

- conclusion_digest: `dec7b8d7a574304bd71b2784c0be4e74a3b6af1b578b1726e231f1f31997b247`
- semantic_freeze_digest: `d2f92b096bb5b45b6c1a24edbc08b8c01bafb9d1f78911b3a1e7c92088e0364d`
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
