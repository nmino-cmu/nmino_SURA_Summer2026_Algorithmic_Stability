# Formal verification report

- operator: `top-k`
- theorem_id: `top-k-margin`
- candidate_digest: `79e333b7d03b13c6c9c57f925db78f877a05b4d0cdbf8415cbbd4e31be3fc5ac`
- bundle_digest: `214e96016c99e46a53cc89cb7382a5130dc53dce20cca16a0e051f71ad2ec902`
- crp_digest: `c5cf208930ee4d26fa99a9340320e87aca11337e69b7952896bcd373ddc78a36`
- verification_run_id: `260bcc24-d284-4713-92b5-c975e2edadce`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Top-k selection uses this ranking core.)

## Lean propositions

- `top_k_margin_invariance` : `Research.Operators.TopK.Preservation.TopKMarginInvarianceProp`
- `top_k_margin_sharpness` : `Research.Operators.TopK.Preservation.TopKMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.top_k_margin.v1"
}
```

- conclusion_digest: `aa37c33cbd792878b34b892d1160561370bff04eded6563e449d137d6487c8d5`
- semantic_freeze_digest: `4c744a72f404c625ec83080be3877cf8cc586aee9bbc73da6399958c6ed565a0`
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
