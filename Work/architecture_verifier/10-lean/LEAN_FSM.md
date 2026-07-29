# 10 — Lean Verification State Machine

**Artifact ID:** `ART-10`  
**Version:** `ARCH-0.3`  
**Normative status:** `PENDING_MIGRATION` · **Responsible iteration:** 8

> **INCOMPATIBILITY WARNING (Iter8):** Non-authoritative. Authoritative Lean binding = ART-10b `LEAN_BINDING.md`. Legacy `claim_id` / `cert_kind` dialect quarantined.

## Purpose
Manifest-backed Lean statuses; forbid agent-asserted LEAN_FULL / silent axioms.

## IO
**In:** claim + Lean files. **Out:** rebuilt manifest; status = f(manifest).

## Authority
Lean Verifier read-only rebuilds status; Orchestrator cannot set LEAN_FULL by assertion.

## Failure modes
sorry/admit in CORE; target axiom theater; status without manifest.

## Audit rules
Status predicates in this file; demotion on gap; LEAN before `math_stable` invalid (ART-08).

## Human gates
`AXIOM_ADOPTION`.

## Statuses

`NOT_READY_FOR_LEAN | LEAN_STATEMENT | LEAN_CORE | LEAN_FULL | LEAN_BLOCKED | LEAN_STALE`

## Manifest (mandatory above NOT_READY)

```text
claim_id
toolchain_hash
mathlib_pin
entry_module
prose_sha
lean_statement_sha
definition_pin_set[]
sorry_count
admit_count
custom_axiom_ids[]
imported_axiom_closure[]
build_ok                 # CI rebuild
verifier_run_id
```

**Status = function(manifest)**, never agent label.

## Predicates

| Status | Predicate |
|--------|-----------|
| LEAN_STATEMENT | build_ok; `prose_sha`↔`lean_statement_sha` match; **proof body may be absent**; if proof body present, sorry/admit in body ⇒ cannot claim LEAN_CORE/FULL; LEAN_STATEMENT never implies proved |
| LEAN_CORE | no sorry/admit in core modules; custom axioms ⊆ reviewed imports; conclusion restricted to finite combinatorics / real inequalities / sensitivity / argmin-under-TB / typed composition arithmetic; probabilistic law-of-ξ steps listed as IMPORTED_RESULT |
| LEAN_FULL | entire target closure: sorry=0, admit=0, no target-asserting custom axiom, build_ok, pins match |
| LEAN_BLOCKED | block_class + unblock_criteria + max_cycles SLA |
| LEAN_STALE | any upstream pin bump or toolchain change without remanifest |

## Refusal checklist (force NOT_READY)

Tie-break unset; neighbor unset; **ART-07c certificate endpoint / notion unset** (legacy checklist token `cert_kind` is non-operational); utility comparator unset when utility claimed; \(Q_\psi\) support unset; prose changed in last k cycles without re-hash.

## Axiom adoption

Human gate; justification; expiry review; dependents list. Default refuse.

## Initial formalization targets (when research unblocked)

Finite-set defs; neighbors; argmin+TB; sensitivity bounds; deterministic utility inequalities; composition arithmetic; parameter transforms; dependency structure. Measure theory deferred.

## Independent verifier

Read-only Lean Verifier rebuilds manifest; Orchestrator cannot set LEAN_FULL without verifier artifact.
