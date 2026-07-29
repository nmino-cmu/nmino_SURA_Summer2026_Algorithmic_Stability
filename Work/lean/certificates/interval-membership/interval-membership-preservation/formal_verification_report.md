# Formal verification report

- operator: `interval-membership`
- theorem_id: `interval-membership-preservation`
- candidate_digest: `ed17f9e4b8314e4919ef82d39926b03b7bd745974fb6b797246b1b69c3ca2ad0`
- bundle_digest: `04980783f3e0e3205173fc7a493f56896fc63f87eedbb9e6a266ec69ad3e5789`
- crp_digest: `3253998523a7ce889a7234ed38d3e4f36ebda1e65d9e74d9c5e92dd728f89c9d`
- verification_run_id: `40a6d795-3ffc-464d-ba25-0aa25145bb53`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let x,x'∈ℝ, ε≥0 with |x'-x|≤ε, and L≤U. Define I(x)=1{L≤x≤U}. (1) if L+ε≤x≤U−ε then I(x')=1; (2) if x<L−ε or x>U+ε then I(x')=0.

## Lean propositions

- `interval_membership_preservation` : `Research.Operators.IntervalMembership.Preservation.IntervalMembershipPreservationProp`
- `interval_membership_sharpness` : `Research.Operators.IntervalMembership.Preservation.IntervalMembershipSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.interval_membership.v1"
}
```

- conclusion_digest: `e6c06f8da3462ca2e554f92c4cc012ea9cd67b2984e7f0ed49e5c2e0893528e8`
- semantic_freeze_digest: `ac3c3ed3f061c922cab8c1228e152cf4204bdaf430086948fea73c8bd50cd7ea`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "CLOSED_INTERVAL",
  "extensionality": "DEFAULT",
  "finiteness": "SCALAR",
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
