# 25b — Release Identity Binding (Normative)

**Artifact ID:** `ART-25b`  
**Version:** `ARCH-0.3-REPAIR-ITER14.1`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-21b · ART-ASI · ART-25 · ART-17b · ART-01 · ART-RBL  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE** until ReleaseManifest sealed  
**Self-contained:** Sole normative text for immutable release identity. Targets `B-RELEASE-IDENTITY-01` and `B-RELEASE-FALSEPASS-01`.

## Purpose

One content-addressed `ReleaseManifest` binds the package. Historical ART-21 / R20 PASS cannot imply readiness. Fresh audit + Sol package gate bind to the manifest digest — not to repair-phase pins alone.

`ponytail:` Sealing the manifest does not approve `DESIGN_FINAL`; that remains HUMAN. Envelope product PKI deferred; property = digest binding.

---

## 1. ReleaseManifest (I-REL-01)

```text
ReleaseManifest
  release_id                          # immutable label, e.g. ARCH-0.3-REPAIR-CANDIDATE
  package_version                     # single version string for the sealed set
  canonicalization_version            # MUST = ART21b.CANON.v1
  artifact_entries[]                  # sorted by path
    path                              # repo-relative
    artifact_id
    normative_status                  # ACTIVE_NORMATIVE | … at seal time
    content_digest                    # SHA-256 of file bytes (raw), hex lowercase
  fixture_root_digest                 # H over sorted fixture path+content digests (ART-21b)
  conformance_catalog_digest          # digest of ART-21b catalog id list + expected codes
  blocker_ledger_digest               # content_digest of BLOCKER_LEDGER.md at seal
  irreversible_policy_digest          # ART-17b IrreversibleKind enum digest
  sealed_at                           # ISO-8601 UTC string
  prior_release_digest?               # ⊥ for first candidate

release_digest = H("ART25b.REL.v1", release_id, package_version, canonicalization_version,
                   artifact_entries_canonical, fixture_root_digest, conformance_catalog_digest,
                   blocker_ledger_digest, irreversible_policy_digest, sealed_at,
                   prior_release_digest_or_⊥)
```

**I-REL-01b Seal path set:** `artifact_entries[]` MUST be exactly the sorted union of:
1. Every path listed as `ACTIVE_NORMATIVE` in ART-ASI (`00-repair/ARTIFACT_STATUS.md`) with a concrete file path column or standard path map below;
2. `00-repair/BLOCKER_LEDGER.md`, `00-repair/INTEGRATION_RULE.md`, `IMPLEMENTATION_BLOCK.md`, `25-audit-reports/FINAL_AUDIT.md`.

**Standard path map (authoritative for seal):**
```text
07-schemas/CANONICAL_OBJECTS.md                         ART-07b
07-schemas/TYPED_CERTIFICATES_AND_BRIDGES.md            ART-07c
06-state/MUTATION_AND_AUTHORITATIVE_STATE.md            ART-06b
04-agents/IDENTITY_AUTHORITY_INDEPENDENCE.md            ART-04c
04-agents/OPERABLE_BINDING.md                           ART-04d
13-proof-review/PROMOTION_INTENT.md                     ART-13b
11-integration-audit/AUDIT_BINDING.md                   ART-11b
11-integration-audit/PROVENANCE_BINDING.md              ART-11c
16-failure-recovery/DEMOTION_WAVES.md                   ART-16b
10-lean/LEAN_BINDING.md                                 ART-10b
08-research-cycle/CYCLE_BINDING.md                      ART-08d
17-indefinite-ops/CHECKPOINT_RESTORE.md                 ART-17b
21-acceptance-tests/CONFORMANCE.md                      ART-21b
25-audit-reports/RELEASE_IDENTITY.md                    ART-25b
00-repair/ARTIFACT_STATUS.md                            ART-ASI
00-repair/BLOCKER_LEDGER.md                             ART-RBL
```

