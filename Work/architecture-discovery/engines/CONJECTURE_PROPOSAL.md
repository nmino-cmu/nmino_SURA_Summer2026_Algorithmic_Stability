# ART-A-CONJ — Conjecture Proposal (System A)

**Artifact ID:** `ART-A-CONJ`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `OWNED_BY_DISCOVERY`  
**Owner:** Research Discovery Assistant (ART-01D)  
**Home:** `architecture-discovery/engines/`

## Purpose

Propose conjectures and falsification targets for Area-1 research packaging. Complements ART-A-ATP (automatic theorems) with human- or agent-driven conjecture authoring.

## Inputs

- Locked discovery question (A-local frontier)  
- Example / falsifier card drafts (ART-08c)  
- Characterization or stabilization intent

## Outputs

- CRP `claims[]` with conjectural maturity intent  
- `falsifiers[]` / `examples[]` drafts  
- `counterexample_claims[]` drafts (non-authoritative until B `RECORD_COUNTEREXAMPLE`)

## Ownership

System A. Role: `CONJECTURE_PROPOSER` (ART-04e). Discovery FSM S03 remains A-local.

## Permitted actions

- Author conjectures and falsification criteria  
- Package into CRP; optional soft (non-authoritative) attack search

## Prohibited actions

- Certify / promote / demote / audit verdicts  
- Close proof obligations  
- Authoritative CX mint or ControlState writes

## Relationship to CRP

Primary writer of speculative claim + falsifier payload fields.

## Relationship to verifier

B materializes Claims, ProofObligations, and authoritative CX after `SUBMIT_CANDIDATE_PACKAGE`.
