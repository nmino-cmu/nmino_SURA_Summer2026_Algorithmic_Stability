# Formal verification report

- operator: `projection-l1-ball`
- theorem_id: `projection-l1-ball-feasible-ball-identity`
- candidate_digest: `5fc87a20ce8cd8def1da2bcccf52ca53becfa959393db5603aa7406e147b7820`
- bundle_digest: `35a11099c9421bc47486528e40eaa73bffa420465115a4a0b875aa7717bd70a2`
- crp_digest: `dfa41a498a39cf1f9efac8805d2e44bd220b69dc4f31013ddedaac96dfd064a5`
- verification_run_id: `4e2a25f1-f6ad-4436-bca6-3daddc91e37b`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

If proj fixes InSet pointwise and the closed epsilon-ball about x lies in InSet, then for all |x'-x|<=epsilon one has proj(x')=x' and proj(x)=x (Projection onto the l1 ball: feasible-ball identity, Mathlib Real).

## Lean propositions

- `projection_l1_ball_feasible_ball_identity` : `Research.Operators.ProjectionL1Ball.Preservation.ProjectionL1BallIdentityProp`
- `projection_l1_ball_feasible_ball_sharpness` : `Research.Operators.ProjectionL1Ball.Preservation.ProjectionL1BallSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.projection_l1_ball.v1"
}
```

- conclusion_digest: `2821f42de56899c9056f7244166f1483eb79b4642887d867dab24a686e3ae3c8`
- semantic_freeze_digest: `6cc995ae77c4f82d9fbb70bde68b86d2d451c39960de206a0905533bf1e9c37f`
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
