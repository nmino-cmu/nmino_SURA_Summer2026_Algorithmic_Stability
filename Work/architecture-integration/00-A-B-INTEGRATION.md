# ART-INT-00 — System A ↔ System B Integration Specification

**Artifact ID:** `ART-INT-00`  
**Version:** `ARCH-0.3-REPAIR-INT.1`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Owner:** Cross-system interface (neither A nor B internals)  
**Home:** `architecture-integration/`  
**Depends on (read-only):** ART-A-00…A-08 · ART-CRP · ART-07b §10A/10B · ART-21b · ART-01D · ART-01V · ART-06b · ART-24  
**Does not redefine:** Discovery FSM; Verification phases; Soft Attack; Pareto; B DeriveEffects algorithms

## Purpose

**Sole authoritative owner** of the A↔B interface: terminology mapping, identifiers, schemas at the boundary, serialization, submission protocol, feedback protocol, authority at the boundary, version negotiation, trust boundary, and integration conformance.

Internal behavior remains owned by System A (`architecture-discovery/`) and System B (`architecture_verifier/`).

## Precedence (cross-system)

1. System B internals — Verification Architecture owns B behavior (ART-01V, ART-06b, ART-07b/c, ART-08d, ART-11b, ART-12*, ART-13b, …).  
2. **ART-CRP** — CRP object schema and B intake DeriveEffects (sole B mathematical intake).  
3. ART-A-00 — System A topology / hard boundaries.  
4. ART-A-02 — System A ownership.  
5. ART-A-03 — Discovery lifecycle / gates timing.  
6. ART-A-04 — Discovery IR field schemas (A-local).  
7. ART-A-05 — Discovery invocation execution.  
8. ART-A-06 — A projection IR→DraftCRP and A-local SubmissionBatch workflow.  
9. ART-A-07 — Discovery persistence / recovery.  
10. ART-A-08 — Discovery conformance enumeration.  
11. **This document (ART-INT-00) + `architecture-integration/schemas/*`** — interface semantics, wire mapping, feedback export, cross-system IDs/status/profiles/notation. **May not override** A or B internal authority.  
12. Readiness matrices, visual companions, design companions — **non-authoritative** derived references.

**Conflict rule:** If A or B prose restates an interface rule differently from ART-INT-00, ART-INT-00 wins for the interface; amend the duplicate to a reference.

## Normative schema appendices (this package)

| File | Owns |
|------|------|
| [schemas/glossary.md](schemas/glossary.md) | Cross-system term mapping |
| [schemas/notation.md](schemas/notation.md) | Interface-facing mathematical notation |
| [schemas/id-contract.md](schemas/id-contract.md) | Identifier producer/consumer/scope |
| [schemas/crp-wire.schema.md](schemas/crp-wire.schema.md) | DraftCRP · SealedCRPSnapshot · SubmissionEnvelope · wire CRP |
| [schemas/feedback-export.schema.md](schemas/feedback-export.schema.md) | VerifierFeedbackExport |
| [schemas/status-map.md](schemas/status-map.md) | Status taxonomy crosswalk |
| [schemas/profile-map.md](schemas/profile-map.md) | Candidate type → CRP profile |
| [schemas/field-map.md](schemas/field-map.md) | Field-level A→B / B→A map |
| [TRACE_MATRIX.md](TRACE_MATRIX.md) | Required E2E traces |
| [AUDIT_LOG.md](AUDIT_LOG.md) | Defect / repair log |
| [FINAL_AUDIT.md](FINAL_AUDIT.md) | Integration audit verdict |

---

## 1. Systems and sole write path

| System | Role |
|--------|------|
| **A** Research Discovery Assistant | Invent, schedule, pack, seal; session-local IR |
| **B** Verification Architecture | Intake, mint obligations, verify, certify, govern |

**I-INT-01 Sole A→B mutation:** Sealed CRP bytes only, via `I.DiscoverySubmit` → `SUBMIT_CANDIDATE_PACKAGE` → `I.Commit`.  
**I-INT-02 B→A:** Read-only (`IntakeReceipt`, `I.DiscoveryStatus`, `I.LibraryExport`, `VerifierFeedbackExport`). B never mutates Discovery IR.  
**I-INT-03** Soft Attack ≠ B `RECORD_COUNTEREXAMPLE`. Intake ≠ mathematical truth (ART-A-02 I-A02-12).

