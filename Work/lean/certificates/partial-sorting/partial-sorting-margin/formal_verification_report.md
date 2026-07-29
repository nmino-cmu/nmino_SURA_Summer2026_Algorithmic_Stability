# Formal verification report

- operator: `partial-sorting`
- theorem_id: `partial-sorting-margin`
- candidate_digest: `05df0814c6bd745d568a4f248d162c26df9080bf205f192fbf70004c82c0aa30`
- bundle_digest: `d486f75a856a2b3a7465757447a3cc4969c0872bbce2602beee2a990dd78c8bb`
- crp_digest: `fd5bb982355d3d113bfafa87c3a308968440c7f319cc0607bb175273ea7466d8`
- verification_run_id: `2c621d7d-0c05-4b08-bb6e-493489bef275`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Partial sorting uses this ranking core.)

## Lean propositions

- `partial_sorting_margin_invariance` : `Research.Operators.PartialSorting.Preservation.PartialSortingMarginInvarianceProp`
- `partial_sorting_margin_sharpness` : `Research.Operators.PartialSorting.Preservation.PartialSortingMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.partial_sorting_margin.v1"
}
```

- conclusion_digest: `583690de43c47b45c36ee1c446fbf648ffeb7fce5e063ee4dcf18a93293ee5e8`
- semantic_freeze_digest: `2e37638901c8def03a2726e70f6b83921f75abc743313c23828c26c9a4b99581`
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
