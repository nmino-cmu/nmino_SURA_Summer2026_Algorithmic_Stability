# Formal verification report

- operator: `sorting`
- theorem_id: `sorting-margin`
- candidate_digest: `174f6fbbad8823b6af65d17d0b7e37c8f358dc8266f69e236e29a81a1b14b39d`
- bundle_digest: `b3b06744d58e21481e79fd5524bf51e17116bd1dc7839416ee58347be99ac072`
- crp_digest: `63faa33df49f5dabe07b474da5a12c7dad8552a2f3699bcb7086eb74c80da3bb`
- verification_run_id: `20cd1b16-53a7-4c47-a00f-d93a397460f7`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Sorting uses this ranking core.)

## Lean propositions

- `sorting_margin_invariance` : `Research.Operators.Sorting.Preservation.SortingMarginInvarianceProp`
- `sorting_margin_sharpness` : `Research.Operators.Sorting.Preservation.SortingMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.sorting_margin.v1"
}
```

- conclusion_digest: `9be965b55070b42fc2ca63c19e8abb656c1bd3506843edaa8960747564060b47`
- semantic_freeze_digest: `35df2a5f85b050b9c57438a48a616e6d9ed34f7c14979ab4503973f69bcbdb38`
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
