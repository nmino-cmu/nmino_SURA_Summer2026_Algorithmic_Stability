# 14 — Literature Boundary Protocol

**Artifact ID:** `ART-14`  
**Version:** `ARCH-0.3`  
**Normative status:** `PENDING_MIGRATION`

> **INCOMPATIBILITY WARNING (Iter5):** Novelty ladder and citation checklist remain; promotion past CONJECTURE requires ART-13b RequiredGates (`PLAUSIBLE_NOVELTY_LABEL` + `NOVELTY_TRACK_ACK`). Literature PASS alone does **not** authorize `APPLY_PROMOTION`.

## Purpose
Bound literature use; novelty ladder; mechanism-family citation checklist (`mechanism_family_checklist_ok`).

## IO
**In:** mechanism family + prior-art packet. **Out:** lit_ids, alignment label, checklist predicate.

## Authority
System may label ≤ `PLAUSIBLE_NOVELTY`; only human confirms novelty / quarantine whole checklist.

## Failure modes
Second-hand IMPORTED_RESULT; `other_typed` dodge of table families; checklist theater without lit_ids.

## Audit rules
`mechanism_family_checklist_ok` or `LIT_QUARANTINE_ACK` before S06→S09; `I.CitationVerify` on imports.

## Human gates
`LIT_QUARANTINE_ACK`, `PLAUSIBLE_NOVELTY_LABEL`, `NOVELTY_TRACK_ACK`, `NOVELTY_CLAIM`, `IMPORTED_RESULT_REGISTER`.

## Allowed uses of literature

- Identify prior results / mechanisms
- Prevent rediscovery
- Locate proof techniques
- Check assumptions
- Identify open boundaries

## Forbidden

- Autonomous novelty confirmation
- Second-hand citations as IMPORTED_RESULT
- Treating blog/summary as primary theorem source

## Literature claim schema

```text
lit_id
source_locator        # DOI / arXiv
verbatim_span         # excerpt
formalization_mapping # or UNKNOWN
epistemic_strength
verification_status   # UNRESOLVED | RESOLVED_MATCH | RESOLVED_MISMATCH | QUARANTINED
```

## Novelty ladder (human confirms top)

`KNOWN_THEOREM → KNOWN_MECHANISM → ADAPTATION → COMBINATION → PLAUSIBLE_NOVELTY → UNVERIFIED_NOVELTY → CONFIRMED_NOVELTY`

Only human may set `CONFIRMED_NOVELTY`. System max autonomous label: `PLAUSIBLE_NOVELTY` with prior-art packet attached.

**Escalation:** Any autonomous label ≥ `PLAUSIBLE_NOVELTY` triggers human gates `PLAUSIBLE_NOVELTY_LABEL` and (before promotion past CONJECTURE) `NOVELTY_TRACK_ACK` — **not** the audit verdict token `ESCALATE_HUMAN`. Mechanism claims with `literature_alignment ≥ COMBINATION` require literature PASS before integration PASS.

## Mechanism-family mandatory citation checklist

Before closing `S06` for these families, attach resolved primary-source `lit_id`s (or `UNKNOWN` with QUARANTINE):

| Family (`joint_law_family`) | Must cite / compare |
|-----------------------------|---------------------|
| `iid_laplace` | Report Noisy Max; Zrnic–Jordan noisy winner |
| `gap_aware` | GAP-MAX (Bun et al.) |
| `hetero_scale` | Closest sensitivity-weighted / private selection priors |
| `correlated` | State absence if none; do not claim novelty from silence |
| `exp_mech` | ExpMech |
| `permute_flip` | Permute-and-Flip |

**Closed table keys:** `{iid_laplace, gap_aware, hetero_scale, correlated, exp_mech, permute_flip}`. Using `other_typed` for any of these is invalid.

### Predicate `mechanism_family_checklist_ok`

Lookup field: Mechanism.`joint_law_family` (ART-07). True iff **one** of:

1. `joint_law_family` ∈ closed table keys above **and** each required cite has a `lit_id` with `verification_status ∈ {RESOLVED_MATCH, QUARANTINED}` (QUARANTINED rows need `LIT_QUARANTINE_ACK`); **or**
2. `joint_law_family = other_typed` **and** rationale states why it is **not** any closed table key (auditor may reject mislabel); **or**
3. Human `LIT_QUARANTINE_ACK` covers the whole checklist for this cycle.

Hard: `S06 → S09` requires this predicate **or** `LIT_QUARANTINE_ACK`. `math_stable` conjunct #6 same.

## Prior-art packet (required above ADAPTATION)

Structured searches, negative queries, closest theorems with assumption diffs, disconfirm attempts.
