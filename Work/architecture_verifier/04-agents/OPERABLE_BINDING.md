# 04d — Operable Minimal Binding (Normative)

**Artifact ID:** `ART-04d`  
**Version:** `ARCH-0.3-REPAIR-DUAL.1`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-04c · ART-06b · ART-07b · ART-08d · ART-13b · ART-15 · ART-01 · ART-01V · ART-CRP  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative text for **System B** day-1 role/registry ceiling. Supersedes ART-04b. Discovery roster = ART-04e.

## Purpose

Hard day-1 **verification** role ceiling and registry write surface. Discovery engines are not on this roster.

`ponytail:` Permanent roster expansion still needs HUMAN ack (ART-15).

---

## 1. Day-1 roles (I-OM-01)

Mapped to ART-04c `role_id` (labels below are explanatory):

| # | role_id | Notes |
|---|---------|--------|
| 1 | VERIFICATION_ORCHESTRATOR | B intake + cycle + APPLY orchestration |
| 2 | PROOF_PROPOSER | ≠ certifier (I-RB-02); may appear on CRP-originated claims |
| 3 | PROOF_CERTIFIER | ≠ proposer |
| 4 | COUNTEREXAMPLE_ATTACKER | RECORD_COUNTEREXAMPLE |
| 5 | INTEGRATION_AUDITOR | |
| 6 | EIO | |
| 7 | HUMAN_GATE_OPERATOR | gates + human CRP submit |
| 8 | COMMITTER | serialization actor |

**Not on B day-1:** `FRONTIER_SCHEDULER`, discovery Mechanism Designer, Novelty Engine (see ART-04e).

**Conditional (I-OM-02)** — may appear in `roles_invoked[]` only with trigger:

| role_id | Trigger |
|---------|---------|
| LITERATURE_ANALYST | B audit of lit-cited CRP evidence (not A frontier) |
| LEAN_VERIFIER | RECORD_LEAN_MANIFEST / lean path |
| RESEARCH_SCOPE | challenge IN_CHAIN or classify ADJACENT/REFUSED |
| RESEARCH_DISCOVERY_ASSISTANT | never in B Commit roles_invoked (A-only author of CRP) |

Design-time Full-System Auditor is **not** a research-runtime role.

**I-OM-03:** `COUNTEREXAMPLE_ATTACKER` is a first-class ART-04c `role_id` authorized for `RECORD_COUNTEREXAMPLE`. Orchestrator remains alternatively authorized.

---

## 2. `I.RoleCeiling` (I-OM-10)

**day1_profile_digest (I-OM-08):**  
`day1_profile_digest = H("ART04d.DAY1.v1", sorted day-1 role_ids, sorted conditional role_ids)`.  
Live ceiling profile = `ControlState.role_ceiling_profile_digest` (ART-06b). At package genesis / IDENTITY_ADMIN Commit, that field MUST equal `day1_profile_digest` unless a `ROLE_EXPANSION` chain has installed a superseding profile digest (logged). Harness/default: equal to I-OM-08.

**Derived `roles_invoked` (I-OM-09):** At Commit validate, `roles_invoked = { RoleBinding.role_id of every principal that authorizes this command }`:
1. Always include the authenticated caller’s live binding `role_id`.  
2. Include every additional principal named in the command payload whose RoleBinding is required for success (e.g. certifier on ATTACH_CERTIFICATION, auditor on RECORD_AUDIT).  
3. Never accept a caller-supplied `roles_invoked[]` array (ignore if present).

**I.RoleCeiling:** Pass iff all hold:
1. Each role in `roles_invoked` is either (a) day-1, or (b) conditional with I-OM-02 trigger satisfied, or (c) covered by live EffectiveDecision(`ROLE_EXPANSION`, `H(day1_profile_digest, role_id)`) approve unexpired at Commit seq.  
2. Each included principal has a live ART-04c RoleBinding at Commit seq.  
3. On certify/propose pairs: PROOF_PROPOSER ≠ PROOF_CERTIFIER principals (I-RB-02).  
4. `command_kind=LOCK_CYCLE` ⇒ VERIFICATION_ORCHESTRATOR ∈ roles_invoked (not FRONTIER_SCHEDULER).  
5. `command_kind=SUBMIT_CANDIDATE_PACKAGE` ⇒ VERIFICATION_ORCHESTRATOR or HUMAN_GATE_OPERATOR ∈ roles_invoked.

