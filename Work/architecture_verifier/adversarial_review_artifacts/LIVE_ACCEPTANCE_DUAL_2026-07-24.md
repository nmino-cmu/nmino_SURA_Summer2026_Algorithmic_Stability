# Dual-System Live Acceptance — Execution Report

**Document ID:** `LIVE-ACCEPT-DUAL-2026-07-24`  
**Date:** 2026-07-24  
**Harness:** `architecture/21-acceptance-tests/harness/live_acceptance_interpreter.py`  
**Authority:** ART-21b I-CF-02 ephemeral design interpreter (in-memory only; does not clear `IMPLEMENTATION_BLOCK`)  
**Artifacts:** `harness/live_runs/test1_phase_a.json`, `test2_phase_b.json`, `summary.json`

**Verdict:** **LIVE ACCEPTANCE PASSED**

---

## TEST 1 — PHASE A CHARACTERIZATION-ONLY

### INPUT PACKAGE
- `author_kind`: HUMAN  
- `profile` / `package_phase`: `PHASE_A_CHARACTERIZATION`  
- Operator: `argmax`  
- Definitions: argmax, bounded score perturbation (model ≠ MechanismInstance/Q_ψ), margin  
- Claim: if unique argmax and `m(F) > 2δ`, then `||ε||_∞ ≤ δ` ⇒ `argmax(F+ε)={λ*}`  
- Assumptions, proof sketch, tie-case warning, out-of-regime CX proposal  
- `mechanism_proposals`: `[]` — no MechanismInstance, Q_ψ, stability cert, inference bridge  

### VALIDATION RESULT
- `SUBMIT_CANDIDATE_PACKAGE` by `HUMAN_GATE_OPERATOR` → **SUCCESS**  
- Did **not** emit `MECHANISM_REQUIRED`  
- Profiles selected: `audit_profile_id=ART11b.CHAR`, `cx_profile_id=ART-12-CHAR`  

### CANONICAL OBJECTS CREATED
- Live `CandidateResearchPackage` (`intake_status=ACCEPTED_DRAFT`, `admissibility_state=ADMISSIBLE`)  
- `IntakeReceipt` (`ACCEPTED_DRAFT`)  
- Typed Claim `chain_segment=characterization`, maturity `OPEN`→ later `RESULT`  
- Dependency graph without mechanism edges  

### PROOF OBLIGATIONS CREATED
- ≥1 `PROOF` obligation, `blocks_promotion=true`, linked to CRP + claim (I-PO-01)  

### CX RESULTS
- ART-12-CHAR: `CX.CHAR.out_of_regime` (PARTIAL), `CX.CHAR.omit_ties` (PARTIAL)  
- No MechanismInstance demanded  

### AUDIT RESULTS
- `ART11b.CHAR`; **Q04 mode = NOT_APPLICABLE** (`NA`); **Q17 rule = characterization_facing** (`YES`)  
- Verdict **PASS**  

### PROMOTION RESULT
1. APPLY with OPEN obligations → **`OBLIGATION_UNRESOLVED`** (I-PO-03 / I-AP-PO)  
2. Discharge obligations via `PROOF_CERTIFIER`  
3. APPLY by `VERIFICATION_ORCHESTRATOR` → **SUCCESS** `OPEN→RESULT`  
4. `I.LibraryExport` → SUCCESS  

### FINAL STATUS
**CERTIFIED**

### EXECUTION TRACE
See `live_runs/test1_phase_a.json` → `EXECUTION_TRACE` / `EVENT_LOG`.  
All Commit-side roles ∈ {`HUMAN_GATE_OPERATOR`, `COUNTEREXAMPLE_ATTACKER`, `INTEGRATION_AUDITOR`, `PROOF_CERTIFIER`, `VERIFICATION_ORCHESTRATOR`}. No `RESEARCH_ORCHESTRATOR`.

### DEFECTS FOUND
None.

---

## TEST 2 — PHASE B STABILIZATION

### INPUT PACKAGE
- `author_kind`: `RESEARCH_DISCOVERY_ASSISTANT` + live binding `BIND_ASSIST_LIVE`  
- `profile`: `PHASE_B_STABILIZATION`  
- Mechanism: noisy-argmax `Q_ψ` (Gumbel β)  
- Claims: selection stability + utility-loss  
- Proof sketch, assumptions, CX candidates  

### VALIDATION RESULT
- Submitted by `VERIFICATION_ORCHESTRATOR` → **SUCCESS**  
- Profiles: `ART11b.BASE`, `ART-12`  
- Mechanism digests minted  

### CANONICAL OBJECTS CREATED
- CRP + claims + **MechanismInstance drafts**  

### PROOF OBLIGATIONS CREATED
- `PROOF` per claim **and** `CERT_ATTACH` mechanism-specific obligations (`blocks_promotion=true`)  

### CX RESULTS
- ART-12: `CX.tie_unstable` PARTIAL  

### AUDIT RESULTS
- BASE profile; Q04 = YES (mechanism present); Q17 = YES; PASS  

### PROMOTION RESULT
- APPLY → **`OBLIGATION_UNRESOLVED`** (obligations left OPEN — expected)  
- Final certification deferred: **REVISION_REQUIRED** (discharge not completed in this session)  

### BOUNDARY TEST
| Field | Value |
|-------|-------|
| Attempted command | `APPLY_PROMOTION` |
| Caller | `RESEARCH_DISCOVERY_ASSISTANT` |
| Rejection code | `ROLE_CEILING` |
| Invariant | ART-01D · ART-04e I-OD-02 · I-CRP-10 |
| Verifier state | **unchanged** (`state_unchanged: true`) |

Stale role `RESEARCH_ORCHESTRATOR` → `APPLY_PROMOTION` → **`UNAUTHORIZED_COMMAND`**.

Negative control: Phase B with empty `mechanism_proposals` → **`MECHANISM_REQUIRED`** (I-CRP-05).

### FINAL STATUS
**REVISION_REQUIRED** (blocking obligations unresolved; discovery cannot certify)

### DEFECTS FOUND
None.

---

## REGRESSION CHECKS

| # | Check | Result |
|---|-------|--------|
| 1 | Characterization intake without MechanismInstance | PASS |
| 2 | Phase B requires mechanism | PASS (`MECHANISM_REQUIRED` negative) |
| 3 | ProofObligations linked to CRP + claims | PASS |
| 4 | Unresolved blocking obligations block APPLY | PASS |
| 5 | Characterization Q04 NOT_APPLICABLE | PASS |
| 6 | Characterization Q17 characterization-facing | PASS |
| 7 | Discovery operational, no verifier authority | PASS (boundary) |
| 8 | State changes by authorized B principals only | PASS |
| 9 | Commit / CX / audit / promotion / library export | PASS |
| 10 | No `RESEARCH_ORCHESTRATOR` authority in trace | PASS |

---

## FINAL VERDICT

**LIVE ACCEPTANCE PASSED**
