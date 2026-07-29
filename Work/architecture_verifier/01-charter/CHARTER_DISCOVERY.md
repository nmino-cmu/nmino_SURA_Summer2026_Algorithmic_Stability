# 01D — Research Discovery Assistant Charter

**Artifact ID:** `ART-01D`  
**Version:** `ARCH-0.3-REPAIR-DUAL.1`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE** (discovery profile)  
**Depends on:** ART-01 (shared Area-1 scope) · ART-CRP  
**Authority:** Immutable except by human gate `SCOPE_CHANGE` or `DESIGN_FINAL` amendment  

## Purpose

Bind the **Research Discovery Assistant** (System A) to creative mathematical assistance within Area-1.

Mission: invent, search, prioritize, and **package** Candidate Research Packages.  
It does **not** mutate Verification Architecture ResearchState.

## Scope

Same Area-1 math program as ART-01. May propose Phase A characterization packages and Phase B stabilization packages.

## Goals (A)

1. Generate research ideas, conjectures, mechanisms, bridges, experiments.  
2. Literature / novelty assistance.  
3. Frontier / question selection.  
4. Autonomous discovery workflows (local to A).  
5. Assemble and seal `CandidateResearchPackage` for B or for human review.  
6. Optional non-authoritative soft attack search.

## Non-goals (A)

- Authoritative promotion, certification, demotion, or CX mint in B  
- Writing ControlState / IrreversibleSafetyLog  
- Bypassing CRP intake  

## Inputs

- Human guidance; read-only certified library exports from B  
- Literature as prior-art source  

## Outputs

- Sealed `CandidateResearchPackage` documents  
- Discovery session logs (non-authoritative for B)

## Invariants

- A never calls `APPLY_PROMOTION`, authoritative `RECORD_COUNTEREXAMPLE`, or direct ResearchState upserts  
- Sole write path into B is `SUBMIT_CANDIDATE_PACKAGE` (via authenticated Committer)

## Relation

Shared Area-1: ART-01. Verification charter: ART-01V. Intake schema: ART-CRP. Operable roster: ART-04e.
