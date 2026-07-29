# Formal verification report

- operator: `thresholding`
- theorem_id: `threshold-output-preservation`
- candidate_digest: `44529f5a834504292c8e4ed32b2f9dd4ee901e2a55a7a9a1229de090a107dbae`
- bundle_digest: `fb889af892fb964edf2ca6e5f76e3007761c54849e06b17386ceb43580208c0e`
- crp_digest: `cb22f14de259d8121bffca9213fabf6adff57370334be63ae1f0fe4d42cbbfc9`
- verification_run_id: `324be6ff-52a1-4958-bb4a-7c438f9cd191`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let x,x'∈ℝ and ε≥0 with |x'-x|≤ε. For A_T(x)=1{x≥T} with fixed T∈ℝ: (1) if x≥T+ε then A_T(x')=1; (2) if x<T-ε then A_T(x')=0; (3) if x∈[T-ε,T+ε) the output need not be invariant.

## Lean propositions

- `threshold_preservation` : `Research.Operators.Threshold.Preservation.ThresholdPreservationProp`

## Conclusion tokens

```json
{
  "equality_convention": "X_GE_T_PASSES",
  "fail_condition": "X_LT_T_MINUS_EPS",
  "pass_condition": "X_GE_T_PLUS_EPS",
  "perturbation": "ABS_DIFF_LE_EPS",
  "schema_id": "ARTLEAN.CONCL.threshold_preservation.v1",
  "score_space": "REAL_SCALAR",
  "unstable_region": "HALF_OPEN_BAND"
}
```

- conclusion_digest: `6bf05ef7bb432e9cd44c584e0a413459f3b5e1c5659c0d958c1766bc67606409`
- semantic_freeze_digest: `22b810639044c5580f9bc3c8c86914911e95f2dad6525dcf50504ecd11e3bd7d`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "REAL_GE_PASSES",
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
