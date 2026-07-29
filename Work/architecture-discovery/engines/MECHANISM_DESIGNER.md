# ART-A-MECH — Mechanism Designer (System A)

**Artifact ID:** `ART-A-MECH`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `OWNED_BY_DISCOVERY`  
**Owner:** Research Discovery Assistant (ART-01D)  
**Home:** `architecture-discovery/engines/`

## Purpose

Specify structured perturbation / selection-mechanism **proposals** (\(Q_\psi\) schemas, operators, domains) for packaging into CRPs. Preserves Mechanism Designer functionality outside the verifier.

## Inputs

- Optimization / selection problem drafts  
- Score constructions; neighbor/oracle intent  
- Phase B / MIXED packaging intent (Phase A may skip this module)

## Outputs

- CRP `mechanism_proposals[]` (draft MechanismInstance bodies)  
- Related definition / assumption drafts  
- Optional certificate_drafts for stability paths (non-authoritative until B)

## Ownership

System A. Role: `MECHANISM_DESIGNER` (ART-04e).

## Permitted actions

- Design and revise mechanism schemas  
- Emit Phase B / MIXED CRP payloads requiring mechanisms (ART-CRP I-CRP-05)

## Prohibited actions

- Certify mechanisms or stability certificates in B  
- Close obligations; promote/demote; authoritative CX  
- Write verifier ControlState / ResearchState  
- Force MechanismInstance onto Phase A characterization packages

## Relationship to CRP

`mechanism_proposals[]` optional for `PHASE_A_CHARACTERIZATION` / `OBLIGATION_ONLY`; required for `PHASE_B_STABILIZATION` at B intake.

## Relationship to verifier

B types MechanismInstance via ART-07b I-MECH / I-CERT-01 after intake. A never APPLYs.
