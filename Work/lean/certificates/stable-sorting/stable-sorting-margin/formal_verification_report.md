# Formal verification report

- operator: `stable-sorting`
- theorem_id: `stable-sorting-margin`
- candidate_digest: `bc82251279093e07e54164f72c8adfc0ae4abb50e75f1fba7c523bfa72716fe2`
- bundle_digest: `a91d275a1ebc6b9e2043c723c06d3254d0161bd4f94fd68f4f3b89eaa8c8d576`
- crp_digest: `96bdfe2f97469f70fe567b87bb4550906f1a204bc8c65c5b31092bb122a5e7ea`
- verification_run_id: `0a73fefc-045c-4b98-9450-75dd1a68853e`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Stable sorting uses this ranking core.)

## Lean propositions

- `stable_sorting_margin_invariance` : `Research.Operators.StableSorting.Preservation.StableSortingMarginInvarianceProp`
- `stable_sorting_margin_sharpness` : `Research.Operators.StableSorting.Preservation.StableSortingMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.stable_sorting_margin.v1"
}
```

- conclusion_digest: `8ad3b0251d4e64d297f1be6d9ece43a4835e040f61a8e34b31c403dd644d299c`
- semantic_freeze_digest: `46e122340aa06ff9a75b16ce079f2ed25823df9242344b2ee264670e606f7b12`
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
