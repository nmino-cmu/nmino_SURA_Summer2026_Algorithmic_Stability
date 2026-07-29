# ART-A-ATP — Automatic Theorem Proposal (System A)

**Artifact ID:** `ART-A-ATP`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `OWNED_BY_DISCOVERY`  
**Owner:** Research Discovery Assistant (ART-01D)  
**Home:** `architecture-discovery/engines/`

## Purpose

Automatically propose theorem / lemma / corollary **candidates** (statement sketches and claim drafts) within Area-1. Preserves generative capability formerly embedded in the monolithic research cycle.

## Inputs

- Scope pin; definition drafts; open questions from Frontier / Discovery Orchestrator  
- Optional certified library digests (read-only)  
- Characterization or stabilization intent

## Outputs

- Draft `claims[]` entries for CRP (`kind` theorem/lemma/conjecture; `chain_segment`)  
- Optional `proof_sketches[]` (non-authoritative)  
- Optional obligation *hints* (become B `ProofObligation` only after intake DeriveEffects)

## Ownership

System A. Role may be exercised by `CONJECTURE_PROPOSER` / Discovery Orchestrator automation (ART-04e). This artifact is the owned module for automatic theorem proposal.

## Permitted actions

- Generate and revise candidate statements  
- Package into IR / DraftCRP inputs (Packager compiles; Assistant seals/submits)

## Prohibited actions

- Certify, promote, demote, audit, or close proof obligations  
- Authoritative CX mint; ControlState writes  
- Assert Lean status or proof floors  
- Seal CRPs or call `I.DiscoverySubmit` / act as B Committer (ART-INT I-INT-64)

## Relationship to CRP

Sole durable output path = CRP `claims[]` / `proof_sketches[]`.

## Relationship to verifier

B canonicalizes claims, generates `ProofObligation`s (ART-07b), attacks, audits, and promotes — never A.
