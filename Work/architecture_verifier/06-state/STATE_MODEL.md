# 06 — Canonical State Model

**Artifact ID:** `ART-06`  
**Version:** `ARCH-0.3`  
**Normative status:** `QUARANTINED_LEGACY`  
**Superseded for mutation/commit authority by:** [MUTATION_AND_AUTHORITATIVE_STATE.md](MUTATION_AND_AUTHORITATIVE_STATE.md) (`ART-06b`)  
**Responsible iteration residual:** 5 (PromotionIntent), 9 (FSM coupling)

> **INCOMPATIBILITY WARNING:** This file’s ID-keyed registries (`claim_id`, `cert_id`, `bridge_id`, …) and caller-supplied promotion booleans (`dep_closure_ok`, `eio_pass`, `hop_chain_ok`, …) are **non-authoritative**.  
> **Authoritative mutation:** ART-06b `I.Commit` only.  
> **Object identity:** ART-07b digests. **Cert/bridge typing:** ART-07c.  
> Do not implement ART-06 as written.

## Purpose (historical)

Defined DesignState vs ResearchState stores, registries, and promotion transaction fields — retained as historical shape notes only.

## IO
**In:** (legacy) promotion/demotion events, cycle commits. **Out:** (legacy) registry snapshots.

## Authority
**Revoked.** See ART-06b.

## Failure modes
Scratch-as-authority; dual frontier writes; promotion without literature/role/loop_tag fields; expired `scope_exceptions` ignored — addressed or deferred under ART-06b + later iterations.

## Stores (historical sketch — non-authoritative keys)

| Store | Notes under ART-06b |
|-------|---------------------|
| `DesignState` | Retained; mutate via `I.Commit` store=DESIGN |
| `ResearchState` | Retained; digest-native keys only (ART-06b §7) |
| *(missing)* ControlState | **Added in ART-06b** for heads / hard-stop fence |

## ResearchState registries (LEGACY KEYS — do not implement)

| Registry | Legacy key | Migration |
|----------|------------|-----------|
| `definitions` | `def_id@pin` | ART-07b DefinitionVersion digests |
| `theorem_dag` | `claim_id` | `claim_digest` |
| `certificates` / `bridges` | `cert_id` / `bridge_id` | Claims + ART-07c; no parallel authority tables |
| `counterexamples` | `cx_id` | `cx_digest` |
| `hard_stop` | singleton in ResearchState | **ControlState** `HardStopRecord` (ART-06b) |
| others | ID-native | digest or scheduled later iter |

## Promotion transaction fields (LEGACY — non-authoritative)

Caller booleans and unary `from_status`/`to_status` are **forbidden** as commit authority (ART-06b §4). Axis transitions applying promotion → `PROMOTION_DEFERRED_ITER5`.

## Triple-store semantics (historical)

Committed / derived / scratch tiers survive as intent; **committed** means ART-06b `MutationEvent` only.
