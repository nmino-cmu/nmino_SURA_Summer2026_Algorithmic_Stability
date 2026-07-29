# 08d — Research Cycle Binding (Normative)

**Artifact ID:** `ART-08d`  
**Version:** `ARCH-0.3-REPAIR-ITER9.10`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-07b · ART-06b · ART-04c · ART-13b · ART-11b · ART-10b · ART-16b · ART-01 · ART-CRP  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative cycle Commit binding.

## Purpose

Commit-backed CycleRecord; hop freeze; S09 class↔CX↔target bind; major APPLY via I-AP-14. Caller `*_ok` forbidden.

`ponytail:` MathStable = hop+pins+demotion+CX discharge+optional Lean. Restore → Iter10.

---

## 1. Objects

```text
QuarantineLock
  quarantine_digest = H(q_id, chain_link, class, classifier_digest, frozen_at_event_seq)
  q_id
  chain_link                          # ART-01 chain segment token
  class
  classifier_digest
  frozen_at_event_seq

ExampleCard
  example_card_digest = H("ART08d.EC.v2", quarantine_digest, chain_link_intent,
                          body_schema_id, body_payload)
  quarantine_digest
  chain_link_intent                   # MUST = QuarantineLock.chain_link
  body_schema_id
  body_payload

FalsifierCard
  falsifier_card_digest = H("ART08d.FC.v2", quarantine_digest, chain_segment,
                            body_schema_id, body_payload)
  quarantine_digest
  chain_segment                       # MUST = QuarantineLock.chain_link
  body_schema_id
  body_payload

AttackAttempt
  class_id
  cx_digest

AttackLog
  attack_log_digest = H("ART08d.AL.v2", cycle_digest, sorted H(class_id, cx_digest))
  cycle_digest
  attempts[]                          # AttackAttempt; nonempty

CycleRecord
  cycle_digest = H("ART08d.CR.v3", quarantine_digest, primary_question_digest, target_claim_digest)
  quarantine_digest
  primary_question_digest
  target_claim_digest
  example_card_digest?                # outside identity; write-once
  falsifier_card_digest?
  phase
  attack_log_digest?
  audit_digest?
  lean_manifest_digest?
  closed
  cursor_event_seq
```

**I-CY-01..03:** quarantine frozen; ≤1 open cycle; cycle_digest immutable.

Genesis **MandatoryAttackClass[quarantine.class] → set of class_id** (closed package set).  
Genesis **ClassConstructSchema[class_id] → construct_schema_id** (closed; every mandatory class_id has a row).

---

## 2. Derived predicates

**DerivedHopChainOk(C):**  
- `example_card_digest` set; ExampleCard.quarantine_digest=C.quarantine_digest; `chain_link_intent = QuarantineLock.chain_link`  
- `falsifier_card_digest` set; FalsifierCard.quarantine_digest=C.quarantine_digest; `chain_segment = QuarantineLock.chain_link = ExampleCard.chain_link_intent`

**DerivedS09Ok(C):** AttackLog.cycle_digest=C.cycle_digest; let R=MandatoryAttackClass[C.quarantine.class];  
∀ class_id ∈ R: ∃ unique attempt with that class_id;  
∀ attempt: live Counterexample CX at cx_digest such that  
1. I-CX-01 hits `C.target_claim_digest`, and  
2. `CX.construct_schema_id = ClassConstructSchema[class_id].construct_schema_id`, and  
3. ART-07b **I-SCH-01 SchemaValid**(`ClassConstructSchema[class_id].construct_schema_id`, `CX.construct_payload`) holds  
else false. Unknown class_id ⇒ `UNKNOWN_ATTACK_CLASS`.
**DerivedS10Ok(C):** AuditRecord present; major PASS path ⇒ verdict=PASS ∧ I-BIND-01 for intent targeting `C.target_claim_digest`.

**IncompleteWave:** DemotionWave `cursor < len(work_items)`.

**DerivedMathStable(C):** DerivedHopChainOk ∧ DefPins match ∧ ¬IncompleteWave ∧ I-DW-21 ok for target ∧ (lean set ⇒ ≠ LEAN_STALE).

