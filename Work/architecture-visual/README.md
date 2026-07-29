# Architecture Visual Guide

Easy-read diagrams for the `architecture/` package. These are **explanatory** — normative text lives in `../architecture/`.

**Package posture (as of Sol package gate PASS):** `NON-RELEASE` · `IMPLEMENTATION_BLOCK` ACTIVE · `DESIGN_FINAL` pending human approval.

## Start here

1. [00-GENERAL — Whole system](00-GENERAL.md)
2. Then skim sections below in order

## Sections

| Doc | Covers |
|-----|--------|
| [01-charter-scope](01-charter-scope.md) | Charter, math scope |
| [02-context](02-context.md) | System context / dual loop |
| [03-agents-identity](03-agents-identity.md) | Roles, identity, operable minimal |
| [04-authority](04-authority.md) | Authority / escalation |
| [05-mutation-state](05-mutation-state.md) | Commit boundary, stores, hard-stop |
| [06-objects-certs](06-objects-certs.md) | Claims, certs, bridges, digests |
| [07-research-cycle](07-research-cycle.md) | Cycle FSM + cycle binding |
| [08-lean-status](08-lean-status.md) | Lean + theorem status axes |
| [09-audit-provenance](09-audit-provenance.md) | Integration audit + DD/model provenance |
| [10-counterexample-demotion](10-counterexample-demotion.md) | CX + demotion waves |
| [11-promotion](11-promotion.md) | Promotion intent / APPLY |
| [12-gates-literature](12-gates-literature.md) | Human gates + literature boundary |
| [13-recovery-checkpoint](13-recovery-checkpoint.md) | Failure recovery + checkpoint/restore |
| [14-models-memory](14-models-memory.md) | Model protocols + memory |
| [15-invariants-interfaces](15-invariants-interfaces.md) | Hard invariants + interfaces |
| [16-conformance-release](16-conformance-release.md) | Conformance fixtures + release identity |
| [18-dual-system-separation](18-dual-system-separation.md) | System A vs B split · CRP intake |
| [**DISCOVERY_VERIFIER_INFORMATION_FLOW**](DISCOVERY_VERIFIER_INFORMATION_FLOW.md) | **A↔B bridge · CRP lifecycle · illegal crossings** |

## How to read the diagrams

- Open any `.md` in Cursor/VS Code preview (or GitHub) so Mermaid renders.
- Solid arrows = authority / data flow.
- Dashed arrows = derived checks (not caller-supplied).
- Boxes labeled **ACTIVE** are current normative; **appendix** means descriptive only.
