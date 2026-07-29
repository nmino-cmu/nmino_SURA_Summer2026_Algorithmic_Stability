# Formal verification report

- operator: `greedy-maximum-selection`
- theorem_id: `greedy-maximum-selection-margin`
- candidate_digest: `da63b321bcbf86263043ff5d2fe2d68890801e4bdf97c97fc8031acbb8c9bd42`
- bundle_digest: `92c833fb3cbdf7df3842cf29ad0825facc851effa83736ac8b1a6fd5d92b13f8`
- crp_digest: `0e678acc7a4d6951b0d3fae3b7cf915fa250faa02157f26d9881947692ff2d6d`
- verification_run_id: `8c96ffce-c5be-4226-b4fe-c8f350e64d73`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (greedy admissible scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Greedy maximum selection reduces to Argmax margin).

## Lean propositions

- `greedy_maximum_selection_margin_invariance` : `Research.Operators.GreedyMaximumSelection.Margin.GreedyMaximumSelectionMarginInvarianceProp`
- `greedy_maximum_selection_margin_sharpness` : `Research.Operators.GreedyMaximumSelection.Margin.GreedyMaximumSelectionMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.greedy_maximum_selection_margin.v1"
}
```

- conclusion_digest: `78650e5bbf964621ec27f3fd9448f38fd7ec7437a7bbac029a62ea1cc42d0da6`
- semantic_freeze_digest: `2fc7aa3abdb2e81f71d4f30713920b845b3e8b4f62742dba6c62517a5405a6fa`
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
