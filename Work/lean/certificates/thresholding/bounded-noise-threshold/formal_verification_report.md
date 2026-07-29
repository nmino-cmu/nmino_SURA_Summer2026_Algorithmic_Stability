# Formal verification report

- operator: `thresholding`
- theorem_id: `bounded-noise-threshold`
- candidate_digest: `a4e42588bd61bbe2edcd80c53f7f2535e25b50367ede6786bb56acf1c81886b8`
- bundle_digest: `554205e2b78ba9f821d9fc6ba24c6c3dbfd8a083b025e5b901858c1f24d4d611`
- crp_digest: `974f5d833ced1a8d37bcb80f10ab7b9fed02c89b142d765e6713ae6541edaaa7`
- verification_run_id: `cb03b799-30d8-471a-affe-1556e1c137cb`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let η≥0 and ξ satisfy |ξ|≤η almost surely. For Ã_T(x)=1{x+ξ≥T} with fixed T∈ℝ: (1) if x≥T+η then Ã_T(x)=1 a.s.; (2) if x<T-η then Ã_T(x)=0 a.s.; (3) if x∈[T-η,T+η) the random output need not be a.s. constant.

## Lean propositions

- `bounded_noise_preservation` : `Research.Operators.Threshold.BoundedNoise.BoundedNoisePreservationProp`
- `bounded_noise_sharpness` : `Research.Operators.Threshold.BoundedNoise.BoundedNoiseSharpnessProp`

## Conclusion tokens

```json
{
  "equality_convention": "X_GE_T_PASSES",
  "fail_condition": "X_LT_T_MINUS_ETA",
  "mechanism": "ABOVE_THRESHOLD_X_PLUS_XI",
  "noise_model": "PATHWISE_ABS_XI_LE_ETA",
  "not_claimed": "FULL_SPARSE_VECTOR_PRIVACY",
  "pass_condition": "X_GE_T_PLUS_ETA",
  "schema_id": "ARTLEAN.CONCL.threshold_bounded_noise.v1",
  "score_space": "REAL_SCALAR",
  "unstable_region": "HALF_OPEN_BAND"
}
```

- conclusion_digest: `82755a9debe0a6f75bc950806a780ec53c957946d93f5527d585f0d7b72b0865`
- semantic_freeze_digest: `3b3c4eb9f65dc03dd374f956f6d38760c6d06ccab8d3f8a60b14596e001c2f5e`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "REAL_GE_PASSES",
  "extensionality": "DEFAULT",
  "finiteness": "SCALAR",
  "measure_stage": "PATHWISE_SURROGATE",
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

- `PATHWISE_NOT_MEASURE_THEORETIC_AS`
- `DEFINITION_PINS_SURROGATE`
- `BOUNDED_NOISE_NOT_FULL_SVT`

## Limitations of this certificate

- `LEAN_FULL` here means kernel-checked Mathlib `ℝ` propositions.
- Smoke theorems alone never authorize operator LEAN_FULL.
- PDF / markdown reports are derived views, not proof authority.

## Reuse

- `Research.Operators.Argmax.Basic` / `Margin` shared by argmax-family aliases.
