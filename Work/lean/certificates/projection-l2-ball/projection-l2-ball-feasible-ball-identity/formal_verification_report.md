# Formal verification report

- operator: `projection-l2-ball`
- theorem_id: `projection-l2-ball-feasible-ball-identity`
- candidate_digest: `684e98ea8b014aaac682b58ef7e025bcaaa8fdb1d01f133f783e2d0ee1863668`
- bundle_digest: `3c3b27d2ef0dc4e6f8ebf3e0f0728f3bdfb809d63807e89f4b066acb2339731c`
- crp_digest: `bfd520e3b9a31bf18e1ac349839af1cadd292b8bb52f200d1958b5494f8ef4b1`
- verification_run_id: `af004e4f-7aff-43d8-a4bb-4ae085e59270`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

If proj fixes InSet pointwise and the closed epsilon-ball about x lies in InSet, then for all |x'-x|<=epsilon one has proj(x')=x' and proj(x)=x (Projection onto the l2 ball: feasible-ball identity, Mathlib Real).

## Lean propositions

- `projection_l2_ball_feasible_ball_identity` : `Research.Operators.ProjectionL2Ball.Preservation.ProjectionL2BallIdentityProp`
- `projection_l2_ball_feasible_ball_sharpness` : `Research.Operators.ProjectionL2Ball.Preservation.ProjectionL2BallSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.projection_l2_ball.v1"
}
```

- conclusion_digest: `11e23f852920b4f5d0ddfc9153d2ebe4aa92061f8181f906338b519ebd89ece9`
- semantic_freeze_digest: `3ecc7790875107dd550bfdae604f8acb3293f255cb63648f7847aa433494599b`
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