**DerivedCycleMilestoneOk(C, intent):** intent.target=`C.target_claim_digest`; S09+S10+hop+MathStable; phase≥S10; audit PASS.

---

## 3. Commands

**LOCK_CYCLE** (VERIFICATION_ORCHESTRATOR): `{ QuarantineLock, primary_question_digest, target_claim_digest }` → phase=S02.  
**DUAL.2:** `LOCK_CYCLE` is **optional**. Required only for ART-08d cycle-bound commands. Default verification after CRP intake is claim-direct (ART-CRP I-CRP-30). `FRONTIER_SCHEDULER` does not authorize LOCK_CYCLE on B. When locking post-CRP, `target_claim_digest` MUST ∈ IntakeReceipt.draft_claim_digests.

**BIND_CYCLE_CARD** (VERIFICATION_ORCHESTRATOR): `{ cycle_digest, ExampleCard | FalsifierCard }`  
- ExampleCard only at phase=S04 and `example_card_digest` currently ⊥ else `CARD_FROZEN`  
- FalsifierCard only at phase=S03 and `falsifier_card_digest` currently ⊥ else `CARD_FROZEN`  
- closed=false; quarantine+chain fields must match lock else `CARD_QUARANTINE_MISMATCH`

**RECORD_CYCLE_ATTACK_LOG** (VERIFICATION_ORCHESTRATOR): `{ cycle_digest, AttackLog }` at phase=S09; upsert; set attack_log_digest (replace allowed only while phase=S09 and before S10).

**RECORD_CYCLE_AUDIT** (VERIFICATION_ORCHESTRATOR): `{ cycle_digest, audit_digest }` at phase=S10; AuditRecord.intent.target_claim_digest=`C.target_claim_digest` else `CYCLE_CLAIM_MISMATCH`; set audit_digest write-once (`AUDIT_FROZEN` if already set).

**RECORD_CYCLE_LEAN** (VERIFICATION_ORCHESTRATOR): `{ cycle_digest, lean_manifest_digest }` at phase=S11; LeanManifest.claim_digest=`C.target_claim_digest`; write-once.

**ADVANCE_CYCLE:** `(phase,to_phase)` ∈ I-CY-10 + entry table.

**I-CY-10:**
```text
S02→S04
S04→S03
S03→S05
S05→S06
S06→S09
S09→S07 | S09→S10
S07→S08 | S07→S09
S08→S09
S10→S11 | S10→S12 | S10→S15
S11→S12
S12→S13 | S12→S15
S13→S14 | S13→S15
S14→S16
S15→S16 | S15→S02
```

| Enter | Require |
|-------|---------|
| S04 | — (BIND ExampleCard on/after entry before leaving) |
| S03 | example_card_digest set |
| S10 | DerivedS09Ok |
| S11 | DerivedS10Ok ∧ DerivedMathStable |
| S12 | phase∈{S10,S11} |
| S14 | ¬IncompleteWave |

**CLOSE_CYCLE:** closed=true at S16.

Caller booleans ⇒ `CALLER_BOOLEAN_FORBIDDEN`. Hard-stop ⇒ `HARD_STOP_ACTIVE`.

---

## 4–5. ART-13b / consumers

I-AP-14 + v6 `cycle_ok` (applied). ART-07b side tables include card/log objects with chain fields. ART-06b/04c commands as listed.

---

## 6. Failures / traces

`QUARANTINE_FROZEN | CYCLE_PHASE_REQUIRED | CYCLE_CLAIM_MISMATCH | ILLEGAL_TRANSITION | CALLER_BOOLEAN_FORBIDDEN | HARD_STOP_ACTIVE | DEMOTION_WAVE_OPEN | UNKNOWN_ATTACK_CLASS | CARD_QUARANTINE_MISMATCH | CARD_FROZEN | AUDIT_FROZEN`

```text
TRACE-9A  LOCK → S04 ExampleCard → S03 FalsifierCard → S09 AttackLog(class↔CX→target) → S10 audit → APPLY
TRACE-9B  S09 with CX not hitting target → DerivedS09Ok false
TRACE-9C  re-BIND ExampleCard → CARD_FROZEN
TRACE-9D  cycle_digest unchanged by BIND
```
