# 24 — Implementation-Neutral Interface Contracts

**Artifact ID:** `ART-24`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `ACTIVE_PARTIAL` · mutation/commit → ART-06b; CRP intake → ART-CRP; A↔B feedback schema → ART-INT-00  
**Depends on:** `ART-06b`; `ART-07c`; `ART-CRP`; `ART-01D`; `ART-INT-00` (feedback export)

> **INCOMPATIBILITY WARNING:** `I.ProposeWrite` / direct `I.HardStop` / caller `*_ok` fields are **non-authoritative**. Sole mutator = ART-06b `I.Commit`. Legacy `ResearchState.hard_stop` is a shadow — ControlState only. Discovery engines are not Commit authorities.

## Purpose
Name mandatory behavioral interfaces before implementation; no stack prescription. Cross-system feedback object shape: ART-INT `VerifierFeedbackExport`.

## Authority
**Normative write authority:** `I.Commit` only (ART-06b). Rejected commits append nothing. Sole external math intake command = `SUBMIT_CANDIDATE_PACKAGE` (ART-CRP).

## Contracts

### Mutation (ART-06b)

| Interface | Input | Output | Invariants |
|-----------|-------|--------|------------|
| `I.Commit` | `Command` (expected_state_head_digest + kind + targets + payload) | ACCEPTED / REJECTED | Sole mutator; effects derived; atomic accept; stale/hard-stop/boolean bans |

### CRP intake (ART-CRP)

| Interface | Input | Output | Invariants |
|-----------|-------|--------|------------|
| `SUBMIT_CANDIDATE_PACKAGE` | CRP / SubmissionEnvelope via Commit | IntakeReceipt | Sole external math intake; Phase A may omit MechanismInstance; idempotent on identical `crp_digest` (ART-INT I-INT-21) |
| `REJECT_CANDIDATE_PACKAGE` | crp_digest + reasons | REJECTED receipt | No Research object upserts |
| `I.DiscoverySubmit` | SubmissionEnvelope | same as SUBMIT… | **A-side alias only** — builds `SUBMIT_CANDIDATE_PACKAGE`; not a second mutation boundary |
| `I.DiscoveryStatus` | crp_digest | draft/live summary | Read-only |
| `I.LibraryExport` | filter | certified digests **or** `VerifierFeedbackExport` | Read-only; package-scoped feedback MUST use ART-INT feedback-export schema |
| `I.VerifierFeedbackExport` | crp_digest + run filter | `VerifierFeedbackExport` | Read-only; schema ART-INT-00 |

### Read / advice (no Research/Control/Design mutation)

| Interface | Input | Output | Invariants |
|-----------|-------|--------|------------|
| `I.Critique` | role + slice | Report ART-18 | No state writes |
| `I.IntegrationAudit` | advice only | structured answers draft | Persistence = ART-11b `RECORD_AUDIT` via Commit; bind to `intent_digest`; legacy IDs non-authoritative |
| `I.EIO` | evaluation context | allow/block **advice** | Commit re-derives; never caller boolean |
| `I.LeanVerify` / `I.LeanCI` | modules + pins | Manifest | Read-only |
| `I.HumanGate` | Packet | Decision stub | Deny-by-default; auth Iter4 |
| `I.CitationVerify` | lit + locator | match enums | Read/advice |
| `I.RoleCeiling` | roles + profile | derived allow | Evaluated inside Commit |
| `I.BullshitLinter` | text + snapshot | CLEAN/… | No silent ResearchState write |
| `I.CheckpointValidate` | checkpoint_id | ok flags | Read-only; trust anchor Iter10 |
| `I.EndpointMatchEvaluate` / Bridge* (ART-07c) | digests | evaluate results | Persistence via Commit |

### Deprecated names (non-operational mutators)

| Legacy name | Status |
|-------------|--------|
| `I.ProposeWrite` | Non-authoritative; use Command→`I.Commit` |
| `I.ProposeCommand` / `PendingCommand` | Removed in ITER3.1 — Command is Commit input |
| `I.Reduce` as public API | Internal to Commit only |
| `I.HardStop` direct mutator | Use Commit kinds HARD_STOP_SET/CLEAR; ControlState only |
| `I.Frontier` / `I.CXRegister` as writers | May **propose** effect payloads; apply **only** via Commit; A frontier never LOCK_CYCLE on B |

## Recovery precedence

| Situation | Precedence |
|-----------|------------|
| Commit REJECTED | No event; heads unchanged |
| CRP intake | `SUBMIT_CANDIDATE_PACKAGE` (ART-CRP) then existing B cmds |
| Promotion axis apply | `APPLY_PROMOTION` (ART-13b) or `AXIS_WRITE_FORBIDDEN` |
| EIO veto set/clear | `SET_EIO_VETO` / `CLEAR_EIO_VETO` (ART-13b); OVERRIDE_EIO HD generation-bound on APPLY |
| EIO assessment | `RECORD_EIO_ASSESSMENT` (ART-13b); **every** APPLY_PROMOTION requires intent-bound ALLOW |
| Integration audit | `RECORD_AUDIT` (ART-11b); major_milestone APPLY requires bound PASS |
| Demotion wave | Iter7 durable waves before restore/S14 |
| Corruption | Forward-fix preferred; Iter10 trust anchor |

## Non-prescriptions

No required language, DB, queue, cloud, or file format. Canonical **boundary** serialization = ART-21b via ART-INT-00.
