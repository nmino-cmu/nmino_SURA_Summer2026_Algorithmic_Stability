# Formal verification report

- operator: `rank`
- theorem_id: `rank-margin`
- candidate_digest: `16e05ae8724342ac19ae05ab293eddd2836a228c05e38d2bd770255cc25497dd`
- bundle_digest: `c05cabac8760afb3c8a3a36b10c669a791a9bf6f2bcf649f4745141f6a3fd3f6`
- crp_digest: `ea9c1c48dfd2e16792ffd17e7d7580efaf60b44d753731776e580a12c52b4ec3`
- verification_run_id: `355ea53f-fd93-41b3-84da-b814569fa7e9`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Rank uses this ranking core.)

## Lean propositions

- `rank_margin_invariance` : `Research.Operators.Rank.Preservation.RankMarginInvarianceProp`
- `rank_margin_sharpness` : `Research.Operators.Rank.Preservation.RankMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.rank_margin.v1"
}
```

- conclusion_digest: `b1abb70e15a124269ef95c82557866fd34bf7742716c07e2e0333e9235c34f2f`
- semantic_freeze_digest: `b58c13feca53774bc772e6c9f3a120543f3172c57d5ad93b7d791bc6bf26687d`
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
