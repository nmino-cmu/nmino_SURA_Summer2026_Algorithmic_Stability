# 07 — Research Artifact Schemas

**Artifact ID:** `ART-07`  
**Version:** `ARCH-0.3-REPAIR`  
**Normative status:** `QUARANTINED_LEGACY`  

> **INCOMPATIBILITY WARNING:** Free-floating `mechanism_id` / `cert_id` / `bridge_id` and untyped bridge status are **quarantined**. Authoritative identity: [ART-07b](CANONICAL_OBJECTS.md). Authoritative certificate/bridge typing: [ART-07c](TYPED_CERTIFICATES_AND_BRIDGES.md). This file is explanatory sketch only — **I-LEGACY-QUARANTINE-01**.

**Normative identity layer:** [CANONICAL_OBJECTS.md](CANONICAL_OBJECTS.md) (`ART-07b`).  
**Normative cert/bridge layer:** [TYPED_CERTIFICATES_AND_BRIDGES.md](TYPED_CERTIFICATES_AND_BRIDGES.md) (`ART-07c`).

## Purpose
Instance field schemas for mechanisms, certificates, utilities, bridges, experiments — subordinate to ART-07b object identity.

## IO
**In:** typed instances. **Out:** schema-valid objects referenced by IDs in ResearchState.

## Authority
Schema changes are design material (C12 reset). Instance authorship follows ART-04/05; EIO checks provenance.

## Failure modes
Ghost fields; HEURISTIC UtilityCompat used as resolved; enum bypass via free strings.

## Audit rules
Conformance checked at promotion/`math_stable`; unknown required fields → fail-closed.

## Human gates
Schema widening that changes cert/utility kinds → `STABILITY_NOTION_CHANGE` / related gates.

## Mechanism

```text
mechanism_id
location                  # scores | other(typed)
joint_law_family          # CLOSED enum: iid_laplace | hetero_scale | correlated | gap_aware | exp_mech | permute_flip | other_typed
                          # Table families (ART-14) MUST use the matching enum value — other_typed forbidden for those
psi_data_dependence       # independent | explicit_submechanism
submechanism_ids[]        # if explicit_submechanism
support
density_or_mass           # optional
correlation_structure
tie_break_id              # must equal DEF.tie_break pin or justify
sensitivity_assumptions[]
gap_assumptions[]
geometry_assumptions[]
composition_behavior
known_failures[]          # cx class ids
utility_effects_hypothesis
selection_operator_id
definition_pin_set[]
```

## Certificate

```text
cert_id
cert_kind   # DET_SENSITIVITY | LIPSCHITZ_OUTPUT | TV | MAX_DIVERGENCE |
            # APPROX_INDISTINGUISHABILITY | DP | ORACLE_STABILITY | MAX_INFO |
            # SELECTIVE_LIKELIHOOD | INFERENCE_COVERAGE | OTHER_TYPED
domain
codomain
selection_operator_id
object_stabilized         # INDEX | SCORE_VECTOR | POLICY | OTHER
quantified_datasets
randomness
params
failure_prob
assumptions[]
composition_rule_id
postprocessing_rule_id
bridge_availability       # NONE | OPEN | ASSUMED | PROVED + bridge_id
forbidden_uses[]
definition_pin_set[]
```

## Utility

```text
utility_id
utility_kind  # SCORE_REGRET_EMP | POP_REGRET | E_REGRET | HP_REGRET | WC_REGRET |
              # POLICY_DISTANCE | POLICY_VALUE | FEASIBILITY | APPROX_RATIO |
              # CI_WIDTH | COMPUTE
comparator
incompatible_with[]
definition_pin_set[]
```

## UtilityCompat

```text
utility_compat_id
cert_id
utility_id
link_kind            # PROVED_INEQUALITY | HEURISTIC | WAIVER_HUMAN
blocker_if_open_on_promotion  # true for PARTIAL_RESULT and above unless WAIVER_HUMAN
definition_pin_set[]
```

**Rule:** No promotion past CONJECTURE without UtilityCompat where `link_kind ∈ {PROVED_INEQUALITY, WAIVER_HUMAN}` **or** experiment-card `utility_analysis_ref = N/A` with `chain_segment=stability` and Integration Auditor ack.  
**`HEURISTIC` link_kind does not satisfy `utility_compat_resolved`.**

## Bridge

```text
bridge_id
from_cert_kind
to_cert_kind
object_from
object_to
status          # OPEN | ASSUMED | PROVED | REFUTED
claim_id?       # if PROVED
human_required  # true if ASSUMED used in milestone
```

## Experiment (cycle)

Required fields per ART-08 / ART-08c; plus `attack_log_id` (alias `adversarial_attack_log_id`), `attack_record_ids[]` (each ≡ `cx_id`), `audit_id`, `result_status`, `utility_compat_id?`.

## Incompatible comparison rule

Utilities with different `utility_kind` or mismatched `comparator` cannot be numerically ranked in synthesis.
