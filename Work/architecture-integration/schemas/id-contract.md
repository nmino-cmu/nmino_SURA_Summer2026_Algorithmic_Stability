# Identifier contract (ART-INT)

**Authority:** ART-INT-00. Digests use ART-21b SHA-256 unless noted.

| ID | Producer | Consumer | Scope | Mutable? | Wire format | Cross-boundary |
|----|----------|----------|-------|----------|-------------|----------------|
| `session_id` | A Orch | A only | Session | No | opaque string/digest | Not sent to B |
| `branch_id` | A DISCOVERY_IR | A | Session | No | opaque | Not sent |
| `artifact_id` / `lineage_id` | A class owner | A | Session lineage | No | opaque | Not sent |
| `version_id` | A class owner | A | Content-addressed | No | hex digest | Not sent (except via payload projection) |
| `candidate_id` / `member_id` | A Portfolio | A | Session | No | opaque | Not sent |
| `DraftCRP.version_id` | Packager | Gate3 / seal | Session | No | digest | Referenced in seal_set only |
| `sealed_snapshot_version_id` | Assistant | Attempts | Session | No | digest | A-local |
| `sealed_digest` / `crp_digest` | Seal (= ART-CRP hash) | A+B | Global content | No | hex SHA-256 | **Copied**; identity key |
| `batch_id` | A Orch | A | Session | No | opaque | **Not sent to B** |
| `attempt_id` | A Orch | A | Session | No | opaque | Not sent |
| `logical_submission_id` | A Orch | A | = sealed_digest recommended | No | digest | Align with crp_digest |
| `idempotency_key` | A | A+B Commit | = crp_digest | No | hex | Carried in attempt; B keys on crp_digest |
| `submission_batch_id` | — | — | — | — | — | **Alias of batch_id; A-only** |
| `author_principal_digest` | A/Human identity | B | Global | No | hex | In CRP envelope |
| `author_binding_digest` | B RoleBinding / A cites | B | Live binding | No | hex | Required if ASSISTANT |
| `math_scope_pin_digest` | Shared Area-1 pin | A+B | Global pin | No | hex | Required in CRP |
| `intake_receipt_id` / `receipt_digest` | B | A+B | Global | No | hex | A stores `receipt_ref` |
| `proof_obligation_id` / `obligation_digest` | B | B; A via feedback | ResearchState | Status mutable | hex | Export only |
| `verification_run_id` | B (optional) | Feedback | Per run | No | opaque/digest | In FeedbackExport |
| `feedback_export_id` / `export_digest` | B | A | Global | No | hex | `export_ref` on prior |
| `claim_digest` | B DeriveEffects | B; A read | ResearchState | No | hex | In receipt/export |
| `mechanism_digest` | B after intake | B | ResearchState | No | hex | |
| `perturbation_mechanism_id` | A ExampleCard only | Packager | Session | No | opaque | **Maps to** mechanism_proposals entry or omit; never a B registry key |
| `prior_crp_digest` | A on revision | B | Global | No | hex | Optional lineage |
| `schema_version` | Encoder | Decoder | Object | No | string | Required |

**I-INT-ID-01:** Never treat `batch_id` as global or as B key.  
**I-INT-ID-02:** `sealed_digest ≡ crp_digest`.  
**I-INT-ID-03:** Unstable display names are not identifiers.
