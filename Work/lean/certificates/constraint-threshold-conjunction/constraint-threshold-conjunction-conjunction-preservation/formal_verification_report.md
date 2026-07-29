# Formal verification report

- operator: `constraint-threshold-conjunction`
- theorem_id: `constraint-threshold-conjunction-conjunction-preservation`
- candidate_digest: `243a78e3e0f3491f14fc3d15cf972e92d8bc8bd924bb35c994e082cb4405edcf`
- bundle_digest: `563a987a62750238995bdd41388871201f76ee999c10c24193af5bfa16a3a874`
- crp_digest: `c64d0b87d6dfa26d39b762aba78d7d2131fe2ed90427c6b1ba84159f0a86eeb2`
- verification_run_id: `e40ebbaf-a800-4d37-829a-b53a4cab36d0`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Under coordinatewise epsilon-stability of each threshold, the multi-threshold pass-count is preserved; hence the conjunction (all-pass) bit is preserved (Constraint-threshold conjunction).

## Lean propositions

- `constraint_threshold_conjunction_conjunction_preservation` : `Research.Operators.ConstraintThresholdConjunction.Preservation.ConstraintThresholdConjunctionPreservationProp`
- `constraint_threshold_conjunction_conjunction_sharpness` : `Research.Operators.ConstraintThresholdConjunction.Preservation.ConstraintThresholdConjunctionSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.constraint_threshold_conjunction.v1"
}
```

- conclusion_digest: `67ae258a841a1dabc03f20728d191e83adfd29576d17b391d856aac350492a7b`
- semantic_freeze_digest: `e4456a92f60345a2fb6753bcad59fc359d32af73bc5a150161339a31ebfabf0f`
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
