# 19 — Context and Memory Management

**Artifact ID:** `ART-19`  
**Version:** `ARCH-0.3`

## Purpose
Keep retrieval and working context from laundering superseded/refuted/quarantined material into belief or promotion.

## IO
**In:** query + pin snapshot needs. **Out:** filtered retrieval set; cite-time pin+label snapshots.

## Authority
Committed events authoritative; scratch never. `historical=true` overrides only for explicit historical queries — not for promotion evidence.

## Failure modes
Summary-as-theorem; citing without pin snapshot; retrieving `NEEDS_REVIEW`/`BLOCKED` into promotion packets; SIMULATION events in `dep_closure_ok`.

## Audit rules
Promotion evidence_refs must resolve to allowed retrieval tier; EIO/`I.BullshitLinter` on synthesis; pin mismatch → fail-closed.

## Human gates
None unique — pin/`SCOPE_CHANGE` and novelty gates apply when retrieval drives those claims.

## Problem
Institutional memory can be complete in storage and unsafe in every agent session.

## Rules

1. Default retrieval excludes `SUPERSEDED`, `REFUTED`, `ARCHIVED`, `NEEDS_REVIEW`, `BLOCKED`, and quarantine tags unless `historical=true`
2. Citations must carry pin + label snapshot at cite time
3. Summaries cannot introduce new theorem-shaped claims (bullshit linter ART-18b)
4. Forced re-derivation triggers: pin bump; contradiction open; promotion of dependents
5. Working context budget: prefer primary objects (defs, claims, audits) over narrative memos
6. Failed-proof and cx fingerprints always searchable when planning new attacks
7. Every committed event carries `loop_tag ∈ {DESIGN, RESEARCH, SIMULATION}`; SIMULATION excluded from research `dep_closure_ok`

## Scratch vs committed

Agent working notes are scratch; only promotion transactions and cycle ledger commits persist authority.
