# Formal verification report

- operator: `beam-pruning`
- theorem_id: `beam-pruning-margin`
- candidate_digest: `f096a81630dd320c479cdac376fabbb6b3744f2e065b9b934c2e6062fc7752e0`
- bundle_digest: `bb976aa1116e8203f04cdea520bbdf1be8ee00a6a073d2a7d38de5d808df7aee`
- crp_digest: `a82baf42f1dde0203776b6ac50fb8021399a27f1c7570bc7d4e35feb4c77be23`
- verification_run_id: `9391b447-a97d-4608-b8ed-6861545deb6e`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let n≥2, s∈ℤ^n, ε≥0. If every pairwise gap exceeds 2ε and ‖δ‖_∞≤ε, then for all indices i,j: s_i < s_j iff (s+δ)_i < (s+δ)_j. (Beam pruning uses this ranking core.)

## Lean propositions

- `beam_pruning_margin_invariance` : `Research.Operators.BeamPruning.Preservation.BeamPruningMarginInvarianceProp`
- `beam_pruning_margin_sharpness` : `Research.Operators.BeamPruning.Preservation.BeamPruningMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.beam_pruning_margin.v1"
}
```

- conclusion_digest: `d3ea1da2d9c5171e7a869f0dee97e7f70d273c177939098f9f450a719e0d7249`
- semantic_freeze_digest: `3b8abef796b58e0f4511ef310e28614ca8426b9b91c7734580748eb3d6d719e0`
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
