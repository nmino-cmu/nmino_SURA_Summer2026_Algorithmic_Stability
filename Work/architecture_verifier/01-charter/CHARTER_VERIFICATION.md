# 01V — Verification Architecture Charter

**Artifact ID:** `ART-01V`  
**Version:** `ARCH-0.3-REPAIR-DUAL.1`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Depends on:** ART-01 (shared Area-1 scope pins) · ART-CRP · ART-06b  
**Authority:** Immutable except by human gate `SCOPE_CHANGE` or `DESIGN_FINAL` amendment  

## Purpose

Bind the **Verification Architecture** (System B) to Area-1 mathematical knowledge management.

Mission: **verify, certify, govern, and persist** mathematical artifacts.  
It does **not** autonomously invent research questions, mechanisms, or conjectures.

## Scope

Same Area-1 math program as ART-01 shared constitution: structured finite-candidate selection / stability / composition / inference — including **Phase A characterization** work that does not yet introduce a perturbation mechanism.

## Goals (B)

1. Accept `CandidateResearchPackage` from humans or the Discovery Assistant only.  
2. Canonicalize and schema-validate intake.  
3. Maintain digest-native objects, dependencies, assumptions.  
4. Search counterexamples; demote on FULL CX.  
5. Audit, Lean-bind, promote/demote maturity.  
6. Certify reusable artifacts; durable checkpoint/restore.  
7. Enforce human gates on verification-side promotions and control.

## Non-goals (B)

- Choosing the next research question or frontier score  
- Mechanism / conjecture / novelty generation  
- Running an autonomous discovery cycle  
- Speculative invention (that is System A)

## Inputs

- `CandidateResearchPackage` (sole external mathematical intake)  
- HumanDecision / hard-stop / release gates  
- Read-only literature only when cited inside a CRP

## Outputs

- Live ResearchState / ControlState / certified library  
- Reject / demotion / audit records  

## Invariants

- No ResearchState mutation outside `I.Commit`  
- No caller-authoritative `*_ok`  
- Discovery engines are not on the B normative path  
- Phase A CRPs need not include `MechanismInstance`  

## Human gates

`DESIGN_FINAL`, `SCOPE_CHANGE`, promotion-related ART-15 gates, `HARD_STOP` / `HARD_STOP_RELEASE`, etc. (ART-15).

## Relation

Shared Area-1 predicates: ART-01. Discovery charter: ART-01D. Intake: ART-CRP.
