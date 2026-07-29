# 09 — Theorem Status State Machine

**Artifact ID:** `ART-09`  
**Version:** `ARCH-0.3-REPAIR`  
**Normative status:** `QUARANTINED_LEGACY` · **Responsible iteration:** 5  

> **INCOMPATIBILITY WARNING:** Unary/dual labels are **non-normative**. Axes + proof floor: ART-07b. RESULT/inference coupling + bridge floors: ART-07c (`I-STATUS-COUPLE-*`). Do not promote using this file’s tables.

## Purpose
Multi-axis claim labels and promotion/demotion rules tied to UtilityCompat, literature, and audits.

## IO
**In:** promotion transaction. **Out:** updated claim axes or reject.

## Authority
Orchestrator proposes; Integration Auditor + EIO + Certifier constraints bind; human gates for novelty/inference.

## Failure modes
Unary-status laundering; promoting past CONJECTURE without UtilityCompat; IMPORTED_RESULT as chain contribution alone.

## Audit rules
Promotion predicates in this file + ART-06/08/11 must all hold; demotion waves incomplete → block S14.

## Human gates
`NOVELTY_*`, `INFERENCE_THEOREM_CLAIM`, `IMPORTED_RESULT_REGISTER`, `MATH_STABLE_ACK`, waivers as listed in ART-15.

## Labels

`OBSERVATION | DEFINITION | ASSUMPTION | EXAMPLE | COUNTEREXAMPLE | HEURISTIC | CONJECTURE | PARTIAL_RESULT | PROVED_ON_PAPER | LEAN_STATEMENT | LEAN_CORE | LEAN_FULL | IMPORTED_RESULT | REFUTED | BLOCKED | SUPERSEDED | NEEDS_REVIEW`

## Multi-axis record (not unary only)

```text
formal_status       # Lean-related
paper_status        # prose proof status
empirical_support   # toy/analytic only in-scope
literature_alignment
human_sanction
active_contradiction_id?
```

Display may show a summary label only if axes are consistent.

## Promotion evidence requirements

| To | Requires |
|----|----------|
| CONJECTURE | Formal statement + falsification criterion |
| PARTIAL_RESULT | Proof sketch + gaps + S09 nonempty + **S08 UtilityCompat resolved or UTILITY_WAIVER/N/A-ack** + literature rule |
| PROVED_ON_PAPER | Complete prose + Certifier ≠ Proposer + S09 + **S10 = PASS** + `audit_id` + UtilityCompat + literature rule |
| IMPORTED_RESULT | Primary-source excerpt ID + assumption map + EIO + `IMPORTED_RESULT_REGISTER` (first use **and** any re-frame of assumptions / formalization mapping / chain role) |
| LEAN_* | ART-10 manifest predicates |
| REFUTED | Active cx FULL_REFUTE |
| SUPERSEDED | Replacement claim ID + pin reason |

## Hard bans

- Cannot display PROVED_* if dependency closure contains CONJECTURE/OPEN bridge used essentially
- Cannot set LEAN_FULL by agent assertion
- Fragmentation laundering: synthesis cannot assemble theorem-shaped claim from shards without a parent claim_id promotion
- **Novelty fragmentation:** cannot assemble contribution-shaped narrative from shards labeled only `ADAPTATION`/`COMBINATION` while any component carries `PLAUSIBLE_NOVELTY` without human novelty-track gate
- Mechanism claims with `literature_alignment ≥ PLAUSIBLE_NOVELTY` cannot promote past CONJECTURE without human gate **`NOVELTY_TRACK_ACK`** (ART-15)

## Demotion

Automatic on pin supersession, cx, Lean gap, human revoke → `NEEDS_REVIEW` or `REFUTED`/`SUPERSEDED`.
