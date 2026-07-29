# ARCHITECTURE DESIGN BLOCK

**Status:** **ACTIVE BLOCK — architecture design only**  
**Design version:** `ARCH-0.3-REPAIR`

## Scope of this block

This block governs the **architecture design artifacts under `architecture_verifier/`,
`architecture-discovery/`, `architecture-integration/`, and `architecture-visual/`**. It does
**not** block work under `implementation/`, `lean/`, `research-results/`, or `scripts/`.

**Live and authorized (already merged on `main`):** operator implementation, the System 3 Lean
formalization runtime, certificate production and recomputation, and the research-result papers
gated on `LEAN_FULL`. Do not refuse those requests on the basis of this file.

## Blocked until human approval

1. Restructuring the Verification Architecture / Discovery Assistant **design artifacts** themselves  
2. Any claim that the architecture is “final” without `DESIGN_FINAL = approved`  
3. Treating the architecture blueprint as a frozen, audited baseline while repair iterations are incomplete

## Revoked until repair + fresh audit

- Blueprint / implementation-planning readiness  
- `AUDIT-0.3-R20` as clearance  
- C12 credit as blueprint convergence  
- Acceptance PASS labels not bound to a release digest  

See [25-audit-reports/FINAL_AUDIT.md](25-audit-reports/FINAL_AUDIT.md) and [adversarial_review_artifacts/INDEPENDENT_BREAKER_AUDIT.md](adversarial_review_artifacts/INDEPENDENT_BREAKER_AUDIT.md).

## Required human decisions (in order)

1. Complete architecture repair iterations to acceptance conditions  
2. Review frozen release + fresh independent audit evidence  
3. Set `DESIGN_FINAL = approved` in gate log (or request revisions)

## Current gate values

```text
DESIGN_FINAL = pending_human_approval
IMPLEMENTATION_START = authorized   # operator + Lean runtime merged on main
RESEARCH_EXECUTION_START = authorized   # LEAN_FULL-gated papers under research-results/
repair_phase = PACKAGE_SOL_GATE_PASS
package_sol_gate = PASS
package_release_state = NON_RELEASE
# Iter1–14 frozen; Sol package gate PASS 2026-07-24; DESIGN_FINAL still pending_human_approval
ARCHITECTURE_BLUEPRINT_READY = no
IMPLEMENTATION_PLANNING_READY = no
```

## Enforcement

Agents must refuse requests that would declare the architecture design final, or that would
rebuild the design artifacts listed under **Scope**, without the corresponding approved human
gate, and must point to this file. Requests scoped to `implementation/`, `lean/`, or
`research-results/` are outside this block and must not be refused on its account.
