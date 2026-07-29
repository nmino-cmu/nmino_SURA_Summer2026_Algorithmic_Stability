# ART-A-04e — Discovery Operable Roster Extension (System A)

**Artifact ID:** `ART-A-04e`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `FROZEN`  
**Frozen:** `2026-07-25`  
**Owner:** Research Discovery Assistant (ART-01D)  
**Home:** `architecture-discovery/`  
**Depends on:** ART-A-00 · ART-A-02 · ART-01D · cites verifier ART-04e (read-only)  
**Does not modify:** `architecture_verifier/**` including ART-04e

## Purpose

Extend the System A operable roster for implementers beyond the historical day-1 list in verifier ART-04e, without editing the frozen Verification Architecture tree.

## Non-goals

- Grant B ResearchState/ControlState Commit rights  
- Change CRP `author_kind` enum  
- Replace verifier ART-04e (remains historical ceiling until a future human gate updates it)

## Principles

**I-A04e-01** Discovery roles never appear as B Commit `roles_invoked` except as CRP `author_*` digests.  
**I-A04e-02** Sole B write remains `I.DiscoverySubmit` → `SUBMIT_CANDIDATE_PACKAGE`.  
**I-A04e-03** This document is authoritative for **System A implementation roster**; verifier ART-04e is cited, not amended.

## Roster (A implementer)

| role_id | Notes |
|---------|--------|
| RESEARCH_DISCOVERY_ASSISTANT | Authorship + seal (ART-A-00/A-02) |
| DISCOVERY_ORCHESTRATOR | FSM control owner |
| FRONTIER_SCHEDULER | A-local frontier; never B LOCK_CYCLE |
| MECHANISM_DESIGNER | ART-A-MECH |
| NOVELTY_ENGINE | ART-A-NOV |
| LITERATURE_ANALYST | Lit search (maps with NOVELTY_LITERATURE module) |
| CONJECTURE_PROPOSER | ART-A-CONJ |
| AUTOMATIC_THEOREM_PROPOSAL | ART-A-ATP |
| OPERATOR_ANALYZER | First-class (ART-A-00) |
| STRUCTURAL_QUANTITY | Quantity discovery |
| PROOF_SKETCHER | Proof sketches |
| SOFT_ATTACK | Non-authoritative soft attack |
| PORTFOLIO_MANAGER | Pareto frontier |
| CRP_PACKAGER | Deterministic packager |
| DISCOVERY_IR | Store / structural records |

## API surface (unchanged semantics; feedback schema ART-INT)

```text
I.DiscoverySubmit(envelope) → SUBMIT_CANDIDATE_PACKAGE only
I.DiscoveryStatus(digest) → read-only
I.LibraryExport(filter) → read-only (may return VerifierFeedbackExport)
I.VerifierFeedbackExport → read-only (ART-INT)
```

**Module role aliases (I-A04e-04):** `NOVELTY_ENGINE` ≡ ART-A-02 module `NOVELTY_LITERATURE`; `CONJECTURE_PROPOSER` ≡ `CONJECTURE_ENGINE`. Roster labels may differ from module taxonomy names; contracts bind responsibilities.

## Illegal

Any B mutation except sealed CRP submit path; FRONTIER_SCHEDULER LOCK_CYCLE on B; Orch APPLY_PROMOTION.

## Audit

Ownership aligns with ART-A-02 modules; no verifier file modified; author_kind unchanged.

## Changelog

2026-07-25: Initial freeze — A-owned extension for new modules.
