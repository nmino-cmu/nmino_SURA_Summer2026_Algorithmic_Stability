# Formal verification report

- operator: `top-k-then-threshold`
- theorem_id: `top-k-then-threshold-margin`
- candidate_digest: `93400aa4002b15cf37f9fb4ea708826b737d02ba1949fb21ba51302e3c6d32ca`
- bundle_digest: `1d0667a977a3e0885d166f6f57e643dc01937ce7574a86f48be1e42fd82bb44c`
- crp_digest: `d9f142c64ae84e38161aa700f58908e66e0e2cd2e55f60d0863a12ab53ed7142`
- verification_run_id: `280903fc-7780-42cb-ba79-924a4ce686d0`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Top-k-then-threshold uses this ranking core.)

## Lean propositions

- `top_k_then_threshold_margin_invariance` : `Research.Operators.TopKThenThreshold.Preservation.TopKThenThresholdMarginInvarianceProp`
- `top_k_then_threshold_margin_sharpness` : `Research.Operators.TopKThenThreshold.Preservation.TopKThenThresholdMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.top_k_then_threshold_margin.v1"
}
```

- conclusion_digest: `eaffb03f207383034436027594be77ec34ae900049b2adada38aa9fcb5f23ce0`
- semantic_freeze_digest: `fba2b42f436180038617a8cd4364e4d71407593b985008cf2cd94912fd41de71`
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
