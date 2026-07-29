# 11b — Audit Policy and Intent-Bound Audit Records (Normative)

**Artifact ID:** `ART-11b`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-07b · ART-07c · ART-06b · ART-04c · ART-13b · ART-01 · ART-CRP · ART-11b-CHAR  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative text for ART-11b baseline questions; characterization overrides = ART-11b-CHAR.

## Purpose

Intent-bound audits for major-milestone APPLY. Closes `B-AUDIT-BIND-01`.

`ponytail:` Q02–Q03, Q07–Q10, Q14–Q17 YES = INTEGRATION_AUDITOR attestation + structural bind. Q04 = ART-11c I-Q04-01 when applicable (not attestation-alone). Machine-checked: Q01, Q11. Full prompt evaluators → Iter12.

### §0 Audit profile routing (DUAL.2)

`RECORD_AUDIT` payload MUST include `audit_profile_id` and `crp_digest?` when the target claim originated from CRP intake.

| CRP profile | audit_profile_id | Authority |
|-------------|------------------|-----------|
| `PHASE_A_CHARACTERIZATION` | `ART11b.CHAR` | ART-11b-CHAR |
| `PHASE_B_STABILIZATION` | `ART11b.BASE` | this file |
| `BRIDGE_ONLY` | `ART11b.BRIDGE` | this file + IF_INFERENCE |
| `MIXED` | `ART11b.MIXED` | per-claim CHAR vs BASE |
| `OBLIGATION_ONLY` | `ART11b.CHAR` | ART-11b-CHAR |
| no CRP (legacy) | `ART11b.BASE` | this file |

---

## 1. Answer + mandatory questions (13)

```text
Answer
  question_id
  response             # YES | NO | NA | UNKNOWN
  evidence_digests[]
  object_class?        # Q01 only; MUST equal claim.subject_ref.object_class ∈ {INDEX, POLICY, OTHER}
```

`answer_payload_digest = H(question_id, response, object_class_or_⊥, evidence_digests_sorted)`.

| ID | mode | prompt_text |
|----|------|-------------|
| Q01 | IF_OTHER_OBJECT | object_class = live SubjectRef; OTHER needs HD |
| Q02 | ALWAYS | Dataset relation pin matches DEF.neighbor |
| Q03 | ALWAYS | Probability law identified |
| Q04 | ALWAYS* | Perturbation DD-independent or sub-mechanism certified (ART-11c I-Q04-01) |
| Q07 | IF_COMPOSED | Composition parameters updated by registered rule |
| Q08 | ALWAYS | Induced policy within scope or INDEX-only |
| Q09 | ALWAYS | Feasibility unchanged or typed |
| Q10 | ALWAYS | Inferential target unchanged or typed |
| Q11 | IF_INFERENCE | BridgeApplicabilityEvaluate = APPLICABLE |
| Q14 | ALWAYS | No theorem assumptions newly violated |
| Q15 | IF_UTILITY | Utility comparator matches utility_kind |
| Q16 | ALWAYS | No new instability or logged |
| Q17 | PASS_REQUIRED | Advances applicable chain (see below); NO ⇒ IRRELEVANT not PASS |

\* **Q04 under `ART11b.CHAR` / characterization-only:** mode = **NOT_APPLICABLE** unless a MechanismInstance (or CRP mechanism_proposal bound to the claim) is present (ART-11b-CHAR).  
\* **Q17 under `ART11b.CHAR`:** YES iff advances **characterization-facing** chain (ART-01) or discharges blocking ProofObligation — **not** mechanism→stability→inference.

Applicability: IF_OTHER_OBJECT ⇔ live object_class=OTHER; IF_COMPOSED ⇔ chain_segment=composition; IF_INFERENCE ⇔ ART-01 inference_facing; IF_UTILITY ⇔ ∃ UTILITY_CONSTRAINT dep; PASS_REQUIRED = always answered.  
NOT_APPLICABLE answers use `response=NA` and do not block PASS when mode says NA.  
Omitted (Iter7/9/11): postprocess, adaptive, selprob, lit, hop.

