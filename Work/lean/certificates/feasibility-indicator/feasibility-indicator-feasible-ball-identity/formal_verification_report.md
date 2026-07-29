# Formal verification report

- operator: `feasibility-indicator`
- theorem_id: `feasibility-indicator-feasible-ball-identity`
- candidate_digest: `54afe74f13c2e47e5478d1d765054073a5609fa66c34101e9456e70e65ae2013`
- bundle_digest: `756b7aa980152ec58f44c4d2307177bc97401e7b3d9c4b02303aa96b2c5bc41a`
- crp_digest: `6d6490f236b5cd7b67b5383fcfcdbeb83fac46cce3b30998bd28ea399b195703`
- verification_run_id: `f7cd11b5-f8f7-45d6-b4c2-ba21cb68998c`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

If proj fixes InSet pointwise and the closed epsilon-ball about x lies in InSet, then for all |x'-x|<=epsilon one has proj(x')=x' and proj(x)=x (Feasibility indicator over a fixed set: feasible-ball identity, Mathlib Real).

## Lean propositions

- `feasibility_indicator_feasible_ball_identity` : `Research.Operators.FeasibilityIndicator.Preservation.FeasibilityIndicatorIdentityProp`
- `feasibility_indicator_feasible_ball_sharpness` : `Research.Operators.FeasibilityIndicator.Preservation.FeasibilityIndicatorSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.feasibility_indicator.v1"
}
```

- conclusion_digest: `f66d6948c685248bbc2aea564de0513017d06a2500765dcb4c62cf6f09e4f180`
- semantic_freeze_digest: `02d3af7977d9dc7f64545f7dde5472e513254e1f800c4d300f3dca07f0aeed32`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "DEFAULT",
  "extensionality": "DEFAULT",
  "finiteness": "SCALAR_OR_LIST",
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
