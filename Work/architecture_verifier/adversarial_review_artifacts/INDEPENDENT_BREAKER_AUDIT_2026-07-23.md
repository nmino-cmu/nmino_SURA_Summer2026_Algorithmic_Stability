# Independent Breaker Audit — Architecture Blueprint Readiness

**Audit ID:** `BREAKER-2026-07-23`  
**Auditor posture:** Adversarial; not author; not repair agent  
**Package under review:** `/architecture` banner `ARCH-0.3-REPAIR`  
**Normative object island:** `ART-07b` `ARCH-0.3-REPAIR-ITER1.26`  
**Evidence passes:** Sol `gpt-5.6-sol` A–E (Codex CLI ephemeral) → `BREAKER_2026-07-23_pass{A..E}.txt`  
**Prior breaker:** `INDEPENDENT_BREAKER_AUDIT.md` (still directionally correct; this audit re-validates post–Iter1)

---

## 1. Executive summary

**Verdict: NOT READY as an implementation blueprint.**

Iteration 1 produced a materially stronger **object-identity island** (`ART-07b`). That island does **not** make the package implementable. The rest of the architecture still speaks a **legacy ID / unary-status / boolean-predicate** dialect (`ART-06`, `ART-08`, `ART-09`, `ART-10`, `ART-11`, `ART-12`, `ART-16`, `ART-17`, `ART-21`, `ART-24`). Repair iterations **2–14 are incomplete by the package’s own ledger**.

Five independent Sol passes all concluded **BLUEPRINT_READY? NO** (maturity **3–4/10**). Consensus maturity: **3/10**.

Finding zero critical issues would require a single digest-bound release, a mutation kernel, proof-carrying promotion, digest-bound audits, durable demotion, enforceable identity, and a reconciled object model. None of that exists end-to-end.

---

## 2. Architecture strengths (narrow; do not over-credit)

1. **Scope lock** remains explicit (finite-candidate structured perturbation → inference).  
2. **`ART-07b` Iter1.26** is a serious identity layer: content-addressed Claims, chain segments, covering-cert bridge anchor, derived proof floor, anti-laundering transforms, acyclic data-dependence core digest.  
3. **Implementation block is ACTIVE** and `DESIGN_FINAL` remains revoked — correct fail-closed posture for *execution*, not evidence of blueprint readiness.  
4. **Intent** for EIO veto, hard-stop, quarantine hop binding, and Lean-as-manifest is directionally right — mostly still **prose**.  
5. Repair program correctly refuses to treat R20/C12 as blueprint clearance.

Strengths are **local**. Blueprint readiness is **global**.

---

## 3. Top ten architectural risks

| # | Risk | Severity |
|---|------|----------|
| 1 | No authoritative mutation / commit kernel | Critical |
| 2 | Dual truth: ART-07b digests vs ART-06/11/12 IDs | Critical |
| 3 | Audit PASS unbound to claim/evidence/policy digests (TOCTOU) | Critical |
| 4 | Promotion uses caller booleans / unary status; no PromotionIntent | Critical |
| 5 | Checkpoint can validate a prefix that omits later FULL_REFUTE | Critical |
| 6 | Demotion waves non-durable / non-resumable | Critical |
| 7 | Identity/independence = agent ID labels; model provenance absent | Critical |
| 8 | HumanDecision forgeable / non-authoritative (I-HD-01) while gates required | Critical |
| 9 | ART-21 “PASS” table contradicts repair ledger (false clearance surface) | Critical |
| 10 | No single release digest; 9 coexisting version strings | Critical |

---

## 4. Critical blockers (must clear before any implementation planning)

### C1 — No authoritative mutation boundary
**Severity:** Critical · **Confidence:** High · **Subsystem:** State / interfaces  
**Failure:** Any writer can mint Claims, audits, maturity, definition heads without a single validated commit path.  
**Evidence:** ART-07b defers boundary to Iter3; ART-24 has proposal without commit contract; ART-06 already calls events “authoritative.”  
**Missing:** Exclusive command→validate→event→reduce boundary with derived predicates (no caller-trusted booleans).  
**Smallest repair:** Repair Iteration 3 as specified in the repair mandate — do not implement registries first.

### C2 — Dual object model (digest world vs ID world)
**Severity:** Critical · **Confidence:** High · **Subsystem:** Schemas / state / audit / CX / Lean  
**Failure:** Two teams implement incompatible systems; promotions against `claim_id` ignore `claim_digest` invariants.  
**Evidence:** ART-06 registries keyed by `claim_id`/`cert_id`/`bridge_id`; ART-07b requires digest identity; ART-11/12/10 consume legacy IDs; ART-07 marks itself subordinate but remains operationally referenced.  
**Missing:** One normative persistence model + migration/supersession map.  
**Smallest repair:** Rewrite ART-06/11/12/10/24 to ART-07b digests; quarantine ART-07 instance sketches until Iter2.

