# Architecture Discovery (System A) — ownership home

**Package:** discovery profile companion to `ARCH-0.3-REPAIR` · **DUAL.2**  
**Charter:** [ART-01D](../architecture_verifier/01-charter/CHARTER_DISCOVERY.md)  
**Bridge into B:** [ART-CRP](../architecture_verifier/24-interfaces/CANDIDATE_RESEARCH_PACKAGE.md)  
**A↔B interface (authoritative):** [ART-INT-00](../architecture-integration/00-A-B-INTEGRATION.md)  
**A↔B information flow (narrative):** [DISCOVERY_VERIFIER_INFORMATION_FLOW](../architecture-visual/DISCOVERY_VERIFIER_INFORMATION_FLOW.md)  
**Operable roster (verifier day-1):** [ART-04e](../architecture_verifier/04-agents/OPERABLE_DISCOVERY.md)  
**Operable roster (A extension):** [ART-A-04e](04e-OPERABLE-ROSTER.md)  
**Readiness:** [readiness/INDEX.md](readiness/INDEX.md)  
**Information flow (narrative):** [ARCHITECTURE_INFORMATION_FLOW.md](ARCHITECTURE_INFORMATION_FLOW.md) · [canvas](/Users/nicholasmino/.cursor/projects/Users-nicholasmino-Desktop-Research-Work/canvases/discovery-information-flow.canvas.tsx)

## Frozen normative set

| Artifact | Path | Status |
|----------|------|--------|
| ART-A-00 Overall | `00-OVERALL.md` | **FROZEN** 2026-07-24 |
| ART-A-02 Internal modules | `02-INTERNAL-MODULES.md` | **FROZEN** (+ amendments) |
| ART-A-03 Session lifecycle | `03-SESSION-LIFECYCLE.md` | **FROZEN** 2026-07-25 (+2026-07-25b) |
| ART-A-04e Operable roster ext | `04e-OPERABLE-ROSTER.md` | **FROZEN** 2026-07-25 |
| ART-A-04 Discovery IR | `04-DISCOVERY-IR.md` | **FROZEN** 2026-07-25 (+2026-07-25b) |
| ART-A-05 Invocation protocol | `05-INVOCATION-PROTOCOL.md` | **FROZEN** 2026-07-25 (+2026-07-25b) |
| ART-A-06 CRP interface | `06-CRP-INTERFACE.md` | **FROZEN** 2026-07-25 (+2026-07-25b) |
| ART-A-07 Persistence/replay | `07-PERSISTENCE-REPLAY.md` | **FROZEN** 2026-07-25 (+2026-07-25b) |
| ART-A-08 Conformance | `08-CONFORMANCE.md` | **FROZEN** 2026-07-25 (+2026-07-25b) |
| Coverage matrix | `COVERAGE_MATRIX.md` | ACTIVE |

## Legacy stubs (retained)

| Artifact | Path |
|----------|------|
| ART-08 / 08b / 08c | `08-research-cycle/` |
| ART-A-NOV/ATP/MECH/CONJ | `engines/` |

**Design companion:** [`docs/superpowers/specs/2026-07-24-discovery-assistant-design.md`](../docs/superpowers/specs/2026-07-24-discovery-assistant-design.md)

## Rule

A invents and packs `CandidateResearchPackage`. Sole write into B = `SUBMIT_CANDIDATE_PACKAGE` (`I.DiscoverySubmit`). Never certify/promote/authoritative CX/ControlState writes.
