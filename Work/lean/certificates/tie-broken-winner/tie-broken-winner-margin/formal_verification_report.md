# Formal verification report

- operator: `tie-broken-winner`
- theorem_id: `tie-broken-winner-margin`
- candidate_digest: `9c1cb3899facc8028a24e5d366e134cf345dac72b1a1f6198b32406eefee0973`
- bundle_digest: `4a1d7b0c4082592481c34c0e1b8bd3dbf1e1039fd4ed92d490c0b11353e629b9`
- crp_digest: `c3383b14ec2c73584498f933ef14d684a7da1d95fec0b2701391055bd4fedc21`
- verification_run_id: `3125dc75-ee2d-409c-a089-d74ca3d6992e`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (tie-broken scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Tie-broken winner selection reduces to Argmax margin).

## Lean propositions

- `tie_broken_winner_margin_invariance` : `Research.Operators.TieBrokenWinner.Margin.TieBrokenWinnerMarginInvarianceProp`
- `tie_broken_winner_margin_sharpness` : `Research.Operators.TieBrokenWinner.Margin.TieBrokenWinnerMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.tie_broken_winner_margin.v1"
}
```

- conclusion_digest: `4d0f2420061f2aaca2d8813079877efdc95917fe354055bc2b665bae2e375b12`
- semantic_freeze_digest: `2631199ac62b5f9fb60bdbefa71187215c0b59ce245868d98e736facc0e75cf4`
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