### C3 — Audit PASS authorizes unbound / stale claims
**Severity:** Critical · **Confidence:** High · **Subsystem:** Integration audit / promotion  
**Failure:** Audit at S₀ reused at S₁ after claim/proof/bridge/CX/policy change.  
**Evidence:** ART-11 schema binds `claim_ids[]`, not digests; no promotion-intent digest; no policy version; `blocker_if_no` author-stored; Q count inconsistency (Q1–Q16 vs Q11b/c).  
**Missing:** Frozen PromotionIntent + policy-bound applicability + freshness predicates (repair Iter5–6).  
**Smallest repair:** Bind audit to intent digest + claim_digest closure; derive blockers from policy registry.

### C4 — Promotion is not proof-carrying
**Severity:** Critical · **Confidence:** High · **Subsystem:** Promotion / theorem status  
**Failure:** Caller supplies `dep_closure_ok`, `contradiction_clear`, `eio_pass`, optional `audit_id`, unary `from_status/to_status`.  
**Evidence:** ART-06 promotion field list; ART-07b revokes unary promotion; Iter5 deferred.  
**Missing:** PromotionIntent + recomputed predicates at mutation boundary.  
**Smallest repair:** Delete caller booleans; require intent digest; recompute all predicates.

### C5 — Checkpoint validates against self-presented history
**Severity:** Critical · **Confidence:** High · **Subsystem:** Long-run / recovery  
**Failure:** Restore to prefix immediately before FULL_REFUTE; merkle of presented log “proves” freshness.  
**Evidence:** ART-17 merkle over presented events; Sol Pass B PB-04.  
**Missing:** Independent monotonic trust anchor of irreversible events (repair Iter10).  
**Smallest repair:** External append-only irreversible log (property, not product) compared at restore.

### C6 — Demotion / CX destruction not crash-safe
**Severity:** Critical · **Confidence:** High · **Subsystem:** CX / recovery  
**Failure:** Partial demotion leaves dependents promoted; ART-12 schema ≠ ART-07b CX objects; FULL CX needs CERTIFIED floor unreachable under I-HD-01.  
**Evidence:** ART-16 demotion prose; ART-07b defers Iter7; I-HD-01 blocks CERTIFIED.  
**Missing:** Durable demotion wave with cursor + completion evidence; authentic CERTIFY path (Iter4+7).  
**Smallest repair:** Wave object + block promotion while open; align CX schemas to ART-07b.

### C7 — Identity, independence, model provenance unenforceable
**Severity:** Critical · **Confidence:** High · **Subsystem:** Agents / models / gates  
**Failure:** Multiple agent IDs from one principal satisfy “Certifier ≠ Proposer”; model swap keeps audit credit.  
**Evidence:** ART-04 ID inequalities; ART-18 missing model build/prompt/tool profile; ART-07b defers Iter4; Sol Pass E.  
**Missing:** Authenticated principals + independence domains + model attestation envelopes.  
**Smallest repair:** Repair Iteration 4.

### C8 — Human gates not restart-safe / conflicting authority
**Severity:** Critical · **Confidence:** High · **Subsystem:** Human gates  
**Failure:** Stale/deny rows match mutable `target_ref`; I-HD-01 makes gates non-authoritative while ART-15 treats them as live.  
**Evidence:** ART-15 vs ART-07b I-HD-01; ART-05 “with expiry” unmet.  
**Missing:** Content-addressed decisions + digest targets + authenticity (Iter4) reconciled with ART-15.  
**Smallest repair:** Make ART-15 bind `decision_digest` + `target_digest` + approve-only; align with I-HD-01 timeline.

### C9 — False acceptance surface (ART-21)
**Severity:** Critical · **Confidence:** High · **Subsystem:** Package integrity  
**Failure:** Another team reads T16/T17 PASS (R20, C12=2) as clearance while ART-25 says reset.  
**Evidence:** ART-21 “Current status” PASS table; ART-25 `audit_pass_id=RESET_PENDING_REPAIR`, `consecutive_clean_rounds=0`.  
**Missing:** Acceptance results bound to release digest; superseded banner on ART-21.  
**Smallest repair:** Mark all historical PASSes superseded; require release-bound rerun (Iter14).

