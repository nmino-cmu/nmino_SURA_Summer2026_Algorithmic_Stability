# Formal verification report

- operator: `multi-criteria-lexicographic`
- theorem_id: `multi-criteria-lexicographic-margin`
- candidate_digest: `2337d6bb54d3f9cc37cdec680475e4ebec8a540b6d545b3eb4606a13ff876d5f`
- bundle_digest: `2b970d6a8a9fcc2457ca29ba6875d21d412038ca535d7d9308d69b6ad48d19fc`
- crp_digest: `beb2b40670024c71c8dab53dbf64db1cb422bee3ec71cae7a52cacae6df6a2d3`
- verification_run_id: `b0ae4f8b-72c7-45c3-af45-a278c93ec567`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Multi-criteria lexicographic uses this ranking core.)

## Lean propositions

- `multi_criteria_lexicographic_margin_invariance` : `Research.Operators.MultiCriteriaLexicographic.Preservation.MultiCriteriaLexicographicMarginInvarianceProp`
- `multi_criteria_lexicographic_margin_sharpness` : `Research.Operators.MultiCriteriaLexicographic.Preservation.MultiCriteriaLexicographicMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.multi_criteria_lexicographic_margin.v1"
}
```

- conclusion_digest: `bcf11694b9e9234e00e56b70bfde9c57b40fb883b96d35f5cb732710b2dbfb97`
- semantic_freeze_digest: `9738f9226b1ea8b689d1336ef1f3bca3050e921e6bf88d052122670c3c2c4157`
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
