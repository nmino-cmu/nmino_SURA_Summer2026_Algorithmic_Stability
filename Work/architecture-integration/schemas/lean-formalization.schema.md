# Lean formalization wire schemas (ART-LEAN)

**Authority:** ART-INT companion · runtime ART-LEAN-RUNTIME · binding ART-10b

## ARTLEAN.BUNDLE.v1

```text
LeanInputBundle
  schema_version              # "ARTLEAN.BUNDLE.v1"
  bundle_digest               # H("ARTLEAN.BUNDLE.v1", body without this field)
  sealed_crp                  # CRP wire object
  crp_digest
  receipt                     # IntakeReceipt wire
  verification_run            # {run_id, results[], audit_verdict, limitations[], counterexamples[]}
  feedback_export_digest?
  created_at                  # ISO-8601 UTC
```

## ARTLEAN.FC.v1

See `architecture_verifier/10-lean/FORMALIZATION_IR.md`. Conclusion payloads are closed-token objects (`ARTLEAN.CONCL.<op>_<thm>.v1`); floats forbidden (ART-21b).

## Feedback export addition

`VerifierFeedbackExport.lean_manifest_digest?` — optional. Consumers **recompute** `DerivedLeanStatus` from the manifest; do not treat a stored status string as authority (I-LM-11).
