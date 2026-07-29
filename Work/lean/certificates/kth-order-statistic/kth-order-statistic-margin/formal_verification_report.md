# Formal verification report

- operator: `kth-order-statistic`
- theorem_id: `kth-order-statistic-margin`
- candidate_digest: `bc6626e329d2f61ce9b9588a2eb7a53f4217f0e41e3864b3bc1c30022414dee0`
- bundle_digest: `8a38cc9793512d55260abe67cf198a9fb2e5af39a234224a05cb418a32e6c581`
- crp_digest: `4c2481af3968828824a625bec7f9b3944f1d1919924f6160e80d721e4a72f4dd`
- verification_run_id: `614be52a-7efc-4f1f-95b0-a352ca943eed`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, k∈ℕ with k<n, ε≥0, and i a unique strict k-th smallest index (exactly k scores strictly below s_i and no other index shares s_i). If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then i remains the unique strict k-th smallest of s+δ. (k-th order statistic selection uses this k-th order statistic core.)

## Lean propositions

- `kth_order_statistic_margin_invariance` : `Research.Operators.KthOrderStatistic.Preservation.KthOrderStatisticMarginInvarianceProp`
- `kth_order_statistic_margin_sharpness` : `Research.Operators.KthOrderStatistic.Preservation.KthOrderStatisticMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.kth_order_statistic_margin.v1"
}
```

- conclusion_digest: `684c04548fa878f83c9ffe9084dc0e53af837d6cbf598e83108d88e272de6b81`
- semantic_freeze_digest: `eac82fb7c94b5bfafb88fd8ccaf35ee06efa812dd2f088763c17c83e3b4ae343`
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
