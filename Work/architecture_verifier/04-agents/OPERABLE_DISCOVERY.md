# 04e — Discovery Operable Profile (Normative)

**Artifact ID:** `ART-04e`  
**Version:** `ARCH-0.3-REPAIR-DUAL.1`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-01D · ART-04c · ART-CRP  
**Package:** discovery profile · **NON-RELEASE**  
**Self-contained:** System A day-1 roster. **No** ResearchState Commit rights.

## Purpose

Hard ceiling for Discovery Assistant roles. These principals may assemble and author CRPs; they do **not** appear as Commit `roles_invoked` on B Research/Control/Irreversible stores (except as CRP `author_*` digests).

## Day-1 A roles (I-OD-01)

| # | role_id / label | Notes |
|---|-----------------|--------|
| 1 | RESEARCH_DISCOVERY_ASSISTANT | CRP author_kind; seals packages |
| 2 | DISCOVERY_ORCHESTRATOR | A-local session drive (not B VERIFICATION_ORCHESTRATOR) |
| 3 | FRONTIER_SCHEDULER | A question selection only; never LOCK_CYCLE on B |
| 4 | MECHANISM_DESIGNER | ART-A-MECH — propose mechanisms in CRP |
| 5 | NOVELTY_ENGINE | ART-A-NOV — lit/novelty packaging |
| 6 | LITERATURE_ANALYST | Discovery lit search (B re-checks at APPLY) |
| 7 | CONJECTURE_PROPOSER | ART-A-CONJ — conjecture drafts in CRP |
| 8 | AUTOMATIC_THEOREM_PROPOSAL | ART-A-ATP — auto theorem/lemma candidates |

**Forbidden for A (I-OD-02):** any `command_kind` that mutates B ResearchState / ControlState / IrreversibleSafetyLog except by submitting CRP through a B Committer acting as `VERIFICATION_ORCHESTRATOR` or `HUMAN_GATE_OPERATOR`.

## API surface

```text
I.DiscoverySubmit(envelope) → builds SUBMIT_CANDIDATE_PACKAGE only
I.DiscoveryStatus(digest)   → read-only
I.LibraryExport(filter)     → read-only certified digests or ART-INT VerifierFeedbackExport
I.VerifierFeedbackExport    → read-only package-scoped feedback (ART-INT-00)
```

Cross-system interface: `architecture-integration/00-A-B-INTEGRATION.md` (ART-INT-00).

## Traces

```text
TRACE-04E-A  FRONTIER_SCHEDULER LOCK_CYCLE on B → ROLE_CEILING
TRACE-04E-B  DISCOVERY_ORCHESTRATOR APPLY_PROMOTION → ROLE_CEILING
TRACE-04E-C  RESEARCH_DISCOVERY_ASSISTANT seals CRP → author OK
```