Fail ⇒ `ROLE_CEILING`.

**I-OM-11:** Major APPLY ValidationPreimage `roles_invoked_ok` ⇔ I-OM-10 PASS for that Commit (Commit-derived only).

---

## 3. Day-1 registries (I-OM-20)

Logical names → ART-07b / ART-06b authoritative stores (all writes via `I.Commit` only):

| Logical | Authoritative |
|---------|---------------|
| definitions | DefinitionVersion / ActiveDefinitionHead |
| claims | Claim (+ bridges as Claims) |
| mechanisms | MechanismInstance |
| audits | AuditRecord (ART-11b) |
| counterexamples | Counterexample |
| frontier | Frontier / cycle locks (ART-08d) |
| quarantine | QuarantineLock |
| human_decisions | HumanDecision |
| lean_manifests | LeanManifest (ART-10b) |
| literature_claims | Claim + provenance (ART-11c); no opaque table |
| demotion_waves | DemotionWave (ART-16b) |
| checkpoints | CheckpointRecord (ART-17b) |
| control | ControlState (hard_stop, …) |

**Forbidden:** opaque literature/bridge views without EIO-readable digest provenance.  
**I-OM-21:** No direct registry poke — ART-06b I.Commit only.

---

## 4. FSM / appendix quarantine (I-OM-30)

| Artifact | Status under this binding |
|----------|---------------------------|
| ART-08 / 08b / 08c | Appendix descriptive; authority = ART-08d |
| ART-09 | Appendix; authority = ART-13b |
| ART-10 | Appendix; authority = ART-10b |
| ART-04b | PENDING_MIGRATION / descriptive; authority = this artifact |
| ART-18 critic roster | Design-time appendix; runtime credit = ART-04c I-MP-02 |

Residual caller `*_ok` / `hop_chain_ok` / `cert_kind` as authority ⇒ invalid (ART-06b / 13b / 08d).

---

## 5. Minimality collapses (I-OM-40)

Normative consumers MUST treat as **derived** (not separately stored authority):

- `source_subject_digest` when equal to Claim subject  
- Cached fingerprint copies when `claim_math_fingerprint` is recomputable  
- ART-04b “charter §IX” cite — **void**; acceptance package = ART-ASI file set  

Inert stubs without Commit writers remain non-authoritative.

---

## 6. Consumer deltas

| Artifact | Delta |
|----------|-------|
| ART-04c | role table includes conditional roles; I-OM-03 |
| ART-13b | roles_invoked_ok on major APPLY |
| ART-06b | RoleCeiling evaluated inside Commit |
| ART-08d | LOCK_CYCLE needs VERIFICATION_ORCHESTRATOR (DUAL.1) |
| ART-CRP | SUBMIT_CANDIDATE_PACKAGE on B day-1 |
| ART-04e | Discovery roster (no ResearchState Commit) |
| ART-04b | non-authoritative |
| ART-24 | I.RoleCeiling = I-OM-10 |

---

## 7. Failures / traces

`ROLE_CEILING | ROLE_EXPANSION_REQUIRED`

```text
TRACE-13A  LOCK_CYCLE without VERIFICATION_ORCHESTRATOR → ROLE_CEILING
TRACE-13B  FRONTIER_SCHEDULER on B LOCK_CYCLE → ROLE_CEILING (discovery ≠ B lock)
TRACE-13C  proposer=certifier → ROLE_CEILING
TRACE-13D  appendix ART-08 prose cannot authorize ADVANCE_CYCLE
TRACE-13E  SUBMIT_CANDIDATE_PACKAGE Phase A without mechanism → allowed
```
