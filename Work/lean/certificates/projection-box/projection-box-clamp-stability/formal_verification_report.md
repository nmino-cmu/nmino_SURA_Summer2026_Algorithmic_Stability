# Formal verification report

- operator: `projection-box`
- theorem_id: `projection-box-clamp-stability`
- candidate_digest: `ba4c351792a610d66313b103fe616ecd9c6de96f2d29588ab69bbd243d4d1cee`
- bundle_digest: `699c2acfcd950252a0231298ccfcb82d7d3ee16a3f8fcfd7a92d9156520d7ebf`
- crp_digest: `b173610af9f1474d326fab64f98fd0d1af61952ae727457bcd2623ba572cddcd`
- verification_run_id: `7f1dd603-bd20-43c0-bdf0-95a13fa88890`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let lo<=hi and |x'-x|<=epsilon. Then |clamp(x';lo,hi)-clamp(x;lo,hi)|<=epsilon (Projection onto box constraints is 1-Lipschitz / nonexpansive on Int).

## Lean propositions

- `projection_box_clamp_stability` : `Research.Operators.ProjectionBox.Preservation.ProjectionBoxStabilityProp`
- `projection_box_clamp_sharpness` : `Research.Operators.ProjectionBox.Preservation.ProjectionBoxSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.projection_box.v1"
}
```

- conclusion_digest: `1d3220eb76fbe8fc039dca68bfabb5c353bfec7b79c75d9448109c441bf3b632`
- semantic_freeze_digest: `0fb8bee544e94a1b8b47ede1a5f159cc2bdaabce76b139e5ef4e21e345f17fbb`
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
