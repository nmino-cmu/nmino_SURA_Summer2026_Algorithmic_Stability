# Formal verification report

- operator: `weighted-score-selection`
- theorem_id: `weighted-score-selection-margin`
- candidate_digest: `4ffe7bd9ef6110b159ccb49cde53099f698d0e527b586a26ed67df687b3df6e1`
- bundle_digest: `f8a34779feb5a4f3e0f5290b20c8cb596b3e184cddc3fb1f21a1dfafdf7574c2`
- crp_digest: `f5d5eac50d9b3a7df9140d395b8ea39d20d89cf335b349b3ded65489f3a666ef`
- verification_run_id: `756a01a3-2e71-4c31-88a5-4a44b1a690b3`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (weighted scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Weighted score selection reduces to Argmax margin).

## Lean propositions

- `weighted_score_selection_margin_invariance` : `Research.Operators.WeightedScoreSelection.Margin.WeightedScoreSelectionMarginInvarianceProp`
- `weighted_score_selection_margin_sharpness` : `Research.Operators.WeightedScoreSelection.Margin.WeightedScoreSelectionMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.weighted_score_selection_margin.v1"
}
```

- conclusion_digest: `2670cd9e177f3d77b09d48d8dacfc9b6b5c4915d91b50642e11baf4e62e05cd4`
- semantic_freeze_digest: `0c472bca66a9a339ce2deb03b4c5813777c19d89c4814a2ab6d980d2430637eb`
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
