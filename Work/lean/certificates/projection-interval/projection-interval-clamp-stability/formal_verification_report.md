# Formal verification report

- operator: `projection-interval`
- theorem_id: `projection-interval-clamp-stability`
- candidate_digest: `a42fef4d2956ba5a6c47731df81448b11e9c73c1ee3838b70afbd16c0ddd0f54`
- bundle_digest: `3c076ad41e8df8a05b38e871a0ed23e3503ff1ee24f6ae4935ea159d0f9004fa`
- crp_digest: `ddf73d34f4ccbb643f54f5c45f4400e1f433b5123a4897d5125e9b2b7726ee78`
- verification_run_id: `90c08150-12d3-4603-b9fd-f78934417192`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let lo<=hi and |x'-x|<=epsilon. Then |clamp(x';lo,hi)-clamp(x;lo,hi)|<=epsilon (Projection onto interval is 1-Lipschitz / nonexpansive on Int).

## Lean propositions

- `projection_interval_clamp_stability` : `Research.Operators.ProjectionInterval.Preservation.ProjectionIntervalStabilityProp`
- `projection_interval_clamp_sharpness` : `Research.Operators.ProjectionInterval.Preservation.ProjectionIntervalSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.projection_interval.v1"
}
```

- conclusion_digest: `2a5740f443bc10ec6002f4835f98dfa7b90af7c7e0c43519f94835c4d558fec1`
- semantic_freeze_digest: `3a54ff8bc471bf76554b18f9054346be888d734bcf2ba3f3f2686c9eb21724bc`
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
