# Formal verification report

- operator: `sign`
- theorem_id: `sign-preservation`
- candidate_digest: `b4f1f378d872a0f081f57f7818c8aa8f2be404a4d9ba08b4055dc6bb4199b0f4`
- bundle_digest: `0d70e1ef015a4521540a923d22f5b6180362c1e000543eccf4ecc7e7573c30b0`
- crp_digest: `4d1a5af552b4fbee7d3ec1b5715c052f9c0f5b0df40672ceb8df2aafb3d32b6c`
- verification_run_id: `b6f2786f-fe89-4037-a1eb-371558c494f2`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let x,x'∈ℝ and ε≥0 with |x'-x|≤ε. Define sign(x)=1 if x>0, -1 if x<0, else 0. (1) if x>ε then sign(x')=1; (2) if x<-ε then sign(x')=-1; (3) if ε=0 and x=0 then sign(x')=0.

## Lean propositions

- `sign_preservation` : `Research.Operators.Sign.Preservation.SignPreservationProp`
- `sign_sharpness` : `Research.Operators.Sign.Preservation.SignSharpnessProp`

## Conclusion tokens

```json
{
  "output": "SIGN_TRICHOTOMY",
  "perturbation": "ABS_DIFF_LE_EPS",
  "schema_id": "ARTLEAN.CONCL.sign_preservation.v1",
  "score_space": "REAL_SCALAR"
}
```

- conclusion_digest: `987547c39c9d6413a8e0148b54f870cfd55a58ad89bfcc2689fefcdd61528a60`
- semantic_freeze_digest: `262f7f4a1cc78fae2d4ce8e349d4f44c6c53fc0d55011bb3d1fdbec1f8f05a89`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "SIGN_ZERO_AT_ZERO",
  "extensionality": "DEFAULT",
  "finiteness": "SCALAR",
  "measure_stage": "NONE",
  "score_encoding": "REAL_MATHLIB",
  "tie_break": "ZERO_AT_ORIGIN"
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
