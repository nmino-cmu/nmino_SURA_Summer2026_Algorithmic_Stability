# 17 — Infinite-Operation and Checkpointing

**Artifact ID:** `ART-17`  
**Version:** `ARCH-0.3`  
**Normative status:** `PENDING_MIGRATION` · **Responsible iteration:** 10

> **INCOMPATIBILITY WARNING:** Descriptive only. Authoritative checkpoint/restore = ART-17b. Legacy merkle-only watermark and `I.HardStop → ResearchState.hard_stop` are shadow/non-authoritative.

## Purpose / IO / Authority

- **Purpose:** Run indefinitely without epistemic decay or silent rollback past refutations.
- **Inputs:** Committed events, pin table, gate statuses.
- **Outputs:** Checkpoint snapshots; restart validation results.
- **Authority:** System creates checkpoints; `I.HardStop` (HUMAN/BUDGET/SYSTEM) sets freeze; EIO blocks invalid restore.

## Failure modes
Silent restore below FULL_REFUTE watermark; merkle mismatch ignored; checkpoint without `I.CheckpointValidate`.

## Audit rules
Startup: `I.CheckpointValidate` PASS before promotions; fail → S15.

## Human gates
`HARD_STOP` / `HARD_STOP_RELEASE` (ART-15); budget freeze via `I.HardStop` without prior HARD_STOP row.

## Checkpoint schema

```text
checkpoint_id          # immutable
event_seq_max          # inclusive
merkle_root            # hash of committed event payloads 0..event_seq_max
pin_table_hash
open_contradiction_ids[]
gate_status_snapshot   # MUST include hard_stop:{active, source, set_at_event_seq, signal_ref, release_dec_id?}
lean_manifest_ids[]
audit_ledger_tail_id
created_at
```

**Not included:** agent scratch, uncommitted drafts.

## Merkle construction (minimal)

1. Canonicalize each committed event as UTF-8 JSON with sorted keys.  
2. `leaf_i = H(canonical_event_i)`.  
3. Merkle tree over leaves `0..event_seq_max` (pairwise H(left||right); odd promote).  
4. Store `merkle_root` on checkpoint.  
5. Startup validator: recompute root; compare; check `event_seq_max ≥ max_seq(FULL_REFUTE events)`.  
6. Fail → S15; no promotions. Interface: `I.CheckpointValidate`.

## Restore rules (integrity)

1. Restore only to a checkpoint with valid merkle verification.  
2. **Never** restore to `event_seq_max` strictly less than the latest FULL_REFUTE event’s seq (refutation watermark).  
3. Prefer forward-fix (replay events) over backward rollback.  
4. After restore: rebuild derived indexes; run startup validator (ART-16 P2).  
5. Failed validation → S15; no promotions.

## Controls

| Control | Spec |
|---------|------|
| Cycle IDs | Immutable once closed |
| History | Append-only committed events |
| Synthesis | Periodic; **no new claims**; bullshit linter required |
| Prune | Archive tier only; never delete |
| Frontier | Single scheduler; atomic commit |
| Failure fingerprints | Match on planning |
| Novelty dampener | ART-08b |
| Retrieval tiers | Exclude SUPERSEDED/REFUTED/NEEDS_REVIEW/BLOCKED/quarantine by default |
| Restart | Rebuild derived from committed; never promote from scratch |
| Definition pins | Versioned + demotion waves |
| Long-horizon goals | Chain-link obligations, not lemma count |
| Interrupt | `I.HardStop` → `ResearchState.hard_stop.active`; HUMAN/BUDGET/SYSTEM; release via `HARD_STOP_RELEASE` |

## Budgets

- `MAX_CYCLES_WITHOUT_CHAIN_ADVANCE = 8`  
- `GLOBAL_CYCLE_BUDGET_PER_MILESTONE = 40`  
- `MAX_CONTRADICTION_AGE_CYCLES = 5`
