# Artifact Normative Status Index

**Artifact ID:** `ART-ASI`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE** · **DUAL.2**  
**Precedence:** [INTEGRATION_RULE.md](INTEGRATION_RULE.md)  
**Dual-system plan:** [DUAL_SYSTEM_SEPARATION_PLAN.md](DUAL_SYSTEM_SEPARATION_PLAN.md)

| Artifact | Status | Notes |
|----------|--------|-------|
| ART-01 CHARTER | ACTIVE_PARTIAL | Shared Area-1 constitution; `admissible_package` |
| ART-01V CHARTER_VERIFICATION | ACTIVE_NORMATIVE | System B mission |
| ART-01D CHARTER_DISCOVERY | ACTIVE_NORMATIVE | System A mission |
| ART-CRP CANDIDATE_RESEARCH_PACKAGE | ACTIVE_NORMATIVE | Sole external math intake; ART-07b §10A |
| ART-02 MATH_SCOPE | PENDING_MIGRATION | Operator transfer → ART-07c |
| ART-03 SYSTEM_CONTEXT | PENDING_MIGRATION | A↔CRP↔B |
| ART-04 AGENT_ROLES | ACTIVE_PARTIAL | Dual-system roster labels; authenticity ART-04c |
| ART-04d OPERABLE_BINDING | ACTIVE_NORMATIVE | B day-1; VERIFICATION_ORCHESTRATOR |
| ART-04e OPERABLE_DISCOVERY | ACTIVE_NORMATIVE | A roster + ART-A-* engines |
| ART-04b OPERABLE_MINIMAL | PENDING_MIGRATION | Descriptive; authority=ART-04d |
| ART-04c IDENTITY_AUTHORITY | ACTIVE_NORMATIVE | No RESEARCH_ORCHESTRATOR alias (DUAL.2) |
| ART-A-NOV / ATP / MECH / CONJ | OWNED_BY_DISCOVERY | `architecture-discovery/engines/` |
| ART-05 | ACTIVE_PARTIAL | Lattice; HD authenticity ART-04c |
| ART-06 STATE_MODEL | QUARANTINED_LEGACY | Superseded by ART-06b |
| ART-06b MUTATION_STATE | ACTIVE_NORMATIVE | + SUBMIT/REJECT_CANDIDATE_PACKAGE |
| ART-07 SCHEMAS | QUARANTINED_LEGACY | Instance sketches |
| ART-07b CANONICAL_OBJECTS | ACTIVE_NORMATIVE | characterization + CRP/IntakeReceipt/ProofObligation |
| ART-07c TYPED_CERTS_BRIDGES | ACTIVE_NORMATIVE | Iter2.7 |
| ART-08d CYCLE_BINDING | ACTIVE_NORMATIVE | LOCK_CYCLE optional; VERIFICATION_ORCHESTRATOR |
| ART-08 / 08b / 08c | OWNED_BY_DISCOVERY | `architecture-discovery/`; stubs in B tree |
| ART-09 | QUARANTINED_LEGACY | Unary status; superseded by ART-13b |
| ART-10b LEAN_BINDING | ACTIVE_NORMATIVE | Iter8 |
| ART-10 | PENDING_MIGRATION | Descriptive; authoritative = ART-10b |
| ART-11 | PENDING_MIGRATION | Descriptive; authoritative = ART-11b |
| ART-11b AUDIT_BINDING | ACTIVE_NORMATIVE | Profile routing; CHAR Q04/Q17 overrides |
| ART-11b-CHAR | ACTIVE_NORMATIVE | Characterization audit profile |
| ART-11c PROVENANCE_BINDING | ACTIVE_NORMATIVE | Iter11 |
| ART-12 | PENDING_MIGRATION | CX register; demotion → ART-16b |
| ART-12-CHAR | ACTIVE_NORMATIVE | Characterization CX profile |
| ART-13 | ACTIVE_PARTIAL | Review labels; promotion → ART-13b |
| ART-13b PROMOTION_INTENT | ACTIVE_NORMATIVE | + I-AP-PO / OBLIGATION_UNRESOLVED |
| ART-18 / 19 / 23 | ACTIVE_PARTIAL | Validation prose |
| ART-15 | ACTIVE_PARTIAL | Gate registry |
| ART-16b DEMOTION_WAVES | ACTIVE_NORMATIVE | Iter7 |
| ART-17b CHECKPOINT_RESTORE | ACTIVE_NORMATIVE | Iter10 |
| ART-16 / 17 | PENDING_MIGRATION | Demotion→16b; restore→17b |
| ART-20 | PENDING_MIGRATION | Invariants → ART-06b/07c |
| ART-21b CONFORMANCE | ACTIVE_NORMATIVE | CF-CRP-* / CF-CHAR-* / CF-PO-BLOCK |
| ART-21 | HISTORICAL_EVIDENCE | conformance→21b |
| ART-22 | PENDING_MIGRATION | Traces; A→CRP→B |
| ART-24 | ACTIVE_PARTIAL | I.Commit + CRP / I.DiscoverySubmit |
| ART-25b RELEASE_IDENTITY | ACTIVE_NORMATIVE | Iter14; seal pending human |
| ART-25 | ACTIVE_NORMATIVE | Repair posture |
| Info-flow | PENDING_MIGRATION | Narrative; A↔CRP↔B |
| IMPLEMENTATION_BLOCK | ACTIVE_NORMATIVE | ACTIVE |
| ART-RBL / ART-RIR / ART-ASI | ACTIVE_NORMATIVE | Repair plane |
| Breaker audits | HISTORICAL_EVIDENCE | Not final audits |

**INCOMPATIBILITY WARNING:** Prefer ART-07b/07c/06b/04c/13b/CRP + fail-closed. Discovery engines are not B Commit authorities.

**DUAL.2 targeted repair:** discovery engines owned; CRP/PO registered; CHAR CX/audit profiles; verifier role rename; stale autonomous-system docs scrubbed. `DESIGN_FINAL` still human-gated.
