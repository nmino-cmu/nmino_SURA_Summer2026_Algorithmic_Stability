# Formalization IR (BUNDLE + FC)

**Schemas:** `ARTLEAN.BUNDLE.v1` · `ARTLEAN.FC.v1` · `ARTLEAN.CONCL.*`

## LeanInputBundle

Persisted handoff from System 2: sealed CRP wire + IntakeReceipt + verification_run snapshot + digests.

Producer: `system_b.lean.bundle.export_bundle`  
Consumer: eligibility → FC mint → Lake workflow.

## FormalizationCandidate

Tokenized conclusion only (closed enums / ints / bools — no free-form math, no floats).  
`conclusion_digest` = ART-21b object digest of conclusion tokens.  
`lean_statement_digest` (transcript) = hash of STATEMENT marker region in Lean source.

## Eligibility

Fail closed: PASS audit, DISCHARGED obligations, profile allowlist, exact statement match, no DEMO_*, no CX.

Wire schema home: `architecture-integration/schemas/lean-formalization.schema.md`.
