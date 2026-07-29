# Formal verification report

- operator: `threshold-then-top-k`
- theorem_id: `threshold-then-top-k-margin`
- candidate_digest: `e60d90a14830494dfc0f8cfe224e3012116d794ffce44da9ce73eeab665d55bb`
- bundle_digest: `7c976342ba3aecbd7949a7333f32042366aa6e65f4b18a206760e9a053790179`
- crp_digest: `6acc85c314cf27e8c3bb7e1452f61c4c688d16367d3996b923500d45a73406f6`
- verification_run_id: `40a4f826-ef50-40d4-ab1f-87c17ada8706`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Threshold-then-top-k uses this ranking core.)

## Lean propositions

- `threshold_then_top_k_margin_invariance` : `Research.Operators.ThresholdThenTopK.Preservation.ThresholdThenTopKMarginInvarianceProp`
- `threshold_then_top_k_margin_sharpness` : `Research.Operators.ThresholdThenTopK.Preservation.ThresholdThenTopKMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.threshold_then_top_k_margin.v1"
}
```

- conclusion_digest: `87e70a7a46968a95a324cc794af132048af0ce950a07dbac127a17d4edcfeabc`
- semantic_freeze_digest: `526eddf266c6c3fa673018976e8d9e644a6830a605f61af6a37329b82b282d47`
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
