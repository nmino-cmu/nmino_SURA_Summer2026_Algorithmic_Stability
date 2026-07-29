# VerifierFeedbackExport (ART-INT)

**Authority:** ART-INT-00. Sole normative B→A feedback object. Carriers: `I.LibraryExport`, `I.DiscoveryStatus`, `IntakeReceipt` copies.

```text
VerifierFeedbackExport
  schema_version              # "ARTINT.FB.v1"
  export_digest               # H("ARTINT.FB.v1", canonical body without this field)
  crp_digest                  # exact submitted package
  sealed_digest               # MUST equal crp_digest
  receipt_digest?             # IntakeReceipt when intake completed
  intake_status               # ACCEPTED_DRAFT | REJECTED | UNKNOWN
  reason_codes[]?             # intake / schema failures
  profile                     # CRP profile used
  audit_profile_id?           # e.g. ART11b.CHAR
  cx_profile_id?              # e.g. ART-12-CHAR
  verification_run_id?
  run_started_at?
  run_completed_at?
  draft_claim_digests[]
  obligation_digests[]
  obligations[]               # { obligation_digest, status, obligation_type, blocks_promotion }
  audit_verdict?              # PASS | FAIL | IRRELEVANT | ESCALATE_HUMAN | NONE
  audit_record_digest?
  counterexamples[]           # { cx_digest, refutation_type, target_claim_digests[] }
  failed_obligations[]        # digests with status FAILED
  unresolved_obligations[]    # OPEN blocking
  discharged_obligations[]
  assumptions_introduced[]?   # claim/assumption digests noted by B
  proof_sketches_refs[]?      # digests only
  maturity_by_claim[]?        # { claim_digest, research_maturity }
  certified_object_digests[]? # library-exportable
  verifier_limitations[]?     # strings / codes
  revision_guidance[]?        # non-authoritative hints for A
  confidence_notes[]?         # non-authoritative
  lean_manifest_digest?       # ART-10b LeanManifest.manifest_digest; recompute status — do not store lean_status labels
  provenance                  # { event_seq?, commit_event_seq?, exporter_role }
  content_digest              # digest of normative export body for VerifierPrior.content_digest
```

**I-INT-FB-01:** Export MUST identify exact package via `crp_digest` / `sealed_digest`.  
**I-INT-FB-02:** Multiple runs ⇒ distinct `verification_run_id`; later export may supersede for A import policy; B retains history.  
**I-INT-FB-03:** Infrastructure failure ⇒ export with `intake_status`/`audit_verdict` unset or `NONE` and `verifier_limitations` including `INFRA_FAILURE`; not a math FAIL.  
**I-INT-FB-04:** A maps export → `VerifierPrior` with `export_ref=export_digest`, `content_digest`, and required provenance fields.

### I.LibraryExport binding

```text
I.LibraryExport(filter) → { objects: certified digests… } | VerifierFeedbackExport
```

When returning package-scoped feedback, result MUST be `VerifierFeedbackExport` (this schema). Bare digest lists remain allowed for library browse; they are insufficient alone for DS12 active prior without receipt/sealed binding.