---

## 2. Batch vs package cardinality (normative)

| Concept | Cardinality | Owner |
|---------|-------------|-------|
| `SubmissionBatch` | A-workflow only; one per Gate-3 seal wave | ART-A-06 |
| Sealed package / CRP | One `crp_digest` per sealed member | ART-CRP + this doc |
| B Commit | **Exactly one** `SUBMIT_CANDIDATE_PACKAGE` per sealed package | ART-CRP |
| `IntakeReceipt` | **One per package** (per `crp_digest`) | ART-CRP |
| ProofObligation mint | Per draft claim of that package | ART-07b I-PO-01 |
| Feedback export | **Per package** (optionally filtered library export multi-object) | This doc |
| Partial batch | Allowed on A; B unaware of `batch_id` | ART-A-06 M-A06-BATCH-* |

**I-INT-10:** A MUST fan-out a batch into N independent submits. B MUST NOT require or store `batch_id`.

---

## 3. Submission protocol (interface)

```text
IR → DraftCRP → Gate3 seal_set → SealedCRPSnapshot
  → SubmissionEnvelope (wire)
  → I.DiscoverySubmit
  → SUBMIT_CANDIDATE_PACKAGE
  → IntakeReceipt
```

| Step | Owner | Input | Output | Failure |
|------|-------|-------|--------|---------|
| Compile | CRP_PACKAGER | coherent Branch | DraftCRP \| CompileError | CompileError |
| Gate 3 | DISCOVERY_ORCHESTRATOR + Human | drafts/errors | seal_set | reject/revise |
| Seal | RESEARCH_DISCOVERY_ASSISTANT | DraftCRP.version_id ∈ seal_set | SealedCRPSnapshot | illegal if unsealed/CompileError |
| Envelope | Assistant (seal) | SealedCRPSnapshot | SubmissionEnvelope = ART-CRP object bytes | schema reject |
| Submit | Assistant executes; Orch owns attempt records | Envelope | transport OK/FAIL | retry per M-A06-BATCH-04 |
| Intake | VERIFICATION_ORCHESTRATOR or HUMAN_GATE_OPERATOR | Envelope via Commit | IntakeReceipt | REJECTED + reason_codes |

**I-INT-20:** `sealed_digest` **≡** `crp_digest` (same SHA-256 over ART-CRP identity fields under ART21b.CANON.v1).  
**I-INT-21 Idempotency:** `idempotency_key = sealed_digest = crp_digest`. Replaying identical envelope → B returns same logical intake outcome (ACCEPTED_DRAFT replay or equivalent) without double-minting distinct claim digests; content change ⇒ different digest ⇒ new submission.  
**I-INT-22:** Unsealed DraftCRP MUST NOT be submitted.  
**I-INT-23:** Post-Gate3 mutation of sealed payload forbidden; material change ⇒ new DraftCRP → new Gate 3 → new seal.

Full field schemas: [schemas/crp-wire.schema.md](schemas/crp-wire.schema.md).

---

## 4. Feedback protocol (interface)

```text
B verification artifacts → VerifierFeedbackExport
  → I.LibraryExport / status / receipt (carriers)
  → A DISCOVERY_ORCHESTRATOR mints VerifierPrior (open session)
```

**I-INT-30:** `VerifierFeedbackExport` is the **sole** normative B→A feedback object schema (this package).  
**I-INT-31:** `I.LibraryExport` / `I.DiscoveryStatus` / raw `IntakeReceipt` are **carriers**; when used as feedback, their content MUST be interpretable as or wrapped into `VerifierFeedbackExport`.  
**I-INT-32:** Only DISCOVERY_ORCHESTRATOR mints `VerifierPrior`. Engines read priors; never rewrite B.  
**I-INT-33:** Active prior into CLOSED session forbidden (ART-A-04 I-A04-PRIOR-*). Late feedback → new session.  
**I-INT-34:** Feedback is **non-authoritative** w.r.t. Discovery mathematical truth unless A’s own rules later elevate content into new IR claims (new authorship).

