# 21b — Conformance Binding (Normative)

**Artifact ID:** `ART-21b`  
**Version:** `ARCH-0.3-REPAIR-ITER12.1`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-07b · ART-07c · ART-06b · ART-13b · ART-11b · ART-11c · ART-04c · ART-16b · ART-17b · ART-01  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative text for hash suite, canonicalization, and executable conformance fixtures. Closes ART-07b §1.2 algorithm deferral. Supersedes ART-21 T-suite for repair-package checks only.

## Purpose

Pin `H` + canonical serialization so digests are interoperable. Bind a minimal fixture catalog with locked golden digests and concrete command sequences. Executable harness is a **design interpreter** for fixtures — not research execution, not blueprint clearance.

`ponytail:` Full Q02–Q17 prompt evaluators and migration replay suites remain optional expansions. Release-bound digests = ART-25b. This artifact’s PASS ≠ `DESIGN_FINAL`.

---

## 1. Hash suite

**I-H-01:** `H(bytes) = SHA-256(bytes)` → 32-byte digest; hex lowercase UTF-8 when embedded in JSON.  
**I-H-02:** Normative `H(...)` in this package means I-H-01 over the multi-arg packing in I-H-03, unless the call site says `H(canonical_serialization(obj))` (then I-CAN-02).  
**I-H-03 Multi-arg packing:** `H(a0, a1, …, an)` = `SHA-256(canonical_serialization([a0,…,an]))` where the list is a JSON array; nested objects/arrays use I-CAN-01; byte strings appear as hex lowercase JSON strings when they are digests.  
**I-H-04:** `canonicalization_version = "ART21b.CANON.v1"`.

---

## 2. Canonical serialization (I-CAN-01)

`canonical_serialization(obj)` → UTF-8 bytes of JSON:

1. Object keys sorted lexicographically (UTF-8 byte order).  
2. Arrays preserve specified normative order; when a rule says “sorted”, sort by canonical JSON of elements.  
3. Absent optional field ⇒ key omitted (never `null`).  
4. No `null` values; use omission or typed token `"⊥"` only where a schema allows it.  
5. Numbers: integers as JSON numbers without exponent; forbid floats in normative fields.  
6. Strings: UTF-8; escape per RFC 8259.  
7. Compact JSON (no insignificant whitespace).

**I-CAN-02 Top-level object digest:** `SHA-256( UTF-8("ART21b.CANON.v1") || 0x00 || canonical_serialization(obj) )`.  
Domain-tagged digests that begin with a literal tag via I-H-03 (`H("ART16b.DW.v4", …)`) do **not** also apply I-CAN-02.

**I-CAN-03:** Unknown keys in a normative payload ⇒ `UNKNOWN_FIELD`.

---

## 3. Golden digest vectors (I-GV-01)

Authoritative bodies: `21-acceptance-tests/fixtures/GV-*.json` with `input` + `expected_digest_hex` locked under I-H-01..04 / I-CAN-01..02. Recompute MUST match. Mismatch ⇒ `DIGEST_MISMATCH`. First-run lock forbidden after freeze.

| Vector ID | Digest rule |
|-----------|-------------|
| GV-CLAIM, GV-PI, GV-AUDIT, GV-CMD, GV-DDV, GV-CP | I-CAN-02 over `input` |
| GV-DW | I-H-03 `H("ART16b.DW.v4", trigger_kind, trigger_digest, seeds, work_items)` from `input` |

---

## 4. Harness interface (I-CF-01)

```text
I.ConformanceRun
  input:  fixture_id, package_manifest_digest
  output: { pass: bool, code?, observed_digest?, expected_digest? }
```

**I-CF-02:** Ephemeral in-memory replay only; MUST NOT write durable research stores or clear `IMPLEMENTATION_BLOCK`.  
**I-CF-03:** `package_manifest_digest = H` (I-H-03) over sorted `(path, content_digest)` pairs of ACTIVE_NORMATIVE repair artifacts in ART-ASI.  
**I-CF-04:** Catalog PASS ⇒ `CONFORMANCE_CATALOG_PASS` for that manifest only — **not** `DESIGN_FINAL` / blueprint / release.

**Harness-local ops** (not ResearchState command_kinds): `EVAL_BRIDGE`, `EVAL_CERT_USE`, `I.CheckpointValidate` — pure evaluators over fixture state.  
**I-CF-05:** CF-* bodies are **design oracles** (initial_state + intended command_kind + expect codes). They are not required to be byte-executable Commit transcripts until `IMPLEMENTATION_START`. Executable bar for package gate = GV-* digest lock + CF expect-code catalog consistency. No second schematic command dialect.

