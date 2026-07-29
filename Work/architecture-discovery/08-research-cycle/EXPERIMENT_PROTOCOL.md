# Experiment Protocol Schema (System A ownership)

**Artifact ID:** `ART-08c`  
**Version:** `ARCH-0.3-REPAIR-DUAL.1`  
**Normative status:** `OWNED_BY_DISCOVERY`  
**Home:** `architecture-discovery/` (DUAL.1 M4)

> **DUAL.1:** Author ExampleCard / FalsifierCard for CRP payload. B freezes/binds via ART-08d after intake.  
> **INCOMPATIBILITY WARNING:** `target_cert_kind` is legacy. Prefer ART-07c endpoint digests.

## Purpose
Define ExampleCard / FalsifierCard / experiment-card fields and readiness gates.

## IO
**In:** cycle intent. **Out:** populated cards referenced by `cycle_id` / attack / utility IDs.

## Authority
Specialists populate; Integration Auditor rejects incomplete cards; S04/S09/S12 gates hard.

## Failure modes
Missing Yes fields; `chain_segment` ≠ quarantine.chain_link; HEURISTIC UtilityCompat; orphan attack IDs.

## Audit rules
Too-vague gate; S09 FalsifierCard bind; T07 acceptance.

## Human gates
`CX_CLASS_SKIP_ACK`, utility N/A / waiver gates as triggered.

## Required experiment card fields

Every cycle must populate (also called **ExampleCard** + **FalsifierCard** when split):

### ExampleCard (before conjecture)

| Field | Required |
|-------|----------|
| `exact_research_question` | Yes |
| `quarantine_q_id` | Yes — must equal locked `q_id`; class from `quarantine[q_id]` (ART-01 `admissible_experiment`) |
| `chain_link_intent` | Yes — must equal `quarantine[q_id].chain_link`; **frozen after S04 entry** |
| `optimization_problem` | Yes (finite argmin instance) |
| `selected_object` | Yes (`S_D` description) |
| `neighboring_datasets` | Yes (pin) |
| `baseline_instability` | Yes |
| `perturbation_mechanism_id` | **Phase B / MIXED with mechanism:** Yes after S06. **Phase A characterization:** Optional (omit OK) |
| `mc_allowed` | Must be `auxiliary_only` if MC used |

### FalsifierCard (with conjecture)

| Field | Required |
|-------|----------|
| `formal_hypothesis` | Yes |
| `falsification_criterion` | Yes |
| `witness_template` | Yes |
| `refutation_type` | Yes — explicit_counterexample \| bound_violation \| bridge_impossibility \| utility_dominance_reversal |
| `mandatory_attack_classes[]` | Yes — subset of ART-12 class IDs |
| `target_cert_kind` | Yes |
| `measurand` | Yes |
| `chain_segment` | Yes — characterization \| perturbation \| stability \| composition \| object \| inference \| bridge; must = `quarantine.chain_link` + ExampleCard.`chain_link_intent`; **frozen after S03 entry** |

### Full experiment card (cycle close)

| Field | Required |
|-------|----------|
| `motivation` | Yes |
| `attempted_proof_ref` | Yes or failed_proof_id |
| `utility_analysis_ref` | Yes or explicit N/A |
| `utility_compat_id` | Yes if promoting past CONJECTURE (unless N/A-ack) |
| `attack_log_id` | Yes — canonical name (alias: `adversarial_attack_log_id`); S09 log whose attacks instantiate `witness_template` |
| `attack_record_ids[]` | Yes — nonempty; each id **≡ `cx_id`**; one per `mandatory_attack_classes[]` entry (N/A skip = `cx_id` with `construct=N/A` + `CX_CLASS_SKIP_ACK`) |
| `integration_implications` | Yes (chain hop list) |
| `lean_status` | Yes |
| `result_status` | Yes |
| `unresolved_issues[]` | Yes (may be empty) |
| `next_experiment_hint` | Yes |

Too-vague gate: missing any Yes field → reject enter/complete `S04`–`S12`.
