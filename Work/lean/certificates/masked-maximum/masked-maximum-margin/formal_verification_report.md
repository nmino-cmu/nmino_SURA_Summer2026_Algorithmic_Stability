# Formal verification report

- operator: `masked-maximum`
- theorem_id: `masked-maximum-margin`
- candidate_digest: `0c20a80a06e7519ab82a0ebcd06c427ffc1d4a1bc1f2749c071d23e1d17a71cb`
- bundle_digest: `dfcfdbf0016addbaa1aded00d181d8e4c03fb39ff2b2403903dd99c73787a6d1`
- crp_digest: `d100dc77416058d4a5937546b54e782ebffe469049f94f8ac6bf008db3267e2a`
- verification_run_id: `5311f38f-ea38-4146-a5ba-3227b1f47e69`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (masked candidate scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Masked maximum reduces to Argmax margin).

## Lean propositions

- `masked_maximum_margin_invariance` : `Research.Operators.MaskedMaximum.Margin.MaskedMaximumMarginInvarianceProp`
- `masked_maximum_margin_sharpness` : `Research.Operators.MaskedMaximum.Margin.MaskedMaximumMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.masked_maximum_margin.v1"
}
```

- conclusion_digest: `8a3099b7ef665bacdd499d7dc549eaa08c95acd405b55053bcc866e85f1ed560`
- semantic_freeze_digest: `b22955761046bc1fba7447e30c3ea9911f50a0f8db99fd7199d238585eb17baa`
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
