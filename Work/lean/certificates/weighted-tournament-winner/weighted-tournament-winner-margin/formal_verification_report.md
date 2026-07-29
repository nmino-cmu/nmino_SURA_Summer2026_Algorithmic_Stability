# Formal verification report

- operator: `weighted-tournament-winner`
- theorem_id: `weighted-tournament-winner-margin`
- candidate_digest: `1ad2def1778f2cf2052a3106ae571dbd4437fa565f395b38b57fa0f3680f84b0`
- bundle_digest: `310b9c68000e1860632203725234bd0029fecc8f1bd3e6401fef187cb63c7613`
- crp_digest: `1408b51f06c91bd44fbf776fefb8848988fbbb55a069b7d8fe7acb8384095cd2`
- verification_run_id: `cdfc2112-3b75-44d0-ad04-18aa0f3c6b84`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (weighted tournament scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Weighted tournament winner reduces to Argmax margin).

## Lean propositions

- `weighted_tournament_winner_margin_invariance` : `Research.Operators.WeightedTournamentWinner.Margin.WeightedTournamentWinnerMarginInvarianceProp`
- `weighted_tournament_winner_margin_sharpness` : `Research.Operators.WeightedTournamentWinner.Margin.WeightedTournamentWinnerMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.weighted_tournament_winner_margin.v1"
}
```

- conclusion_digest: `4757007c1f4df21ac5d930337aa5eba1376773e0d0be8e1fae45745af6964727`
- semantic_freeze_digest: `f72ba620d469e7d52e34b93bf248e76cd513d1100b5f04396bc56479a052e994`
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
