# Formal verification report

- operator: `projection-simplex`
- theorem_id: `projection-simplex-feasible-ball-identity`
- candidate_digest: `e6bff027074081eb3939c92bad0c722961a0c4fac3381a50747eb0779d1aded7`
- bundle_digest: `5ef89dd90f2ea18aa836fe21f971697b6143b20c805b143d8403b9f2410560cb`
- crp_digest: `2e0a0ae45e31bde34b401c87b22134b46a76830cc5797a93bc45a0b45972f0cc`
- verification_run_id: `41dbad96-edf4-405f-8f34-82f0d4be60c1`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

If proj fixes InSet pointwise and the closed epsilon-ball about x lies in InSet, then for all |x'-x|<=epsilon one has proj(x')=x' and proj(x)=x (Projection onto simplex: feasible-ball identity, Mathlib Real).

## Lean propositions

- `projection_simplex_feasible_ball_identity` : `Research.Operators.ProjectionSimplex.Preservation.ProjectionSimplexIdentityProp`
- `projection_simplex_feasible_ball_sharpness` : `Research.Operators.ProjectionSimplex.Preservation.ProjectionSimplexSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.projection_simplex.v1"
}
```

- conclusion_digest: `8f64a9e70db33f76d7d74988e984c83cb2234b3333fa2b352d264be19bd563d2`
- semantic_freeze_digest: `dc2d4696baf84a1bd2f9b43a3d5d5b3239fb7693aa7c8d8f509ce389cea32243`
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
