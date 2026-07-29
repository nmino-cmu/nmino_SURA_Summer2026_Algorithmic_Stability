# 12 — Counterexample Protocol

**Artifact ID:** `ART-12`  
**Owner:** Counterexample specialist (proposes); Integration Auditor + EIO (effects)  
**Version:** `ARCH-0.3`  
**Normative status:** `PENDING_MIGRATION` · **Responsible iteration:** 7

> **INCOMPATIBILITY WARNING:** `cx_id` / `target_claim_ids` dialect conflicts with ART-07b. Anti-gaming “cert kind” language is legacy — ART-07c. Demotion waves not durable (`B-DEMOTION-WAVE-01`). **Register/demotion effects apply only via ART-06b `I.Commit`** (Auditor/EIO do not mutate registries directly). BRIDGE_OPEN → ART-07c applicability.

## Purpose
Persist adversarial attacks as first-class research outputs; force demotions; prevent failure laundering.

## IO
**In:** attack constructs / FalsifierCard. **Out:** `cx_id` registry rows; demotion waves.

## Authority
Attacker proposes; Integration Auditor + EIO apply demotion effects; fingerprints prevent delete-laundering.

## Failure modes
Empty S09; prose-only attacks; applicable-class omit; non-registry skip IDs.

## Audit rules
Applicable-set ⊇ mandatory; `attack_record_ids[]`≡`cx_id`; nonempty construct or `CX_CLASS_SKIP_ACK`.

## Human gates
`CX_CLASS_SKIP_ACK`; pin-narrowing that dodges active cx → human if neighbor/selector/cert changes.

## Mandatory attack classes

Every cycle’s `S09` must attempt at least one applicable class and log all applicable skips with reason:

| Class ID | Attack |
|----------|--------|
| `CX.vanish_gap` | Score gaps → 0 |
| `CX.zero_prob` | Positive mass under \(D\), zero under \(D'\) |
| `CX.hetero_norm` | Heterogeneous scales break normalization / density ratios |
| `CX.data_dep_scale` | Data-dependent \(\psi\) without sub-mechanism cert |
| `CX.support_change` | Candidate support / remaining set changes |
| `CX.nonunique_min` | Nonunique argmin / tie-break sensitivity |
| `CX.tie_unstable` | Unstable or data-dependent tie-break |
| `CX.active_set` | Inner active-set / feasibility bit flips |
| `CX.unbounded_sens` | Unbounded or vacuous \(\Delta\) |
| `CX.noncompose` | Adaptive composition invalidates parameter additivity |
| `CX.bridge_fail` | Stability cert does not imply inference |
| `CX.index_vs_policy` | Index stable, induced \(S_D\) / policy not |

### Applicable-set expansion (hard)

`FalsifierCard.mandatory_attack_classes[]` **must include every applicable class**. Omitting an applicable class is invalid S03/S09 (cannot shrink the set to dodge INVARIANTS #5).

| If … | Then applicable (minimum) |
|------|---------------------------|
| `joint_law_family ∈ {hetero_scale, correlated}` | `CX.hetero_norm` |
| `psi_data_dependence = explicit_submechanism` or data-dep ψ claimed | `CX.data_dep_scale` |
| inference-facing claim / ART-07c bridge not INFERENCE-applicable | `CX.bridge_fail` |
| `object_stabilized = POLICY` (or policy claim) | `CX.index_vs_policy` |
| always (baseline) | ≥1 of `{CX.vanish_gap, CX.nonunique_min, CX.tie_unstable}` |

Additional classes from the table may be listed; skips use registry `cx_id` + `CX_CLASS_SKIP_ACK`.

## Counterexample record schema

```text
cx_id
cycle_id
target_claim_ids[]
definition_pin_set[]
attack_class
refutation_target    # DEFINITION | MECHANISM | CERTIFICATE | BRIDGE | UTILITY | COMPOSITION | INFERENCE
construct            # finite analytic description preferred; nonempty required for ≥1 attack
witness_kind         # analytic_closed | finite_construction | limit_family
parameters            # gap schedule, support, scales, n, m, …
refutes              # claim predicate
severity             # FULL_REFUTE | PARTIAL | ASSUMPTION_EXPOSED
fingerprint          # attack_class + refutation_target + goal_shape + obstruction_class + pin hash
status               # ACTIVE | SUPERSEDED_EQUIVALENT | ARCHIVED
equivalent_to[]      # other cx_ids
demotion_triggered[] # claim_ids demoted
```

## Bridge-open attack obligation

Any inference-facing milestone whose ART-07c `I.BridgeApplicabilityEvaluate(use_class=INFERENCE_FACING)` is not APPLICABLE auto-spawns a `CX.bridge_fail` obligation before any integration PASS for that claim. Legacy `BRIDGE_OPEN` label is non-operational.

## Demotion rules

- `FULL_REFUTE` → **synchronous demotion transaction** before any same-cycle promotion: targets `REFUTED`/`SUPERSEDED`; DAG dependents → `NEEDS_REVIEW`; `demotion_triggered[]` **must be nonempty** or cx record is invalid
- `PARTIAL` with `refutes` binding a live claim → if certifier does not downgrade within 1 cycle → auto `NEEDS_REVIEW` + promotion block
- `ASSUMPTION_EXPOSED` → add assumption obligation or weaken; block promotion until resolved; `assumption_carve_out` human-gated if charter-narrowing
- Fingerprint match → equivalence class; no duplicate
- Independent certifier may challenge severity; unresolved → ACTIVE blocker
- Pin supersession → demotion **wave** (ART-16): incomplete wave blocks S14

## Anti-gaming

Narrowing definitions to dodge an active `cx_id` requires new pin + human gate if it changes neighbor, selector, or cert kind; old claims do not automatically inherit immunity.

**S09 nonempty construct rule:** At least one attack record must include a nonempty `construct` field that instantiates the cycle’s FalsifierCard `witness_template`. Logging all classes as N/A without human `CX_CLASS_SKIP_ACK` is invalid S09.

**`attack_record_id` binding:** Experiment-card `attack_record_ids[]` entries are `cx_id`s — one per mandatory class (which must cover the applicable set). Invalid S09 if any id is missing from the registry. Class skip = still a `cx_id` with `construct=N/A` + human `CX_CLASS_SKIP_ACK` (no non-registry IDs).

## Invariants

- Counterexamples never deleted; prune = archive tier only
- Default retrieval excludes ARCHIVED unless `historical=true`
- Empty `S09` log blocks milestone promotion

## Failure modes

- “Attacked” with prose only
- Redefining away pathology without pin bump
- Ignoring index≠policy class for policy claims
