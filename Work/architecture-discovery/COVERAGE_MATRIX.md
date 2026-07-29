# Discovery Architecture — Coverage Matrix

**Status:** ACTIVE (planning artifact; updated as sections freeze)  
**Date:** 2026-07-25  
**Depends on:** ART-A-00, ART-A-02, ART-A-03 (FROZEN)

## Plan-audit findings (P1–P11)

Recorded from audited plan; incorporated into section charters:

| ID | Severity | Finding | Resolution |
|----|----------|---------|------------|
| P1 | High | Verifier ART-04e missing new A roles | ART-A-04e Discovery-owned extension |
| P2 | High | Gate-3 policy type missing | `SessionPolicy` in A-02 |
| P3 | Med | Slice rules underspecified | A-03 §9.1 frozen |
| P4 | Med | close_reason home | SessionClosed event |
| P5 | Med | DS91 misuse | A-03 allowlist |
| P6 | Med | Conformance fork risk | A-08 sole normative |
| P7 | Med | Brainstorm §4–15 open list | Fold-map in design companion |
| P8 | Low | Readiness bloat | Six readiness files |
| P9 | Low | Matrix-before-A-04 | This document before A-04 |
| P10 | Low | A-04 ownership drift | A-04 schemas-only charter |
| P11 | Info | A-04…A-08 + A-04e sufficient | Confirmed below |

## Coverage

| Topic | Status | Authoritative | New section? |
|-------|--------|---------------|--------------|
| Overall component architecture | Complete | ART-A-00 | No |
| Module ownership / contracts | Complete | ART-A-02 | No |
| Lifecycle / FSM | Complete | ART-A-03 | No |
| Discovery IR field schemas | Partial | A-02 taxonomy | **ART-A-04** |
| Engine invocation / slice I/O | Partial | A-03 §9.1 | **ART-A-05** |
| Gates / human packets | Complete | ART-A-03 | No |
| Frontier scheduling | Partial | ART-08b + A-03 DS02 | No new (A-05 may cite) |
| Branch / portfolio formal semantics | Partial | A-02 §1.3/§6 | Covered in **A-04** + A-02 |
| CRP compile / seal / submit | Partial | A-02/A-03 | **ART-A-06** |
| Verifier-feedback integration | Partial | A-03 §11.2 | **ART-A-07** |
| Persistence / replay | Partial | A-03 history | **ART-A-07** |
| Failure / recovery | Partial | A-03 | **ART-A-07** |
| Security / authority / roster | Partial | verifier ART-04e | **ART-A-04e** |
| Configuration / policy | Partial | SessionPolicy | A-03 + A-07 |
| Implementation interfaces | Partial | ART-24 / A-03 | **ART-A-06** |
| Testing / conformance | Missing | — | **ART-A-08** |
| ART-08 migration | Partial | A-03 I-A03-07 | **ART-A-07** |
| Observability / audit logging | Partial | SessionEvent | A-03 + A-07 |

## Fold map

| Brainstorm topic | Home |
|------------------|------|
| Information flow | A-00 + A-04/05/06 |
| Reasoning pipeline | A-03 + A-05 |
| Math KR | A-04 |
| Lit / hyp / op / qty / thm / sketch / soft-CX | A-02 + A-05; engine stubs |
| CRP generation | A-06 |
| Verifier interfaces | A-06 + A-07 |
| Human researcher | A-03 |

## Remaining section plan (locked) — COMPLETE

1. ART-A-04e — **FROZEN**  
2. ART-A-04 — **FROZEN**  
3. ART-A-05 — **FROZEN**  
4. ART-A-06 — **FROZEN**  
5. ART-A-07 — **FROZEN**  
6. ART-A-08 — **FROZEN**  
7. readiness/ — **COMPLETE** (FINAL_AUDIT PASS)

**No ART-A-09+** required.
