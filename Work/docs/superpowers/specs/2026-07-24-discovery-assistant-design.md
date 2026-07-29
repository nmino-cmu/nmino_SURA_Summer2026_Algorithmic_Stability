# Research Discovery Assistant — Design Spec

**Date:** 2026-07-24 (updated 2026-07-25)  
**Status:** ART-A-00 … ART-A-08 + ART-A-04e **FROZEN**; readiness PASS  
**Normative home:** [`architecture-discovery/`](../../../architecture-discovery/)  
**Verification Architecture:** frozen (`architecture_verifier/`) — not modified

## Locked design choices

Unchanged from dual-system brainstorm (extend-in-place, soft attack, hybrid gates, Pareto, operators, IR, pack-before-Gate-3, etc.).

## Frozen sections

| ID | Path |
|----|------|
| ART-A-00 | `architecture-discovery/00-OVERALL.md` |
| ART-A-02 | `architecture-discovery/02-INTERNAL-MODULES.md` |
| ART-A-03 | `architecture-discovery/03-SESSION-LIFECYCLE.md` |
| ART-A-04e | `architecture-discovery/04e-OPERABLE-ROSTER.md` |
| ART-A-04 | `architecture-discovery/04-DISCOVERY-IR.md` |
| ART-A-05 | `architecture-discovery/05-INVOCATION-PROTOCOL.md` |
| ART-A-06 | `architecture-discovery/06-CRP-INTERFACE.md` |
| ART-A-07 | `architecture-discovery/07-PERSISTENCE-REPLAY.md` |
| ART-A-08 | `architecture-discovery/08-CONFORMANCE.md` |

## Fold map (brainstorm §4–15)

| Topic | Home |
|-------|------|
| Information flow | A-00 + A-04/05/06 |
| Reasoning pipeline | A-03 + A-05 |
| Math KR | A-04 |
| Lit/hyp/op/qty/thm/sketch/soft-CX | A-02 + A-05 |
| CRP generation | A-06 |
| Verifier interfaces | A-06 + A-07 |
| Human researcher | A-03 |

## Readiness

[`architecture-discovery/readiness/`](../../../architecture-discovery/readiness/) — INDEX, MATRICES, WBS, CONFORMANCE_INDEX, ASSUMPTIONS, FINAL_AUDIT (**PASS**).

## Freeze rule

No edit to frozen architecture shape without explicit unfreeze.
