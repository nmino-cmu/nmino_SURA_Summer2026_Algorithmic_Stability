# Formal verification report

- operator: `best-first-node-selection`
- theorem_id: `best-first-node-selection-margin`
- candidate_digest: `b698e06afd967967b071c07ea1027e9881d3129485c6a957c9d155fd5228d6ec`
- bundle_digest: `239672650bd5c9fd57accec6b2794a6999bfebc3bf245d1589c7ab20d3386db7`
- crp_digest: `acdc247bf5177bb735cd85394edbed329949cc6ff083885b9bff7c741f7e6dbf`
- verification_run_id: `09124b90-aa1d-4ff6-bbf8-5775473d98cc`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (best-first node scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Best-first node selection reduces to Argmax margin).

## Lean propositions

- `best_first_node_selection_margin_invariance` : `Research.Operators.BestFirstNodeSelection.Margin.BestFirstNodeSelectionMarginInvarianceProp`
- `best_first_node_selection_margin_sharpness` : `Research.Operators.BestFirstNodeSelection.Margin.BestFirstNodeSelectionMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.best_first_node_selection_margin.v1"
}
```

- conclusion_digest: `77a6845548650e4b84a4be7fbfb44cabd882a4f2dcd7bee4b303f622a5587d09`
- semantic_freeze_digest: `3be8abab2255136ecea45fc8f9561b74919f499a03e01df3d38dfd3b41346ab0`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "DEFAULT",
  "extensionality": "DEFAULT",
  "finiteness": "FINITE_VECTOR",
  "measure_stage": "NONE",
  "score_encoding": "REAL_MATHLIB",
  "tie_break": "UNIQUE_REQUIRED"
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