---

## 5. Fixture catalog

Authoritative bodies under `21-acceptance-tests/fixtures/CF-*.json`. Each MUST include `initial_state`, `commands[]`, and `expect` or `expect_sequence`.

| ID | Expect |
|----|--------|
| CF-3A | SUCCESS |
| CF-3B | CALLER_BOOLEAN_FORBIDDEN |
| CF-3C | SUCCESS (+ hard_stop active) |
| CF-3D | STALE_WRITE |
| CF-3F | REJECT |
| CF-3G | HARD_STOP_ACTIVE |
| CF-F2-OK | SUCCESS |
| CF-F2-02 | TYPED_REJECT |
| CF-F2-09 | PROOF_FLOOR_INSUFFICIENT |
| CF-Q01 | SUCCESS |
| CF-Q11 | SUCCESS |
| CF-AUDIT-CARD | UNKNOWN_AUDIT_QUESTION |
| CF-DDV-OK | VERIFIED |
| CF-DD-CORE | DD_CORE_MISMATCH |
| CF-MP-STALE | MODEL_PROV_STALE |
| CF-7A | SUCCESS (seed SUPERSEDED) |
| CF-10A | IRREVERSIBLE_PREFIX |
| CF-10C | SUCCESS then DEMOTION_WAVE_OPEN |
| CF-AP-BOOL | CALLER_BOOLEAN_FORBIDDEN |
| CF-AP-CX | CX_BLOCKS_PROMOTION |
| CF-CRP-A | SUCCESS (Phase A, no mechanism) |
| CF-CRP-B | MECHANISM_REQUIRED |
| CF-CRP-C | CRP_AUTHOR |
| CF-CRP-REG | SUCCESS (CRP/IntakeReceipt/ProofObligation registered) |
| CF-CRP-HUMAN | SUCCESS (HUMAN Phase A + obligations) |
| CF-CRP-ASSIST | SUCCESS (ASSISTANT Phase A) |
| CF-CHAR-CX-OK | SUCCESS (characterization audit PASS, Q04=NA) |
| CF-CHAR-CX-NEG | FAIL_OR_FULL_CX (omit-ties / bad radius) |
| CF-PO-BLOCK | OBLIGATION_UNRESOLVED |

**I-CF-10:** Missing/empty `commands` on CF-* ⇒ `FIXTURE_MISSING`. Missing `expected_digest_hex` on GV-* ⇒ `FIXTURE_MISSING`. CF-* fixtures do **not** require `expected_digest_hex`.

---

## 6. ART-21 supersession

ART-21 T01–T24 remain HISTORICAL_EVIDENCE. Repair conformance = this catalog. **Release rebinding** = ART-25b (`release_digest` / I-REL-11); seal-bound conformance MUST use fixture digests equal to the sealed `fixture_root_digest` / `conformance_catalog_digest`.

---

## 7. Consumer deltas

| Artifact | Delta |
|----------|-------|
| ART-07b §1.2 | H + canon = this artifact |
| ART-21 | historical only |
| ART-25 | may record CONFORMANCE_CATALOG_PASS + manifest; not clearance |
| B-OBJ-DUAL-01 | PARTIAL — boundary digests; legacy ID purge →14 |

---

## 8. Failures / traces

`DIGEST_MISMATCH | UNKNOWN_FIELD | FIXTURE_MISSING | CONFORMANCE_CATALOG_PASS | CANON_VERSION_MISMATCH`

```text
TRACE-12A  GV-* digests stable
TRACE-12B  CF-3B → CALLER_BOOLEAN_FORBIDDEN
TRACE-12C  CF-DD-CORE → DD_CORE_MISMATCH
TRACE-12D  catalog PASS ⇏ DESIGN_FINAL
TRACE-CRP-A  CF-CRP-A → SUCCESS
TRACE-CRP-B  CF-CRP-B → MECHANISM_REQUIRED
TRACE-CRP-C  CF-CRP-C → CRP_AUTHOR
TRACE-CRP-REG  CF-CRP-REG → SUCCESS
TRACE-CHAR-OK  CF-CHAR-CX-OK → PASS
TRACE-CHAR-NEG CF-CHAR-CX-NEG → FAIL_OR_FULL_CX
TRACE-PO-BLOCK CF-PO-BLOCK → OBLIGATION_UNRESOLVED
```
