# Formal verification report

- operator: `tournament-winner`
- theorem_id: `tournament-winner-margin`
- candidate_digest: `d563e4489a275f275f3edf37f994f48ea32e00943f84b3113c5bfd2517c66128`
- bundle_digest: `978fcc564f86db761a2cb2a63c001ea0c4d6efaa743c4c8fe2fc6b77b0fd8169`
- crp_digest: `11b4c276620ad8af2534aa6746ed609d7d4161795386a7ae1cc7645585b12a82`
- verification_run_id: `a3acfd41-c54c-498b-bc7c-ef156c10dd9d`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (tournament scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Tournament winner reduces to Argmax margin).

## Lean propositions

- `tournament_winner_margin_invariance` : `Research.Operators.TournamentWinner.Margin.TournamentWinnerMarginInvarianceProp`
- `tournament_winner_margin_sharpness` : `Research.Operators.TournamentWinner.Margin.TournamentWinnerMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.tournament_winner_margin.v1"
}
```

- conclusion_digest: `26e8bfd6ff462c87b1bf47e21cc45a1cc09181c2220c447888deb137fbff3177`
- semantic_freeze_digest: `8b84afcc01655401826f76b93c9efed4dea71e6b3f4f7755c9fd603728834d61`
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
