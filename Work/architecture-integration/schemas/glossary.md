# Cross-system glossary (ART-INT)

**Authority:** ART-INT-00. Internal A/B terms may differ; this table owns **boundary** meaning.

| Term | System A | System B | Mapping / notes | Definition owner |
|------|----------|----------|-----------------|------------------|
| candidate | PortfolioMember / IR draft object | — | Becomes CRP claims/mechs after pack | A-02; wire: ART-INT |
| proposition | Informal statement in drafts | Claim assertion payload | Wire as claim fields | ART-07b / ART-CRP |
| claim | TheoremCandidate / ConjectureCandidate | ART-07b Claim | Draft until intake | ART-CRP payload |
| theorem | TheoremCandidate (ATP) | Claim with maturity RESULT (post-cert) | A never asserts B RESULT | ART-13b |
| conjecture | ConjectureCandidate | Maturity CONJECTURE | | ART-13b |
| characterization | Phase A intent / chain_segment | `chain_segment=characterization` | | ART-07b |
| mechanism | MechanismProposal | MechanismInstance / mechanism_proposals[] | | ART-CRP |
| optimization operator | OPERATOR_ANALYZER output | SelectionOperator | Not a mechanism (I-CRP-03) | ART-07b |
| perturbation | Q_ψ / mechanism proposal | MechanismInstance joint law | Optional Phase A | ART-CRP I-CRP-02 |
| perturbation_mechanism_id | ExampleCard field (legacy A) | **Not a B field** | Maps to mechanism_proposals[].local_id or omit | ART-INT profile-map |
| structural / instability quantity | STRUCTURAL_QUANTITY IR | Claim payload / characterization | | ART-INT profile-map |
| proof obligation | hint only | ProofObligation object | Minted at intake I-PO-01 | ART-07b |
| verification target | sealed package claims | draft_claim_digests | | ART-CRP |
| verification result | — | audit verdict / CX / maturity | See status-map | ART-INT status-map |
| package | DraftCRP / SealedCRPSnapshot | CandidateResearchPackage | sealed_digest≡crp_digest | ART-INT |
| CRP | Draft or sealed A package | CandidateResearchPackage | | ART-CRP |
| DraftCRP | Unsealed packager output | — | Not submittable | ART-INT crp-wire |
| SealedCRPSnapshot | Immutable sealed bytes | — | Equals wire CRP | ART-INT crp-wire |
| CandidateResearchPackage | Wire target | Live + sealed object | | ART-CRP |
| SubmissionBatch | A workflow multi-package wave | **Does not exist** | Fan-out N submits | ART-A-06 / ART-INT |
| SubmissionAttempt | Per-package attempt record | — | | A-03 |
| SubmissionEnvelope | Wire wrapper for one CRP | Command payload | | ART-INT crp-wire |
| intake | — | SUBMIT path | | ART-CRP |
| submission | I.DiscoverySubmit | SUBMIT_CANDIDATE_PACKAGE | Alias | ART-24 |
| receipt | receipt_ref | IntakeReceipt | | ART-CRP |
| feedback | VerifierPrior content | VerifierFeedbackExport | | ART-INT |
| prior / VerifierPrior | A IR prior | — | Minted from export | A-04 |
| branch | Discovery Branch | — | A-local | A-02 |
| portfolio member | PortfolioMember | — | One draft path | A-02 |
| package member | Batch member | One CRP | | ART-INT |
| phase | A profile_hint intent | CRP profile / package_phase | | ART-INT profile-map |
| profile | profile_hint | CRP profile | | ART-INT profile-map |
| audit status | — | AuditRecord.verdict | PASS/FAIL/… | ART-11b |
| PASS / PARTIAL / FAIL | — | Audit PASS/FAIL; CX PARTIAL; maturity PARTIAL_RESULT | **Not interchangeable** | ART-INT status-map |
| version / revision | ArtifactVersion.version_id | schema_version / prior_crp_digest | | ART-INT id-contract |
| immutable artifact | version payload | sealed CRP / receipt | | A-02 / ART-CRP |
| lifecycle metadata | ArtifactLifecycleRecord | intake_status | Must not change math digest | A-02 |
| provenance | parents[] / declared_reads | source_provenance | | ART-INT |
| digest | version_id / sealed_digest | crp_digest / claim_digest | ART21b | ART-21b |
| identifier | see id-contract | see id-contract | | ART-INT id-contract |
| promotion / demotion | Forbidden on A | ART-13b / ART-16b | | B only |
| Soft Attack | A IR drafts | Forbidden as B CX | | A-02 I-A02-07 |