### C10 — No immutable release identity
**Severity:** Critical · **Confidence:** High · **Subsystem:** Package / versioning  
**Failure:** Nine version strings coexist; README banner cannot identify bytes.  
**Evidence:** Version scan: `ARCH-0.1-ITER1` … `ARCH-0.3-REPAIR-ITER1.26`; info-flow doc still `ARCH-0.3-ITER5`.  
**Missing:** Single release manifest with content digests (Iter14).  
**Smallest repair:** Freeze release identity only after Iter2–13; until then mark package **NON-RELEASE**.

### C11 — Research maturity can say RESULT while unproved
**Severity:** Critical · **Confidence:** High · **Subsystem:** Theorem correctness  
**Failure:** `ResearchMaturityRecord=RESULT` with `DerivedProofFloor=UNPROVED`; unproved bridge fills mandatory bridge slot.  
**Evidence:** ART-07b axes; Sol Pass D C01/C02.  
**Missing:** Axis coupling invariants + bridge proof floor for inference (Iter5 + Iter2).  
**Smallest repair:** `RESULT ⇒ floor≥CERTIFIED` (once Iter4 enables CERTIFY); inference requires proved bridge.

---

## 5. High-priority improvements (not optional for blueprint)

| ID | Issue | Repair iteration |
|----|-------|------------------|
| H1 | Certificate/bridge concrete schemas still deferred | 2 |
| H2 | Lean binds `claim_id`; incomplete staleness triggers | 8 |
| H3 | FSM not re-derived from repaired objects; `psi_data_dependence` self-field | 9 / 2 / 11 |
| H4 | Hard-stop lacks transaction fencing | 3 / 10 |
| H5 | Data-dependence factual completeness deferred; FIXED derivation can omit hidden reads | 11 |
| H6 | Over-roster vs OPERABLE_MINIMAL unresolved | 13 |
| H7 | E2E traces / acceptance not release-bound | 14 |
| H8 | Broken critique UUID links in iteration records (15 normative-side) | cleanup |
| H9 | ART-11 question-count / applicability bitmap inconsistency | 6 |
| H10 | Role lattice not an enforceable resolver | 4 / 3 |

---

## 6. Potential overengineering

- Large agent roster vs OPERABLE_MINIMAL (bureaucracy without identity enforcement).  
- Parallel registries (`certificates`, `bridges`, `utilities`) once Claims are segment-tagged.  
- Design-loop artifact sprawl (25+ ARTs) while repair says most are non-normative relative to ART-07b.  
- `ARCHITECTURE_INFORMATION_FLOW.md` as a second narrative map with stale package ID.

**Burden of proof:** keep only components that enforce an invariant ART-07b cannot express alone.

---

## 7. Potential underengineering

- Mutation kernel, PromotionIntent, audit policy registry, demotion wave, independent restore anchor, identity/independence, Lean closure binding, conformance executable — all **missing or deferred**.  
- This is underengineering of **enforceable mechanism**, not of documentation volume.

---

## 8–16. Missing components (compressed)

| Category | Missing |
|----------|---------|
| **8 Components** | Mutation boundary; PromotionIntent; AuditQuestion registry; DemotionWave; ReleaseManifest; Conformance model; ModelProvenanceRecord (live) |
| **9 Invariants** | RESULT⇒proof; audit freshness; restore vs irreversible log; independence domains; no caller-trusted booleans |
| **10 Ownership** | Who may commit; who may CERTIFY; who may release hard-stop — labels exist, authenticity does not |
| **11 Interfaces** | Commit/reduce; restore-validate; demotion-resume; model-substitute |
| **12 Audits** | Policy-versioned Q registry; intent-bound audits; invalidation triggers |
| **13 Validation** | Executable fixtures (Iter12); ART-21 currently document-presence theater |
| **14 Theorem safeguards** | Proof-carrying promotion; axis coupling; dependency demotion |
| **15 Lean safeguards** | claim_digest binding; import/proof mutation staleness; cross-axis demotion txn |
| **16 Research safeguards** | Proved bridges for inference; non-self-attested ψ dependence; CX destruction reachable under auth model |

---

## 17–21. Package integrity

| Issue | Detail |
|-------|--------|
| **17 Integrity** | Dual normative layers; acceptance PASSes contradict repair ledger |
| **18 Cross-doc** | ART-06 vs ART-07b; ART-09 non-normative but still used; ART-12 vs ART-07b CX; ART-15 vs I-HD-01; info-flow `ARCH-0.3-ITER5` |
| **19 Broken refs** | 15 broken UUID links in iteration records; many absolute path “links” in adversarial artifacts |
| **20 Versions** | 9 distinct `ARCH-*` strings live |
| **21 Acceptance** | T16/T17 claim R20/C12 while ART-25 resets; T05 obsolete vs Iter2 deferral; no release digest |

