# Formal verification report

- operator: `quantile`
- theorem_id: `quantile-margin`
- candidate_digest: `ecd65131b7ec7748a05f0c51e4d5ee546c4552b3c4fecd179a9501ec89dbdf7a`
- bundle_digest: `bfa95570c2792c7c42d0f82a38f82fffadad6d9a9b130646826bc5ffb5f0661d`
- crp_digest: `d0b8f58eb00cb8b0da420583b242486137725a06efc2d4a3791f68a5dbb471e0`
- verification_run_id: `564c7e26-6dad-4a63-9bbe-05f51b1cdde3`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, k∈ℕ with k<n, ε≥0, and i a unique strict k-th smallest index (exactly k scores strictly below s_i and no other index shares s_i). If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then i remains the unique strict k-th smallest of s+δ. (Quantile selection uses this k-th order statistic core.)

## Lean propositions

- `quantile_margin_invariance` : `Research.Operators.Quantile.Preservation.QuantileMarginInvarianceProp`
- `quantile_margin_sharpness` : `Research.Operators.Quantile.Preservation.QuantileMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.quantile_margin.v1"
}
```

- conclusion_digest: `722ea21dcc0f15bf1067f302ffefaaec6f31e93160494654ab14741c1df1e92b`
- semantic_freeze_digest: `b2cc50ae19dd3f70993c8b6dd61364a307ae8b62ffd24ff217ce54f8339ec446`
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
