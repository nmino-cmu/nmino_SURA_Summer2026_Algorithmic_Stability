# ART-A-NOV — Novelty Engine (System A)

**Artifact ID:** `ART-A-NOV`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `OWNED_BY_DISCOVERY`  
**Owner:** Research Discovery Assistant (ART-01D)  
**Home:** `architecture-discovery/engines/`

## Purpose

Score and package prior-art / novelty assessments for candidate research within Area-1. Produces literature and novelty fields that travel inside a `CandidateResearchPackage` (CRP).

## Inputs

- Draft claim statements / conjectures  
- Literature locators and citation packets  
- Optional read-only certified-library digests from B (`I.LibraryExport`)  
- Area-1 scope pin (ART-01/02)

## Outputs

- `literature_refs[]` for CRP payload  
- Novelty ladder / prior-art summary notes (`free_text_notes` or structured draft fields)  
- Recommended `profile` hint (Phase A vs B) — advisory only

## Ownership

System A only. Not on B day-1 roster (ART-04d). Role label: `NOVELTY_ENGINE` (ART-04e).

## Permitted actions

- Search / score / summarize literature  
- Assemble novelty evidence into CRP **drafts** (IR only)  
- Emit advisory `profile_hint` (ART-INT profile-map)

## Prohibited actions

- Certify claims; close proof obligations; promote/demote  
- Authoritative `RECORD_COUNTEREXAMPLE`  
- Write ResearchState / ControlState / IrreversibleSafetyLog  
- Seal CRPs or call `I.DiscoverySubmit` (Assistant only; ART-INT I-INT-64)  
- Issue audit verdicts or EIO decisions  
- `LOCK_CYCLE` / `APPLY_PROMOTION` / `ATTACH_CERTIFICATION`

## Relationship to CRP

Writes only draft payload fields. Authority begins only after B `SUBMIT_CANDIDATE_PACKAGE` succeeds (ART-CRP).

## Relationship to verifier

None except CRP submission and read-only library export. B re-checks novelty gates at APPLY (ART-14 / ART-15) independently.
