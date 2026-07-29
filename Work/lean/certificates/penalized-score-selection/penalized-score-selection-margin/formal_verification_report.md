# Formal verification report

- operator: `penalized-score-selection`
- theorem_id: `penalized-score-selection-margin`
- candidate_digest: `4994ebba8361d4d2bf52856d4d4b22788ba0ae15c9bbc107d11e3e4c25af0acb`
- bundle_digest: `dd8ec150e787e1e6f91d945b696352d178ac6a63059c4d8614a320d7a7fda9e6`
- crp_digest: `27df76c0b3c5d5d74e590ac4702942c216e6c96065a34d2efc05fa2a01f67602`
- verification_run_id: `91704413-f148-42b1-b702-634cac99ee7d`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (penalized scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Penalized score selection reduces to Argmax margin).

## Lean propositions

- `penalized_score_selection_margin_invariance` : `Research.Operators.PenalizedScoreSelection.Margin.PenalizedScoreSelectionMarginInvarianceProp`
- `penalized_score_selection_margin_sharpness` : `Research.Operators.PenalizedScoreSelection.Margin.PenalizedScoreSelectionMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.penalized_score_selection_margin.v1"
}
```

- conclusion_digest: `dc140d9ebc855f28f0052e54e6aa12ef6dfa98d22771fb47244d095f2abf933a`
- semantic_freeze_digest: `3da7cad659374a5cbc51107b1f893140fbe055992786c23b7db4f220ee0a10d0`
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
