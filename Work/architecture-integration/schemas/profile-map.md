# Profile / candidate-type map (ART-INT)

**Authority:** ART-INT-00. CRP profile enum owned by ART-CRP.

| Discovery candidate / intent | Admissible in CRP? | Required fields (beyond ART-CRP baseline) | CRP `profile` | Mechanism | Audit/CX | Notes |
|------------------------------|--------------------|---------------------------------------------|---------------|-----------|----------|-------|
| Instability characterization | Yes | claims with `chain_segment=characterization` | `PHASE_A_CHARACTERIZATION` | Optional empty | ART11b.CHAR / ART-12-CHAR | |
| Structural quantity claim | Yes | claim payload typed quantity | `PHASE_A_CHARACTERIZATION` or `MIXED` | Optional | CHAR if pure | |
| Perturbation mechanism proposal | Yes | `mechanism_proposals[]` nonempty | `PHASE_B_STABILIZATION` or `MIXED` | Required if Phase B | BASE / MIXED | |
| Stabilization claim | Yes | stability segment + mechanism | `PHASE_B_STABILIZATION` | Required | ART11b.BASE | |
| Theorem / lemma conjecture | Yes | claims[] + optional sketches | Per intent Phase A/B/MIXED | Per profile | Per profile | |
| Bridge theorem | Yes | bridge_proposals / bridge segment | `BRIDGE_ONLY` or `MIXED` | Only if stability included | ART11b.BRIDGE | |
| Utility tradeoff | Yes | utility-related claims | Usually Phase B / MIXED | Per stability | BASE | |
| Impossibility claim | Yes | characterization or other segment | Often Phase A | Optional | CHAR | |
| Algorithm-specific proposition | Yes | operator bindings | Per segment | Per profile | | |
| Characterization-only package | Yes | no mechanism | `PHASE_A_CHARACTERIZATION` | Empty OK | CHAR | I-CRP-02 |
| Obligation-only | Yes | obligation-facing claims | `OBLIGATION_ONLY` | Empty OK | CHAR | |

**I-INT-PR-01:** `PortfolioMember.profile_hint` MUST be one of the ART-CRP profile enum values (or map via fixed table below). Illegal hint ⇒ CompileError `PROFILE_MISMATCH`.

### profile_hint normalization

| profile_hint (A) | CRP profile |
|------------------|-------------|
| `PHASE_A_CHARACTERIZATION` | same |
| `PHASE_B_STABILIZATION` | same |
| `MIXED` | same |
| `OBLIGATION_ONLY` | same |
| `BRIDGE_ONLY` | same |
| `PHASE_A` / `characterization` | `PHASE_A_CHARACTERIZATION` |
| `PHASE_B` / `stabilization` | `PHASE_B_STABILIZATION` |
| other | CompileError |

**I-INT-PR-02:** Packager MUST NOT invent mechanisms to satisfy Phase B; missing ⇒ CompileError (A) or MECHANISM_REQUIRED (B) if wrongly sealed.
