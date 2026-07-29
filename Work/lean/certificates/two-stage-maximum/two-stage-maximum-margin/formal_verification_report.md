# Formal verification report

- operator: `two-stage-maximum`
- theorem_id: `two-stage-maximum-margin`
- candidate_digest: `19b9a8a0d6e2addaf8064c46bef9f107b3c1f7d32b015f32a6606637bcdc8fcc`
- bundle_digest: `e34d559bb65056ed08f3245d782385673249985ac8fc3f183c0439a96ab77478`
- crp_digest: `0495377eae02cb1d3b9178265471be1cac67c6fcc12cadb2bd1d3f1d4c7de7b7`
- verification_run_id: `f603b567-5364-4869-8526-e15ca9cbcc82`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (two-stage scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Two-stage maximum reduces to Argmax margin).

## Lean propositions

- `two_stage_maximum_margin_invariance` : `Research.Operators.TwoStageMaximum.Margin.TwoStageMaximumMarginInvarianceProp`
- `two_stage_maximum_margin_sharpness` : `Research.Operators.TwoStageMaximum.Margin.TwoStageMaximumMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.two_stage_maximum_margin.v1"
}
```

- conclusion_digest: `b494773fda76741589d9b23d7b2715afba2aa8b4aaed189ce521cdc6854bb755`
- semantic_freeze_digest: `c88a13a6a15f355ef0d908e6534716537010a242ecd31c98d3cda132ccf38a11`
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
