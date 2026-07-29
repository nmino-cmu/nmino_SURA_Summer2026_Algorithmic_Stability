# Formal verification report

- operator: `lexicographic-ordering`
- theorem_id: `lexicographic-ordering-margin`
- candidate_digest: `45578e05561081d3f3b3a8718ad724655c83e4b9bbe6acb37fb9532a9f22d693`
- bundle_digest: `1ec04266805a32c8447e7a37d498f0428b2f7624c91467d214bbacbc299cfc45`
- crp_digest: `166a7ca9ecd9f45a5e90ebfe57ae94939b174fceaa699f69c5456f0610bd5029`
- verification_run_id: `2ecece70-a83e-4546-9d01-42a9148911f5`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Lexicographic ordering uses this ranking core.)

## Lean propositions

- `lexicographic_ordering_margin_invariance` : `Research.Operators.LexicographicOrdering.Preservation.LexicographicOrderingMarginInvarianceProp`
- `lexicographic_ordering_margin_sharpness` : `Research.Operators.LexicographicOrdering.Preservation.LexicographicOrderingMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.lexicographic_ordering_margin.v1"
}
```

- conclusion_digest: `fe85d48013dd85639d38f484e9b655a46e700d42497b25673ca12c248e71ae2c`
- semantic_freeze_digest: `1add0fd53811a910b8ba7916a997fd2d6a2c1b7b26b66649e00f92740298cdb4`
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
