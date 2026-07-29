# Dual-System Separation — Conformance Re-Audit (post DUAL.2 repair)

**Document ID:** `AUDIT-DUAL-CONFORM-2026-07-24-R2`  
**Date:** 2026-07-24  
**Prior:** `AUDIT-DUAL-CONFORM-2026-07-24` = REFACTOR PARTIALLY COMPLETE (7/4/1)  
**Scope:** Implemented architecture after targeted repairs 1–6  
**Method:** Same 12 checks; evidence-only; no redesign  
**Verdict:** **REFACTOR COMPLETE**

Score: **12 PASS · 0 PARTIAL · 0 FAIL**

---

### 1. Verification Architecture rechartered verification-only
- **STATUS:** PASS
- **EVIDENCE:** ART-01V `CHARTER_VERIFICATION.md` unchanged mission/non-goals; ART-ASI.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 2. Discovery Assistant separate upstream
- **STATUS:** PASS
- **EVIDENCE:** ART-01D; ART-04e; `architecture-discovery/` including `engines/`.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 3. Discovery capabilities preserved outside verifier
- **STATUS:** PASS
- **EVIDENCE:** Owned modules: `architecture-discovery/engines/NOVELTY_ENGINE.md` (ART-A-NOV), `AUTOMATIC_THEOREM_PROPOSAL.md` (ART-A-ATP), `MECHANISM_DESIGNER.md` (ART-A-MECH), `CONJECTURE_PROPOSAL.md` (ART-A-CONJ); plus ART-08/08b/08c. Each specifies purpose/IO/ownership/permitted/prohibited/CRP/verifier relations. Generation preserved; not deleted.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 4. Discovery excluded from verify/certify/promote/demote/audit
- **STATUS:** PASS
- **EVIDENCE:** B command authors use `VERIFICATION_ORCHESTRATOR` only (ART-08d, 11b, 13b, 16b, 10b). ART-04c has no `RESEARCH_ORCHESTRATOR` alias. ART-A-* prohibited lists ban certify/PO-close/promote/demote/CX/Control/audit. `AGENT_ROLES.md` / visual/07 show Frontier forbidden from LOCK_CYCLE.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 5. First-class CandidateResearchPackage
- **STATUS:** PASS
- **EVIDENCE:** ART-CRP + ART-07b §10A registers `CandidateResearchPackage` and `IntakeReceipt` with identity, schema_version, author_kind, package_phase, admissibility_state, provenance, contained refs, intake_status, commit_event_seq, emitted_obligation_digests. Stub claim removed. Fixtures `CF-CRP-REG`, `CF-CRP-HUMAN`, `CF-CRP-ASSIST`.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 6. CRP principals HUMAN + RESEARCH_DISCOVERY_ASSISTANT
- **STATUS:** PASS
- **EVIDENCE:** ART-CRP / ART-07b I-CRP-OBJ-02; `CF-CRP-HUMAN`, `CF-CRP-ASSIST`, `CF-CRP-C`.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 7. Characterization-only without mechanism/Qψ/stability/bridge
- **STATUS:** PASS
- **EVIDENCE:** I-CRP-02; ART-07b characterization; `CF-CRP-A`/`CF-CRP-HUMAN`; ART-11b-CHAR I-AR-CHAR-01; discovery ExampleCard mechanism optional for Phase A.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 8. Complete external intake → library pipeline
- **STATUS:** PASS
- **EVIDENCE:** ART-CRP §4–5 + ART-07b I-PO-01..05: CRP → Claims → ProofObligations → tracking → discharge → I-AP-PO promotion gate. CX/audit/Lean/promo/demotion via existing B. `LOCK_CYCLE` normative as **optional** (I-CRP-30/31); claim-direct default. `CF-PO-BLOCK` → `OBLIGATION_UNRESOLVED`.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 9. Phase A characterization claim types first-class
- **STATUS:** PASS
- **EVIDENCE:** Unchanged ART-07b/ART-01/ART-CRP profile enum (+ `BRIDGE_ONLY`).
- **DEFECT:** —
- **REQUIRED FIX:** —

### 10. CX/audit/integration profiles for characterization-only
- **STATUS:** PASS
- **EVIDENCE:** `ART-12-CHAR` `CHARACTERIZATION_CX_PROFILE.md` (13 CHAR classes). `ART-11b-CHAR` + ART-11b §0 routing (`PHASE_A`/`PHASE_B`/`BRIDGE_ONLY`/`MIXED`). Q04 NOT_APPLICABLE under CHAR; Q17 characterization-facing. Fixtures `CF-CHAR-CX-OK`, `CF-CHAR-CX-NEG`.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 11. Verification infrastructure preserved
- **STATUS:** PASS
- **EVIDENCE:** ART-ASI ACTIVE_NORMATIVE for 06b, 07b, 07c, 08d, 10b, 11b, 13b, 16b — present.
- **DEFECT:** —
- **REQUIRED FIX:** —

### 12. No mandatory discovery cycle to begin verification
- **STATUS:** PASS
- **EVIDENCE:** Human CRP path; I-CRP-30 claim-direct; no A FSM prerequisite.
- **DEFECT:** —
- **REQUIRED FIX:** —

---

## Regression checks

| # | Check | Result |
|---|-------|--------|
| 1 | Human characterization CRP intake | PASS (`CF-CRP-HUMAN` / `CF-CRP-A`) |
| 2 | Assistant characterization CRP intake | PASS (`CF-CRP-ASSIST`) |
| 3 | Stabilization still requires mechanism | PASS (`CF-CRP-B`) |
| 4 | Discovery engines exist and can generate packages | PASS (ART-A-* + ART-08*) |
| 5 | Discovery cannot certify/promote/demote/audit/close obligations | PASS (ART-A-* prohibited + ART-04e I-OD-02) |
| 6 | B kernel intact | PASS (ART-ASI) |

---

## Final verdict

**REFACTOR COMPLETE**
