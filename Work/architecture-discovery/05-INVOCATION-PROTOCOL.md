# ART-A-05 — Invocation Protocol (System A)

**Artifact ID:** `ART-A-05`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `FROZEN`  
**Frozen:** `2026-07-25` (re-audited `2026-07-25b`)  
**Owner:** Research Discovery Assistant (ART-01D)  
**Depends on:** ART-A-02 · ART-A-03 (slice lifecycle) · ART-A-04 (schemas)  
**Does not modify:** Engine stub bodies; Soft Attack B-authority; FSM transitions

## Purpose

**Authoritative home** for DiscoverySlice **execution** contracts (inputs, depends_on, completions, parallel reads).

## Non-goals

- Decide when slices open/close (ART-A-03)  
- Rewrite ART-A-NOV/ATP/MECH/CONJ  
- Authorize Soft Attack as B CX

## Principles

**I-A05-01** Orch schedules; engines execute only scheduled invocations.  
**I-A05-02** Inputs bound to fixed `input_snapshot_digest` (ART-A-03 open).  
**I-A05-03** Outputs = owner-minted IR versions or proposal requests (A-02).  
**I-A05-04** Precedence: A-03 = slice lifecycle timing; **this section = execution semantics**.

## Protocols

### P-A05-INV — Invocation

```text
invocation_id, slice_id, module, intent, input_refs[], depends_on[]
```

### P-A05-CMP — CompletionRecord

```text
invocation_id, status: OK|FAILED|CANCELLED, output_version_ids[], error?
```

### P-A05-PAR — Parallel rules

1. All unordered parallel invocations read the **same** fixed input snapshot.  
2. One invocation MUST NOT read another’s outputs in the same slice unless `depends_on` lists that invocation.  
3. Outputs are append-only IR mints.  
4. Completion records retained for replay (ART-A-07).  
5. Barrier snapshot digest uses deterministically ordered tip pins (A-03/A-04).  
6. Math outputs may vary across runs; control replay uses recorded completion version_ids.

## Legal / illegal

| Legal | Illegal |
|-------|---------|
| Execute scheduled invocation | Engine commits FSM transition |
| Mint owned classes | Cross-invocation read without depends_on |
| Soft Attack RewriteProposal | Soft Attack RECORD_COUNTEREXAMPLE |

## Failures

Invocation FAILED recorded; slice may COMPLETED with partials; Orch chooses refine/close per A-03 — not DS91 for math failure.

## Changelog

2026-07-25: Initial.  
2026-07-25b: Explicit authority for slice execution; P-A05-* IDs; parallel rules moved from A-03.
