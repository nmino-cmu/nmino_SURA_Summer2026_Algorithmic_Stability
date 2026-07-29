# 11 — Integration Audit Specification

**Artifact ID:** `ART-11`  
**Owner:** Integration Auditor (blocking); never drafts research claims  
**Version:** `ARCH-0.3`  
**Normative status:** `PENDING_MIGRATION` · **Responsible residual iteration:** 14 (descriptive Q-table only; authoritative audit = ART-11b)

> **INCOMPATIBILITY WARNING (Iter6):** Legacy `audit_id` / `cert_id` / `bridge_ids[]` / untyped `BRIDGE_PROVED` **must not authorize promotion**. Authoritative audit = ART-11b AuditRecord bound to `PromotionIntent.intent_digest`. This artifact’s Q-table is descriptive seed for ART-11b genesis questions only.

## Purpose
Reject locally correct results that are irrelevant, mistyped, or incompatible with the obligatory chain.

## IO
**In:** claim/mechanism/cert/utility/bridge IDs + evidence_refs. **Out:** structured audit record + verdict.

## Authority
Integration Auditor issues verdicts; never drafts research claims. EIO may still veto promotion. Orchestrator cannot override FAIL.

## Failure modes
Narrative-only audits; self-produced `disconfirm_log`; Q15 YES via `external_theorem` alone; treating IRRELEVANT as admissibility.

## Audit rules
Q1–Q16 structured answers; `disconfirm_log` producer ≠ auditor; major_milestone blockers; BRIDGE_OPEN fails inference milestones; `hop_chain_ok` / Q16 required for PASS.

## Human gates
`N/A_UTILITY_ACK`; escalation paths → ART-15 novelty/inference/scope gates (verdict `ESCALATE_HUMAN` ≠ gate satisfaction).

## Audit record schema (structured — not narrative)

```text
audit_id
cycle_id
claim_ids[]
definition_pin_set[]
selection_operator_id
mechanism_id
cert_id / cert_kind
utility_id / utility_kind (or NONE)
bridge_ids[]          # required if inference-facing
disconfirm_log_id     # required; anti-laundering
verdict               # PASS | FAIL | IRRELEVANT | ESCALATE_HUMAN
                      # ESCALATE_HUMAN = audit outcome only; does NOT satisfy ART-15 gates
                      # (requires separate human_decisions row with gate_id + target_ref)
answers[]             # 16 structured Answer objects (Q1–Q15 + Q16)
new_instabilities[]
assumptions_newly_violated[]
chain_advancement     # which link advanced, or NONE
hop_chain_ok          # boolean: cards match frozen quarantine.chain_link
```

### Answer object

```text
question_id   # Q1..Q16
response_enum # YES | NO | NA | UNKNOWN
evidence_refs[]  # registry IDs only; prose alone insufficient
blocker_if_no    # boolean: if true and response NO => FAIL
```

## Sixteen questions (machine fields)

| ID | Question | Blocker if NO (when ART-01 `major_milestone` true) |
|----|----------|--------------------------------------|
| Q1 | What exact object was stabilized? (`object_stabilized`: INDEX \| SCORE_VECTOR \| POLICY \| OTHER) | YES if OTHER without human |
| Q2 | Dataset relation pin matches `DEF.neighbor`? | YES |
| Q3 | Probability law of randomness identified (`Q_psi` / none)? | YES |
| Q4 | Perturbation calibration data-independent OR explicit sub-mechanism certified? | YES |
| Q5 | Post-processing preservation justified by cert’s postprocessing rule? | YES if post-processed |
| Q6 | Adaptive repetition accounted for? | YES if repeated |
| Q7 | Composition parameters updated by registered rule? | YES if composed |
| Q8 | Induced policy within scope (or INDEX-only claim)? | YES |
| Q9 | Feasibility unchanged or change typed? | YES |
| Q10 | Inferential target unchanged or change typed? | YES |
| Q11 | Downstream theorem accepts this `cert_kind` via `BRIDGE_PROVED` (or non-inference claim)? | YES if inference milestone — **`BRIDGE_OPEN` / `BRIDGE_ASSUMED` ⇒ FAIL** for inference milestones |
| Q11b | Support of selection law stable under neighbor change, or support-change typed in composition record? | YES if cert quantifies over selection probabilities |
| Q11c | If `literature_alignment ≥ COMBINATION`, literature PASS present (`verification_status = RESOLVED_MATCH` or human ack)? | YES for those mechanism claims |
| Q12 | No theorem assumptions newly violated? | YES |
| Q13 | Utility comparator matches utility_kind? | YES if utility claimed |
| Q14 | No new instability introduced (or logged)? | YES |
| Q15 | Result advances main chain link? | NO → `IRRELEVANT` allowed |
| Q16 | Card hop fields still equal frozen `quarantine[q_id].chain_link`? (`hop_chain_ok`) | YES — ExampleCard.`chain_link_intent` = FalsifierCard.`chain_segment` = `quarantine.chain_link` |

## Verdict rules

- `FAIL`: any blocker NO/UNKNOWN on required path; **inference milestone** (ART-01) with `BRIDGE_OPEN` or `BRIDGE_ASSUMED`; **`hop_chain_ok` false / Q16 NO**  
- `IRRELEVANT`: locally coherent but Q15 = NO (or wrong chain link); record `chain_placement` hop list — **does not** create `admissible_experiment` after the fact  
- `ESCALATE_HUMAN`: scope, cert-kind change, novelty, inference claim, contradiction (audit **verdict** only; ≠ ART-15 gates)  
- `PASS`: all blockers satisfied; Q15 YES; Q16 YES / `hop_chain_ok`; disconfirm log present; EIO still required for promotion  
- Q15 YES **cannot** be satisfied by `external_theorem` alone (ART-01)
- **`hop_chain_ok` ↔ Q16:** must agree; if either false/NO → FAIL (neither field alone can PASS)

## Composition / post-processing evidence (required when Q5–Q7 applicable)

```text
composition_record:
  stages[]              # each: mechanism_id, selection_operator_id, remaining_support_desc
  adaptive              # bool
  parameter_rule_id
postprocessing_chain[]  # functions applied to selector output
support_stability       # STABLE | TYPED_CHANGE | UNKNOWN
```

Audit bound to `definition_pin_set`; pin supersession invalidates PASS.

## Anti-narrative rule

Answers with empty `evidence_refs` count as UNKNOWN.

**`evidence_ref_kind`:** each ref tagged `{REGISTRY_ID | CLAIM | CX | LIT | AUDIT | MANIFEST}`; stub strings that do not resolve → UNKNOWN.

**Applicability bitmap:** at audit open, Integration Auditor records which Q1–Q16 apply; later “N/A” without bitmap entry → FAIL.

**`disconfirm_log` producer** must not equal `auditor_id` (no self-produced disconfirm).

## `disconfirm_log` schema

```text
disconfirm_log_id
cycle_id
attempts[]   # each: channel (CX|LEAN_NEGATION|LIT_DISCONFIRM|OTHER), result, refs[]
producer     # Literature Analyst or Counterexample Attacker — not Integration Auditor
```

Required for integration PASS and for promotions ≥ PARTIAL_RESULT.

## Failure modes

- Checklist filled with prose “yes”
- Passing INDEX stability as POLICY stability
- Treating DP cert as inference coverage without bridge

## Human gates

Auditor cannot approve novelty or new cert kinds; must escalate.
