# Formal verification report

- operator: `greedy-choice-tie-break`
- theorem_id: `greedy-choice-tie-break-margin`
- candidate_digest: `22c4fd41743d2ce8ff37444e9fc3dcf26f547fac1f5536667d1cc3f9a71754cf`
- bundle_digest: `d12ade3016eea1f98d5b22c40a9e16f8cc6e22639c29b05fdb1cd1451963560d`
- crp_digest: `9f3ffe63cffee54ac19a700ac6e13c76753f83e61184bc0f4dacf949b6834bab`
- verification_run_id: `29aa7065-2c43-4b67-b815-20c5db5ba2ca`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (tie-broken greedy scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Greedy choice with deterministic tie-breaking reduces to Argmax margin).

## Lean propositions

- `greedy_choice_tie_break_margin_invariance` : `Research.Operators.GreedyChoiceTieBreak.Margin.GreedyChoiceTieBreakMarginInvarianceProp`
- `greedy_choice_tie_break_margin_sharpness` : `Research.Operators.GreedyChoiceTieBreak.Margin.GreedyChoiceTieBreakMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.greedy_choice_tie_break_margin.v1"
}
```

- conclusion_digest: `510b7bc12b6aec04633f44dda65f960237cbd3ed709dbe0353ec04fc7c03b160`
- semantic_freeze_digest: `2b07cee53c273d4552e3151403260d83bcad949fcd4784e875623dd98e8890c6`
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