**I-AR-05:** `answers[]` is a bijection from these 13 question_ids → Answer (no missing, no duplicate question_id).

---

## 2. Side tables + commands

```text
DisconfirmLog
  disconfirm_digest = H("ART11b.DL.v6", claim_digest, attempts_canonical)
  claim_digest
  attempts[]   # nonempty; channel ∈ {CX,LEAN_NEGATION,LIT_DISCONFIRM,OTHER}; result_digest required
  attempts_canonical = H(sorted H(channel, result_digest, refs_sorted))

AuditRecord
  audit_digest = H("ART11b.AR.v8", intent_digest, sorted answer_payload_digests, verdict,
                   record_pre_state_head_digest)
  intent_digest
  answers[]
  verdict   # PASS | FAIL | IRRELEVANT | ESCALATE_HUMAN
```

`record_pre_state_head_digest` = Commit pre_state_head at RECORD_AUDIT (hashed into identity; not a free caller field). Re-RECORD at a new head ⇒ new audit_digest ⇒ new intro event.

**RECORD_DISCONFIRM** (VERIFICATION_ORCHESTRATOR): `{claim_digest, attempts[]}` → upsert DisconfirmLog.  
**RECORD_AUDIT** (INTEGRATION_AUDITOR): `{promotion_intent, answers[], verdict}` → intent from payload; I-AR-03…05; upsert AuditRecord.

---

## 3. EvidenceKindResolver

First match: DISCONFIRM_LOG table; else Claim with UTILITY_ prefix or cited by UTILITY_CONSTRAINT → UTILITY; else Claim chain_segment=bridge → BRIDGE; else CERT/PROOF/DISCHARGE/MECHANISM/CX/HUMAN_DECISION tables; else Claim → CLAIM; else UNKNOWN.

(UTILITY before BRIDGE so utility-constrained bridge Claims still type as UTILITY for Q15.)

---

## 4. CommitTypedBind

`target = intent.target_claim_digest`.

Exempt from per-Q allow: digests with kind DISCONFIRM_LOG (I-DL-02 only).

| Q | rule |
|---|------|
| Q01 | ∃ CLAIM=target; object_class=live SubjectRef; if OTHER: also ∃ HUMAN_DECISION digest that is EffectiveDecision approve gate∈{SELECTED_OBJECT_CHANGE,SCOPE_CHANGE} target∈{target,intent_digest}. Non-exempt digests ∈ {CLAIM, HUMAN_DECISION} only. |
| Q02–Q04,Q07–Q10,Q14,Q16,Q17 | each non-exempt digest kind∈ allow (CLAIM; +MECHANISM Q03; +CERT/PROOF Q04; +BRIDGE Q09/Q10; +DISCHARGE Q14; +CX Q16) |
| Q11 | applicable only if target Claim satisfies I-INF-CLAIM-01 preconditions; let B=unique BRIDGE dep; evidence contains d=B; BridgeApplicabilityEvaluate(B, source/target/use_class from I-INF-CLAIM-01, ctx_digest=pre_state_head_digest)=APPLICABLE. If inference_facing but not I-INF-CLAIM-01 Claim ⇒ AUDIT_FAIL (cannot PASS). |
| Q15 | each non-exempt digest satisfies UTILITY kind (resolver) |

---

## 5. Independence + PASS

**DerivedAuditor(A)** / **DerivedProducer(D):** introducing RECORD_* caller_principal.  
**CanonicalDisconfirm(A, intent):** DISCONFIRM_LOG in evidence union with claim_digest=target, max intro event_seq.  
**I-DL-02:** D exists; IndependenceCheck(DerivedProducer(D), DerivedAuditor(A), SAME_HUMAN)=DISJOINT; MODEL_RUNTIME ⇒ also SAME_MODEL_FAMILY; UNKNOWN_ATOM ⇒ AUDIT_INDEPENDENCE.  
**I-AR-04:** ∀ p ∈ DerivedBasisProposers(intent,S): IndependenceCheck(DerivedAuditor(A), p, SAME_HUMAN)=DISJOINT (+ model family).

