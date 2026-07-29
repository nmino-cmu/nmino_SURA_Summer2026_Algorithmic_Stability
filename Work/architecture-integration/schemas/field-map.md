# Field map A ↔ B (ART-INT)

**Authority:** ART-INT-00.

## A → B (submission)

| Destination (ART-CRP) | Source (A) | Req/Opt | Notes |
|-----------------------|------------|----------|-------|
| author_kind | Assistant seal context | Req | RESEARCH_DISCOVERY_ASSISTANT or HUMAN |
| author_principal_digest | Identity | Req | |
| author_binding_digest | Live binding | Req if ASSISTANT | |
| profile | profile_hint normalized | Req | profile-map |
| math_scope_pin_digest | ScopeBinding / tip | Req | |
| payload.definitions[] | DefinitionDraft | arrays present | |
| payload.assumptions[] | AssumptionDraft | | |
| payload.claims[] | TheoremCandidate, ConjectureCandidate | | |
| payload.proof_sketches[] | ProofSketch | | |
| payload.bridge_proposals[] | BridgeProposalDraft | | |
| payload.mechanism_proposals[] | MechanismProposal; ExampleCard.perturbation_mechanism_id alias | Opt Phase A | |
| payload.examples[] | ExampleCard | | |
| payload.falsifiers[] | FalsificationTarget, SoftFalsifierDraft | | |
| payload.counterexample_claims[] | Soft-attack drafts | | Soft ≠ B CX |
| payload.certificate_drafts[] | CertificateDraft | | |
| payload.literature_refs[] | LiteratureNode / NoveltyAssessment | | |
| payload.declared_reads[] | VerifierPrior / library digests | | |
| payload.free_text_notes | optional | Opt | |
| sealed_at | Seal time | Req | |
| prior_crp_digest | Prior sealed digest | Opt | Revisions |

B ignores: `session_id`, `batch_id`, `branch_id`, A version_ids (except projected content).

## B → A (feedback)

| Destination (A) | Source (B) | Notes |
|-----------------|------------|-------|
| SubmissionAttempt.receipt_ref | IntakeReceipt.receipt_digest | |
| SubmissionAttempt.b_intake_result | IntakeReceipt.status | |
| VerifierPrior.sealed_digest | crp_digest | |
| VerifierPrior.receipt_ref | receipt_digest | |
| VerifierPrior.export_ref | VerifierFeedbackExport.export_digest | |
| VerifierPrior.content_digest | export.content_digest | |
| (engines read prior content) | obligations, CX, audit, maturity | Non-authoritative |

ProofObligation objects are **not** written into A IR; only digests/status via export/prior content.
