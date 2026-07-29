# Formal verification report

- operator: `multi-threshold`
- theorem_id: `multi-threshold-count-preservation`
- candidate_digest: `3f52fb1325916b770c164e26685fc97a743ed02e4d2d79491cf848f7a27b99df`
- bundle_digest: `8485cb9184a68636470f3dd532d58f0cb155a4fea394b32759bb28b1a886d5f2`
- crp_digest: `77dc741eb5b483243a36ec772f7a5641ceac53b276a9ad1ad3ec6025b03c6b46`
- verification_run_id: `f8a0c5db-7464-48f7-a658-e99b5e337445`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let x,x'∈ℝ, ε≥0 with |x'-x|≤ε, and let T=(T_0,…,T_{n-1}) be a finite list of finite thresholds. Define C_T(x)=|{i: x≥T_i}|. If for every i either x≥T_i+ε or x<T_i−ε, then C_T(x')=C_T(x).

## Lean propositions

- `multi_threshold_preservation` : `Research.Operators.MultiThreshold.Preservation.MultiThresholdPreservationProp`
- `multi_threshold_sharpness` : `Research.Operators.MultiThreshold.Preservation.MultiThresholdSharpnessProp`

## Conclusion tokens

```json
{
  "equality_convention": "X_GE_TI_PASSES",
  "output": "PASS_COUNT",
  "perturbation": "ABS_DIFF_LE_EPS",
  "schema_id": "ARTLEAN.CONCL.multi_threshold_preservation.v1",
  "score_space": "REAL_SCALAR",
  "stability": "ALL_COORDINATES_STABLE"
}
```

- conclusion_digest: `c1d2c1fed33b9138747e1fad3df0200dd27474289f6986d7261fdf806da3bbc9`
- semantic_freeze_digest: `dc5a7be0037a2406a11d7caa0c502d96c93208906e72fedef7b5c7cd666041f0`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "INT_GE_PASSES_PER_CUT",
  "extensionality": "DEFAULT",
  "finiteness": "FINITE_THRESHOLD_LIST",
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