Schema: [schemas/feedback-export.schema.md](schemas/feedback-export.schema.md).

---

## 5. Serialization (canonical wire)

**I-INT-40:** Boundary bytes use ART-21b:

- UTF-8  
- `canonicalization_version = "ART21b.CANON.v1"`  
- SHA-256 digests; hex lowercase when embedded  
- Object keys sorted lexicographically for digests  
- Absent optional ⇒ key omitted (never `null`)  
- Timestamps: ISO-8601 UTC (`…Z`)  
- Enums: `UPPER_SNAKE_CASE` strings  
- Field names: `snake_case`  
- Math text: Unicode NFC; LaTeX allowed in typed string fields flagged `math_text`; digest over NFC UTF-8  

Owner of hash algorithm: ART-21b. Owner of CRP identity hash domain tags: ART-CRP. Owner of binding A seals to this wire: this document.

---

## 6. Authority matrix (boundary only)

| Action | Who |
|--------|-----|
| Create DraftCRP | CRP_PACKAGER |
| Authorize seal_set | Human Gate 3 (via Orch GateRecord) |
| Seal SealedCRPSnapshot | RESEARCH_DISCOVERY_ASSISTANT |
| Mint SubmissionBatch / Attempt | DISCOVERY_ORCHESTRATOR |
| Execute I.DiscoverySubmit | RESEARCH_DISCOVERY_ASSISTANT |
| Mint IntakeReceipt / ProofObligation | B Commit DeriveEffects (VERIFICATION_ORCHESTRATOR or HUMAN_GATE_OPERATOR issues Command) |
| Select verification profile | Derived from CRP `profile` (ART-11b §0); not chosen by A post-seal |
| PASS/FAIL audit / CX / APPLY | System B only |
| Emit VerifierFeedbackExport | System B (read APIs) |
| Mint VerifierPrior | DISCOVERY_ORCHESTRATOR |
| Mutate sealed CRP content | **Nobody** |

---

## 7. Version negotiation

**I-INT-50:** Wire objects carry `schema_version` (`ARTCRP.v1`, `ARTINT.FB.v1`, …).  
**I-INT-51:** Unsupported `schema_version` ⇒ explicit reject (`UNSUPPORTED_SCHEMA_VERSION`); **no silent coercion**.  
**I-INT-52:** Legacy ART-08 packages: B `LEGACY_CYCLE_INTAKE` (I-CRP-20) only; A new sessions use ART-A-03 + this wire.  
**I-INT-53:** Revising a rejected package ⇒ new `prior_crp_digest` link + new `crp_digest`.

---

## 8. Trust boundary

**I-INT-60:** Validate all inbound envelopes (schema, digests, author binding).  
**I-INT-61:** Reject forged `receipt_ref` / `export_ref` that do not hash-verify against B EventLog / export content.  
**I-INT-62:** Replay with altered content fails digest equality (I-INT-21).  
**I-INT-63:** Feedback import MUST bind `sealed_digest` and/or `receipt_ref` to the cited package (I-A04-PRIOR-01). Wrong-package import forbidden.  
**I-INT-64:** Engines MUST NOT call `I.DiscoverySubmit` or seal; only Assistant seals/submits (control: Orch).

---

## 9. Illegal interface operations

- Submit unsealed DraftCRP  
- B mutates Discovery IR  
- A APPLY / RECORD_COUNTEREXAMPLE / LOCK_CYCLE on B  
- Feedback auto-rewrites IR claims without new authorship versions  
- Dual conflicting interface rule owners  
- Silent schema coercion  
- Resubmit ACCEPTED_DRAFT member in partial batch retry (M-A06-BATCH-04)

---

## 10. Integration conformance (summary)

Cases `CF-INT-*` in [TRACE_MATRIX.md](TRACE_MATRIX.md). Cross-ref existing `CF-CRP-*` / `CF-A-*`.

## Changelog

2026-07-25: Initial ART-INT-00 — repairs BLOCKING-0 (no integration owner).