**I-AR-03 PASS:** (1) applicable ALWAYS/IF_* ⇒ YES (NA iff not applicable) (2) Q17=YES (3) CommitTypedBind all non-NA (4) I-DL-02 (5) I-AR-04 + I-AR-05. Else reject PASS.

---

## 6. I-BIND-01

Non-noop APPLY only (I-AP-00 skips).  
Let `A*` = AuditRecord with `intent_digest=intent_digest(PI)` and **maximum introducing event_seq** (any verdict). Require `A*.verdict=PASS`; if latest is FAIL/IRRELEVANT/ESCALATE_HUMAN or missing ⇒ `AUDIT_REQUIRED` / `AUDIT_FAIL` (a later non-PASS supersedes prior PASS).  
Freshness since intro(A*): no later Effects upserting ResearchMaturityRecord[target]; ProofAttachment/CertificationRecord/DisconfirmLog for target; EioVeto[target]; EioAssessment[intent_digest(PI)]; Claim[target]; bridge Claim = I-INF BRIDGE dep of target; UTILITY Claim cited by target; Discharge for target; Mechanism of target; **or** (at APPLY, under **current** ClaimRelation/fingerprint state) any **live** Counterexample whose ART-07b I-CX-01 closure hits any digest in EvidenceClosure(A*, intent). The Counterexample clause is not limited to Counterexamples introduced after intro(A*): a pre-existing FULL Counterexample that becomes connected to audited evidence via a later RENAMES/EQUIVALENT_TO edge still stales the audit when I-CX-01 is re-evaluated at APPLY.

**EvidenceClosure(A*, intent)** (Claim digests only — I-CX-01 does not hit object-table digests):
1. `intent.target_claim_digest`
2. every digest in answers’ `evidence_digests[]` whose EvidenceKindResolver kind is CLAIM, UTILITY, or BRIDGE (Claim digests)
3. for each answer digest of kind PROOF: if ProofAttachment, use that attachment’s `claim_digest` and the linked PE’s `lemma_claim_digests[]`; if ProofEvidence, use `PE.claim_digest` ∪ `PE.lemma_claim_digests[]`
4. for each answer digest of kind CERT (CERT table / CertificationRecord): resolve `CertificationRecord.proof_evidence_digest` → PE; include `PE.claim_digest` ∪ `PE.lemma_claim_digests[]`
5. for each answer digest of kind DISCHARGE: `DischargeRecord.discharger_claim_digest` ∪ `DischargeRecord.target_claim_digest`; if a ProofAttachment exists for `discharger_claim_digest`, also union that PE’s `lemma_claim_digests[]` (same depth as PROOF path)

Do **not** put `proof_evidence_digest` / `certification_digest` / `attachment_digest` / `discharge_digest` themselves into EvidenceClosure for CX freshness (wrong type for I-CX-01).

Re-hold I-AR-03…05 with intent=PI; ValidationPreimageAPPLY.v7 audit_ok + audit_digest.
DRAFT or ACTIVE.

---

## 7. Failures / traces / deferred

`AUDIT_REQUIRED | AUDIT_FAIL | AUDIT_STALE | AUDIT_INDEPENDENCE | AUDIT_EVIDENCE_MISSING | DISCONFIRM_MISSING | UNKNOWN_AUDIT_QUESTION`

TRACE-6A..6K as before; TRACE-6L re-RECORD_AUDIT after stale write at new head → new digest usable for APPLY.

Deferred omitted Qs → Iter7/9/11. ART-11 cleanup Iter14.
