# Formal verification report

- operator: `absolute-value-threshold`
- theorem_id: `abs-threshold-preservation`
- candidate_digest: `d2c43d13f6a417bb748df733d3332c6380e775043a83548ea99efa78942d81b4`
- bundle_digest: `8f6f20359ebf9c7a0bf2c426326a24f10c42f76f881562cbf653c18e8889d696`
- crp_digest: `734e09ac3e0e8746f71bd64f9d0d3a46f13272f9c67313752980d8f778a74de4`
- verification_run_id: `6224d465-d4a5-4f6a-9164-f2bbf796f850`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let x,x'∈ℝ, ε≥0 with |x'-x|≤ε, and T≥0. Define A(x)=1{|x|≥T}. (1) if |x|≥T+ε then A(x')=1; (2) if |x|+ε<T then A(x')=0.

## Lean propositions

- `abs_threshold_preservation` : `Research.Operators.AbsThreshold.Preservation.AbsThresholdPreservationProp`
- `abs_threshold_sharpness` : `Research.Operators.AbsThreshold.Preservation.AbsThresholdSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.abs_threshold.v1",
  "score_space": "REAL_SCALAR"
}
```

- conclusion_digest: `47f2855d21dd032823198a5915e6e44ab47936ebc18ce42da647f9f08e79d6e1`
- semantic_freeze_digest: `759b4bef34e3b7f43339eac3523c51e3e00cb57cd03742dc2124f8ef444cd27b`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "ABS_GE_T_PASSES",
  "extensionality": "DEFAULT",
  "finiteness": "SCALAR",
  "measure_stage": "NONE",
  "score_encoding": "REAL_MATHLIB",
  "tie_break": "NONE"
}
```

## Build

- build_ok: `True`
- sorry_count: `0`
- admit_count: `0`
- lake_log_digest: `018e0cd8d327aea55a50e638c4b28c565a65a50f320102cf49cf0d40ce860bf1`
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
