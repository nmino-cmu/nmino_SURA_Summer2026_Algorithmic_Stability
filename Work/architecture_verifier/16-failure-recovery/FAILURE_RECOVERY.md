# 16 — Failure-Recovery Specification

**Artifact ID:** `ART-16`  
**Version:** `ARCH-0.3`  
**Owner:** Verification Orchestrator (executes B recovery); EIO (blocks unsafe recovery); Discovery Orchestrator owns A-local crash recovery only
**Normative status:** `PENDING_MIGRATION` · **Responsible iterations:** 7 (demotion→ART-16b), 10 (restore)

> **INCOMPATIBILITY WARNING (Iter7):** Demotion wave prose below is non-authoritative. Authoritative durable waves = ART-16b `DEMOTION_WAVES.md`.

> **INCOMPATIBILITY WARNING:** Demotion prose ≠ durable waves. Checkpoint restore → ART-17b (independent trust anchor). **Hard-stop:** use ART-06b `I.Commit` HARD_STOP_*; ControlState authoritative — not direct `I.HardStop` / ResearchState flag.

## Purpose / IO / Authority

- **Purpose:** Recover from integrity failures without resurrecting refuted claims or inventing promotions.
- **Inputs:** Failure class, checkpoint IDs, contradiction/cx IDs.
- **Outputs:** Recovery action record; required `I.HardStop` when any playbook freezes writes; demotion wave_id.
- **Authority:** Orchestrator proposes; EIO may block restore/promote; `I.HardStop` may be invoked by HUMAN / BUDGET / SYSTEM (ART-15 enter-freeze exception); human alone for `OVERRIDE_EIO` / `HARD_STOP_RELEASE`.

## Failure modes
Restore below FULL_REFUTE watermark; incomplete demotion wave then S14; inventing promotions during recovery.

## Audit rules
Playbook steps logged; ART-24 recovery precedence; `I.CheckpointValidate` before resume promotions.

## Human gates
`HARD_STOP` release; `OVERRIDE_EIO`; S15 packets.

## Playbooks (operational)

### P1 — Contradictory theorem claims
1. Open `contradictions` with both claim IDs + pins.  
2. Block promotions in dependency closure.  
3. If age > `MAX_CONTRADICTION_AGE_CYCLES` (default 5) → S15 human packet.  
4. Resolution only via human Decision or REFUTED/SUPERSEDED of one side.

### P2 — Corrupted / inconsistent state
1. Freeze writes via `I.HardStop` (`source=BUDGET` on budget breach, or `HUMAN`/`SYSTEM`) → `ResearchState.hard_stop.active=true` (authoritative; ART-06/15). Release requires ART-15 `HARD_STOP_RELEASE`.  
2. Select restore target by **forward-fix only** (ART-17): never `event_seq` below latest FULL_REFUTE event.  
3. Rebuild derived indexes from committed events.  
4. Discard scratch.  
5. Startup validator: if any PROVED_* depends on REFUTED/SUPERSEDED cx → fail-closed to S15.

### P3 — Repeated rediscovery / obstruction
1. Fingerprint match → attach to existing failed_proof/cx.  
2. If same fingerprint ≥3 cycles → force {definition revision | impossibility cycle | human escalation} — not another proof attempt.

### P4 — Lean gap / contradiction
1. Demote to LEAN_STALE / NOT_READY.  
2. Triage: revise defs | weaken theorem | split conjecture | register cx.  
3. **Forbidden:** silent axiom to unblock.

### P5 — Excessive speculative prose
1. Run bullshit linter (ART-18b).  
2. If claims/evidence ratio exceeds threshold OR contribution lexicon without registry IDs → stagnation report; block synthesis commit.

### P6 — Orchestrator / auditor failure
- Orchestrator: `I.HardStop` `{source=SYSTEM, signal_ref=orchestrator_failure}` → `ResearchState.hard_stop.active=true`; human restart from validated checkpoint; resume only after `HARD_STOP_RELEASE`.  
- Auditor: fail-closed (no PASS); human.

### P7 — Runaway iteration
- `MAX_CYCLES_WITHOUT_CHAIN_ADVANCE` (default 8) → mandatory S15.  
- `GLOBAL_CYCLE_BUDGET_PER_MILESTONE` (default 40) → `I.HardStop` `{source=BUDGET}`.

## Demotion wave (shared with ART-12)

```text
wave_id
trigger            # FULL_REFUTE | PIN_SUPERSESSION | HUMAN
order: pin bump → invalidate audits → demote claims by DAG closure → LEAN_STALE dependents → emit wave_id
incomplete_wave blocks S14
```

## Fail-closed defaults

When uncertain: do not promote; do not claim Lean verified; do not claim novelty; do not start implementation; do not restore below refutation watermark.
