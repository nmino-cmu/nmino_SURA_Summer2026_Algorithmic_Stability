# Formal verification report

- operator: `constraint-threshold-disjunction`
- theorem_id: `constraint-threshold-disjunction-disjunction-preservation`
- candidate_digest: `b1d75d313311a36d4f9021e7cc683bc45021c5d8f50834ff59be073c4747f27b`
- bundle_digest: `07acc574657d1d0c2803a5af7198fe25e819594bc0ddb30aea48719b82135c81`
- crp_digest: `38cb9f4fc03448fa28f6fab339d5ede3cd1c60e079d88631017fe778586a07a3`
- verification_run_id: `b8e1c97d-a552-44c4-98e5-e7207e749d16`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Under coordinatewise epsilon-stability of each threshold, the multi-threshold pass-count is preserved; hence the disjunction (any-pass) bit is preserved (Constraint-threshold disjunction).

## Lean propositions

- `constraint_threshold_disjunction_disjunction_preservation` : `Research.Operators.ConstraintThresholdDisjunction.Preservation.ConstraintThresholdDisjunctionPreservationProp`
- `constraint_threshold_disjunction_disjunction_sharpness` : `Research.Operators.ConstraintThresholdDisjunction.Preservation.ConstraintThresholdDisjunctionSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.constraint_threshold_disjunction.v1"
}
```

- conclusion_digest: `812d4aee59d36aa350d8a4f198986f2e50717394cbe0bec5b42eef5b75dce1ce`
- semantic_freeze_digest: `f8700530775e1a9dfbca7d82c2e3e248e33a70da348833af046345fe8aecb11d`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "DEFAULT",
  "extensionality": "DEFAULT",
  "finiteness": "SCALAR_OR_LIST",
  "measure_stage": "NONE",
  "score_encoding": "REAL_MATHLIB",
  "tie_break": "NONE"
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
