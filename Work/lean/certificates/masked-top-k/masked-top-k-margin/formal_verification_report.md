# Formal verification report

- operator: `masked-top-k`
- theorem_id: `masked-top-k-margin`
- candidate_digest: `27d5fe5fabd7af5e74d928d28833001dfff208ae6844af7f48174fca96d09b76`
- bundle_digest: `60f53a507eba7583fe0a310e8dfe3964be6e9da33fae79159871d5a3b5d8b0d0`
- crp_digest: `7e242c0fed4d7e24363b8ddebf2fd85d424aaafadeccf4b6bd0a5cbdf1117b49`
- verification_run_id: `47e7ba56-839a-482e-ac56-6a1eadc8e0c7`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Masked top-k uses this ranking core.)

## Lean propositions

- `masked_top_k_margin_invariance` : `Research.Operators.MaskedTopK.Preservation.MaskedTopKMarginInvarianceProp`
- `masked_top_k_margin_sharpness` : `Research.Operators.MaskedTopK.Preservation.MaskedTopKMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.masked_top_k_margin.v1"
}
```

- conclusion_digest: `a509a68c8d11205a878345389e8da5a6f29fbc6eb73e3c698984e13209e83bd3`
- semantic_freeze_digest: `40097bd6a8b4c7dd9ae7d58d13b4075ba9f071de5e4133b4256e8b6c3034ce7f`
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
