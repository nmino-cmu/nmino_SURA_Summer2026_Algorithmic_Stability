# Formal verification report

- operator: `nms-finite`
- theorem_id: `nms-finite-margin`
- candidate_digest: `162b9a4949e09977aded9be89252c1012e16ed0509670bceaddb53162d0b1884`
- bundle_digest: `6188c15f0d1a6be4438f8c306e2da075835695a3934b574c6ae7f29486dcfb47`
- crp_digest: `b04388509c8d0e96398cd9b8ab1896fc4400d9ad53b37d3741112bb001dc5d3f`
- verification_run_id: `fdd538ab-f110-4ec5-bbbb-af723c554804`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (finite NMS candidate scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Non-maximum suppression (finite) reduces to Argmax margin).

## Lean propositions

- `nms_finite_margin_invariance` : `Research.Operators.NmsFinite.Margin.NmsFiniteMarginInvarianceProp`
- `nms_finite_margin_sharpness` : `Research.Operators.NmsFinite.Margin.NmsFiniteMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.nms_finite_margin.v1"
}
```

- conclusion_digest: `037c95e9085637b7fee5bb69faebb761b0c2cd8d1bccfe23572c73074f8be34c`
- semantic_freeze_digest: `9a23ea63e24e88c3e9b17c5991a5c4a1656d6b2256e6b71bbc5f84d65c602177`
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