---

## 22. Traceability weaknesses

Repair acceptance conditions (22 items in the human repair mandate) map as:

| Condition family | Status |
|------------------|--------|
| Canonical objects | **Partial** (Iter1 only) |
| Typed certs/bridges | **Missing** (Iter2) |
| Mutation / Control vs Research | **Missing** (Iter3) |
| Identity / independence | **Missing** (Iter4) |
| Promotion / audits | **Missing** (Iter5–6) |
| CX/demotion | **Partial objects / missing waves** (Iter7) |
| Lean | **Partial prose** (Iter8) |
| FSM | **Legacy** (Iter9) |
| Long-run | **Unsafe** (Iter10) |
| Model/data provenance | **Missing** (Iter11) |
| Conformance | **Missing** (Iter12) |
| Minimality | **Not done** (Iter13) |
| Release integrity | **Missing** (Iter14) |

Many requirements have **definition text** without **enforcement + audit + failure owner**.

---

## 23. Long-term operation weaknesses

- Self-referential checkpoint freshness.  
- Non-resumable demotion.  
- No authenticated model substitution invalidation.  
- Hard-stop race / release non-atomic.  
- Definition-head change without atomic invalidation wave.  
- Memory/growth budgets mentioned; not tied to authoritative compaction semantics with replay equivalence.

---

## Tabletop results (mandatory scenarios)

| # | Scenario | Architecture handles it? |
|---|----------|--------------------------|
| 1 | Successful theorem discovery/promotion | **No** — promotion path legacy + Intent deferred |
| 2 | CX destroys promoted theorem | **No** — FULL CX auth blocked; demotion non-durable; schema dual |
| 3 | Definition change after proofs | **No** — pin check exists; invalidation wave prose |
| 4 | Lean rejects accepted theorem | **No** — claim_id manifest; cross-axis demotion absent |
| 5 | Inference bridge failure | **Partial** — structural bridge required; unproved bridge still slots |
| 6 | Corrupted checkpoint / omit refutation | **No** — self-validating prefix |
| 7 | Human interrupt mid-promotion | **No** — boolean hard_stop without txn fence |
| 8 | Model replacement | **No** — no provenance invalidation |
| 9 | Scope drift | **Partial** — charter gates exist; enforcement authenticity deferred |
| 10 | Data-dependent ψ introduced | **Partial** — derived class; factual omission still possible (Iter11) |

---

## Scored issue register (selected)

Each issue: Title · Severity · Confidence · Subsystem · Failure · Root cause · Evidence · Repair · Impact  
(Full Sol transcripts: `BREAKER_2026-07-23_passA..E.txt`.)

Representative Criticals: **C1–C11** above.  
Representative Highs: **H1–H10** above.

---

## 24. Overall architecture maturity

**3 / 10**

Justification: object-identity repair is real (~local 6–7/10). End-to-end enforceable research system is not (~2/10). Weighted package maturity ≈ **3/10**. Improvement vs prior breaker (~2.5) is **marginal and localized**, not blueprint-grade.

---

## 25. Readiness for implementation planning

**NO.**

Also **NO** for treating Iter1 completion as permission to draft an implementation plan. `IMPLEMENTATION_BLOCK` correctly forbids that; this audit affirms the block for **technical** reasons, not only process reasons.

---

## 26. Exactly what must change before implementation planning

1. Complete repair **Iterations 2–14** to the stated acceptance conditions (or an explicitly reduced set approved by human with equivalent invariants).  
2. Eliminate dual object models: one digest-native ART-06/08/09/10/11/12/16/17/24.  
3. Ship mutation boundary + proof-carrying promotion + intent-bound audits.  
4. Ship durable demotion + independent restore anchor.  
5. Ship identity/independence/model provenance.  
6. Reconcile HumanDecision authenticity with required gates.  
7. Produce one release digest + purge/supersede ART-21 false PASSes.  
8. Pass a **fresh** full-system breaker audit + two subsequent adversarial rounds on the **frozen** release.  
9. Human `DESIGN_FINAL` on that evidence — only then consider planning.

Until then: **do not implement; do not plan implementation; do not execute research cycles.**

---

## Why “no issues” is rejected

Extraordinary claim. Counter-evidence is abundant: deferred Iter2–14, dual schemas, ART-21 vs ART-25 contradiction, five independent NO verdicts, failed tabletops. The architecture does **not** survive adversarial review as an implementation blueprint.

---

## Auditor note on Iter1

Crediting Iter1 as “done” is compatible with this verdict. Iter1 improves the **mathematical object layer**. Blueprint readiness requires the **system layer**. Conflating the two is how false convergence happens.
