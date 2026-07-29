# Cross-Iteration Integration Rule

**Artifact ID:** `ART-RIR`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

## Mandatory invariant

A repair iteration is **not** complete merely because its new artifact is internally coherent.

Before an iteration may be marked complete, every existing normative artifact that consumes, mutates, references, validates, audits, promotes, invalidates, checkpoints, restores, formalizes, or displays the repaired objects must be classified as exactly one of:

1. **Migrated** to the repaired model.  
2. **Explicitly non-normative and quarantined.**  
3. **Scheduled** for a named later iteration with an **active incompatibility warning**.

No legacy artifact may remain silently operational against the repaired model.

## Completion report must include

- affected legacy artifacts;
- their current normative status;
- migration status;
- remaining dialect conflicts;
- temporary compatibility rules;
- prohibited uses;
- responsible later iteration;
- blocker impact;
- evidence that no undocumented compatibility assumption remains.

## Supersession

A new artifact may not silently supersede an old artifact. Supersession must be explicit and machine-trackable in principle (`supersedes_artifact_id`, `supersession_digest` when content-addressed).

## Interim normative precedence (until repair complete)

1. Repair charter / current human repair mandate — highest.  
2. `ART-07b` — canonical mathematical object identity.  
3. `ART-07c` — certificate/bridge typing.  
4. `ART-06b` — authoritative mutation / Control+Research commit semantics.  
5. `ART-04c` — identity, authority, HumanDecision, independence, CERTIFY.  
6. `ART-13b` — PromotionIntent / axis application (when ACTIVE).  
7. `ART-11b` — Audit policy / intent-bound audit (when ACTIVE).  
8. Any legacy artifact conflicting with ART-07b/07c/06b/04c/13b/11b is **non-authoritative** for those scopes.  
9. Legacy artifacts may remain authoritative only for unrepaired concepts.  
10. Future-scheduled legacy artifacts must display an incompatibility warning.  
11. Historical audit/acceptance records = process history only, **not readiness**.  
12. Unresolved conflicts → **fail-closed**.  
13. In conflict, choose fail-closed.

## Artifact normative-status labels

| Label | Meaning |
|-------|---------|
| `ACTIVE_NORMATIVE` | Authoritative for its scope |
| `ACTIVE_PARTIAL` | Authoritative for unrepaired subset; conflicts fail-closed to ART-07b / repair artifacts |
| `QUARANTINED_LEGACY` | Non-authoritative; must not authorize promotion/audit PASS |
| `HISTORICAL_EVIDENCE` | Process history only |
| `SUPERSEDED` | Replaced; do not use |
| `DRAFT_REPAIR` | Under repair review; not frozen |
| `PENDING_MIGRATION` | Still operationally referenced; migration scheduled; unsafe for readiness |

## Fail-closed default

If classification is missing → treat as `QUARANTINED_LEGACY` for readiness and promotion authorization.