`fixture_root_digest = H("ART25b.FIX.v1", sorted (path, content_digest) for all files under 21-acceptance-tests/fixtures/)`.  
`conformance_catalog_digest = H("ART25b.CAT.v1", sorted fixture_id, expect_or_expect_sequence)`.  
`irreversible_policy_digest = H("ART25b.IR.v1", sorted IrreversibleKind enum tokens from ART-17b)`.

**I-REL-02:** Identity immutable. Any byte change of a listed path ⇒ new manifest / new `release_digest`.
**I-REL-03:** At most one **sealed** candidate per `release_id`. Supersession uses new `release_id` + `prior_release_digest`.

---

## 2. Seal / false-pass controls (I-REL-10)

**SEAL_RELEASE_MANIFEST** (IDENTITY_ADMIN or designated RELEASE_ADMIN): Commit upserts ReleaseManifest; computes digests under ART-21b. Package remains `NON_RELEASE` until HUMAN `DESIGN_FINAL` targets this `release_digest`.

**I-REL-11 False-pass ban:** The following MUST NOT be cited as current readiness or as substitutes for a seal bound to `release_digest`:
- ART-21 T01–T24 historical PASS  
- `AUDIT-0.3-R20` / C12 under R20  
- Any `CONFORMANCE_CATALOG_PASS` bound only to a repair `package_manifest_digest` without equality to this seal’s fixture/conformance digests  
- Repair-phase ART-25 pins without `release_digest`

**I-REL-12:** ART-25 current posture fields that claim clearance MUST include `bound_release_digest = release_digest` or remain explicitly non-clearance (`NO CURRENT AUDIT PASS`).

---

## 3. Dual-dialect residual (I-REL-20)

**B-OBJ-DUAL-01 at seal:** Every ACTIVE_NORMATIVE artifact entry MUST be digest-native at its Commit boundary (ART-21b / ART-07b). Remaining descriptive ID-native prose in PENDING_MIGRATION / appendix files is allowed only with an INCOMPATIBILITY WARNING pointing to the digest-native authority. Full prose purge is not required for seal; residual dual in appendix ≠ open blocker if ACTIVE paths are digest-only.

**I-REL-21:** Checkpoint envelopes at seal cite `release_digest` in create metadata when ART-17b CheckpointRecord is extended: optional field `release_digest_at_create` (Iter14). Unsigned envelopes remain valid for repair; seal-bound ops SHOULD include the field.

---

## 4. Fresh audit binding (I-REL-30)

A **fresh package audit** for readiness evidence MUST:
1. Name `release_digest` under review.  
2. Run ART-21b catalog against that seal’s fixture digests.  
3. Record Sol (or successor) A–D combined verdict bound to `release_digest`.  
4. Not treat pre-seal internal FREEZE_OK alone as package audit PASS.

**I-REL-31:** `DESIGN_FINAL` HumanDecision `target_digest` MUST equal `release_digest`. Else gate fail.

---

## 5. Consumer deltas

| Artifact | Delta |
|----------|-------|
| ART-25 | posture may bind `bound_release_digest`; false-pass revoked claims stay revoked |
| ART-21 / 21b | historical vs seal-bound conformance |
| ART-RBL | close B-RELEASE-IDENTITY-01 / B-RELEASE-FALSEPASS-01 on freeze+seal rules present |
| ART-17b | optional release_digest_at_create |
| ART-ASI | list ART-25b |

---

## 6. Failures / traces

`RELEASE_DIGEST_MISMATCH | RELEASE_UNSEALED | FALSE_PASS_CITATION | DESIGN_FINAL_TARGET_MISMATCH`

```text
TRACE-14A  SEAL → release_digest stable under recompute
TRACE-14B  cite R20 PASS for readiness → FALSE_PASS_CITATION
TRACE-14C  DESIGN_FINAL target ≠ release_digest → reject
TRACE-14D  file byte change → release_digest changes
```
