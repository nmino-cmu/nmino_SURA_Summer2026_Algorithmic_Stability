# Formal verification report

- operator: `priority-queue-maximum`
- theorem_id: `priority-queue-maximum-margin`
- candidate_digest: `89a43b90146dc45d5cd49072d54f07ba03fcc78da7c55fc6a0ad4648784121b9`
- bundle_digest: `57fca98fc2353771b7f3d17671f937017d3386354bddcf8f7c705a317c617177`
- crp_digest: `901827065c6f496cae8224bafcc36781ea054766e5feceafce135abaa3720993`
- verification_run_id: `ac03ad0b-68f1-4233-898f-4425b65582df`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (priority-queue key scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Priority queue maximum reduces to Argmax margin).

## Lean propositions

- `priority_queue_maximum_margin_invariance` : `Research.Operators.PriorityQueueMaximum.Margin.PriorityQueueMaximumMarginInvarianceProp`
- `priority_queue_maximum_margin_sharpness` : `Research.Operators.PriorityQueueMaximum.Margin.PriorityQueueMaximumMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.priority_queue_maximum_margin.v1"
}
```

- conclusion_digest: `b60747955e2ad796176a63ab56806eca36b2ce0c0a3c0e8d39dd718dd286f47d`
- semantic_freeze_digest: `3d9cefecf144da0ed815b2dcc842777a788a7a10a6d6359e42d898f1fe29e375`
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
