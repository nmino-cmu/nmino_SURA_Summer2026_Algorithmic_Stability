# 18 — Model Interaction Protocols

**Artifact ID:** `ART-18`  
**Version:** `ARCH-0.3`  
**Normative status:** `ACTIVE_PARTIAL` · report schema here; runtime model identity → ART-04c ModelProvenanceRecord

> **INCOMPATIBILITY WARNING (Iter4):** Critic/orchestrator model strings are non-authoritative for independence or certification credit. Bind MODEL_RUNTIME acts via ART-04c `model_prov_digest` + RoleBinding.

## Purpose
Fix critic report schema and orchestrator reconciliation obligations.

## IO
**In:** critic reports. **Out:** reconciliation record (`accepted/rejected/deferred` + reasons).

## Authority
Critics do not write canonical design/research state. Orchestrator reconciles; must address every CRITICAL (accept, reject-with-reason, or escalate). Full-System Auditor never drafts.

## Failure modes
Reconciliation theater (CRITICAL ignored); orchestrator self-grading `material_new`; critic collusion via shared drafts.

## Audit rules
Iteration record lists every CRITICAL disposition; unanswered CRITICAL → block `DESIGN_FINAL` readiness claims.

## Human gates
Unresolved CRITICAL after reconciliation → human; `DESIGN_FINAL` only human.

## Critic / specialist report schema (fixed)

```text
scope_examined
assumptions
identified_flaws[]
concrete_failure_scenarios[]
affected_components[]
proposed_corrections[]
tradeoffs[]
unresolved_questions[]
confidence
author_principal_digest               # required when ART-04c ACTIVE
author_binding_digest                 # required
author_model_prov_digest?             # required if MODEL_RUNTIME
act_event_seq                         # required when ART-04c ACTIVE; = introducing MutationEvent.event_seq
```

## Orchestrator reconciliation record

```text
iteration_id
critiques_accepted[]
critiques_rejected[]
critiques_deferred[]
canonical_diff_summary
remaining_risks[]
audit_result
convergence_status
next_targets[]
reconciler_principal_digest           # required when ART-04c ACTIVE
reconciler_binding_digest
reconciler_model_prov_digest?
act_event_seq                         # required when ART-04c ACTIVE; = introducing MutationEvent.event_seq
```

## Rules

- Critics do not see each others’ reports until reconciliation (reduce collusion) when feasible
- Orchestrator must address every CRITICAL finding (accept, reject-with-reason, or escalate)
- Confidence scores are informational only
- When ART-04c is ACTIVE: unpinned `act_event_seq` or seq not equal to the introducing MutationEvent ⇒ report/reconciliation is not a credited act (I-MP-02)
