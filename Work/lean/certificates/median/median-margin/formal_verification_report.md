# Formal verification report

- operator: `median`
- theorem_id: `median-margin`
- candidate_digest: `6de186a06bc3a3bc237ab9f16026dc9a29c4dca61cde1e5e39729719ab793aff`
- bundle_digest: `7d19007804a7c61d1b44c29197b897a384fa26f7dad2ab048ef8d54f5fca74ae`
- crp_digest: `a8c3edb44ec6d0a19a47e69ff15bf7dec6151aa55c1557103080aa2d890f405a`
- verification_run_id: `fbb73248-d86e-465b-87dc-cf7d6e337f7b`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, k∈ℕ with k<n, ε≥0, and i a unique strict k-th smallest index (exactly k scores strictly below s_i and no other index shares s_i). If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then i remains the unique strict k-th smallest of s+δ. (Median selection uses this k-th order statistic core.)

## Lean propositions

- `median_margin_invariance` : `Research.Operators.Median.Preservation.MedianMarginInvarianceProp`
- `median_margin_sharpness` : `Research.Operators.Median.Preservation.MedianMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.median_margin.v1"
}
```

- conclusion_digest: `d7b9bc6f44e6f789282de40edbe208cd2d68c642ad545977fdff63325444f676`
- semantic_freeze_digest: `338ee2a08b1bb9c546511f3cacdefe2df19e5a211f7a41d79be7931c6fbd43c4`
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
