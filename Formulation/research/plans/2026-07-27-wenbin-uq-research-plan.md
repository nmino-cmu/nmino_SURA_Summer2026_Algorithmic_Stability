---
name: wenbin-uq-research-execution
overview: "Execute Wenbin-narrowed UQ problem only — Part I LOO stability of constrained opt (2) → Part II post-hoc validity of (1) at θ̂, with goal (iii) via data-randomize selection (W5, no recalibration of C). All artifacts under research/; writeup/ and context/ frozen."
todos:
  - id: lit-pattern-mine
    content: "Phase 0 — Mine stability→post-selection validity, randomization/noise-for-stability, and inverse-opt structured-noise patterns from priority + CRC/CREDO-as-methods literature; write digests under research/literature/"
    status: completed
  - id: formal-part-i
    content: "Phase 1 — Formalize Part I — LOO stability notions for θ̂(D) from (2); state assumptions on f̂,ĝ; candidate lemmas under research/formal/"
    status: in_progress
  - id: formal-part-ii
    content: "Phase 2 — Formalize Part II — validity inflation bounds; conditions for (1) at θ̂; randomized selection map (no C recalibration) under research/formal/"
    status: in_progress
  - id: proof-sketches
    content: "Phase 3 — Proof sketches → tighten → self-checks (assertable lemmas / Lean or Python) under research/proofs/ and research/experiments/"
    status: pending
  - id: audit-gates
    content: "Phase 4 (continuous) — Multi-agent audit after every deliverable — Wenbin coverage, scope creep, assumption warrant, math correctness under research/audit/"
    status: pending
  - id: sol-hard-gaps
    content: "Phase 5 (on-demand) — Reserve Sol/Codex CLI only for hardest proof gaps; log prompts/results under research/proofs/sol_gaps/"
    status: in_progress
  - id: integrate-methods
    content: "Phase 6 — Integrate W5 method candidates (PTO-style data-driven policy, data-randomize, structured noise / inverse opt) as selection mechanisms answering (iii) only — not as problem expansion"
    status: pending
isProject: false
---

# Wenbin UQ Execution Plan — Stability → Post-Hoc Validity (No Recalibration)

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to execute this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Using writing-plans skill** to produce an execution-only research plan (not prose essay).

**Goal:** Answer frozen writeup goals (i)–(iii) for plugging \(\hat\theta(\mathcal{D})\) from constrained opt (2) into validity (1), with Part I = LOO stability of (2), Part II = post-hoc validity, and (iii) restored **only** by data-randomizing selection (**no** recalibration of \(\mathcal{C}\); Wenbin W5).

**Architecture:** Literature pattern extraction → formal Part I → formal Part II → proof sketches + machine-checkable self-checks → continuous 4-gate audits after every deliverable. Sol/Codex CLI is reserved for stubborn proof gaps only.

**Tech Stack:** Markdown + LaTeX fragments under `research/`; optional Python assert-demos under `research/experiments/`; optional Lean stubs under `research/proofs/lean/` if a lemma is small enough; `codex exec --ephemeral -s read-only -m gpt-5.6-sol` for hard gaps only.

## Global Constraints

- **Scope ceiling = frozen writeup only:** `/Users/nicholasmino/Desktop/Research/Formulation/writeup/Problem_Writeup.tex` (+ PDF). Equations (1)–(2), goals (i)–(iii) with W5 override on (iii), Part I / Part II as written.
- **FROZEN — never edit:** `writeup/**`, `context/**` (see `research/FREEZE.md`, `research/FROZEN_CHECKSUMS.txt`).
- **All new artifacts:** `research/{notes,formal,proofs,audit,literature,experiments,plans}/` only.
- **Selected object:** only \(\hat\theta(\mathcal{D})\) from (2) — not general \(\hat S\), not co-equal decision \(z\), not Woody HT end-product as live math.
- **Goal (iii) path:** data-randomize the data-driven selection so (1) holds; **no** recalibration of \(\mathcal{C}\).
- **CREDO / CREME / CREAM / CRC:** literature for *methods patterns only* — never expand the problem statement to \(\pi_\varepsilon\), \(\lambda\), \(z^*_\lambda\), decision-risk, Algo 1 baselines.
- **Notation discipline:** Keep writeup quirks visible (third slot \(\theta\) in (1); lowercase \(y\) in \(\hat f(y;\theta)\)). Do not “fix” silently; flag in `research/notes/notation_quarantine.md`.
- **Authority:** Wenbin W1–W5 + UQ example control live math. L1 Woody agenda constrains *class* (opt-induced policy) but does **not** widen this plan’s equations. Do not equate H2 stand-in with missing July 2 Overleaf.
- **W4 flexibility:** May *propose* a more principal reformulation in `research/notes/` only; live deliverables stay on (1)(2) until mentors accept a change (still do not edit `writeup/`).

---

## Wenbin Ceiling (ruthless)

| Keep | Cut |
| --- | --- |
| Intersection: post-hoc + algo stability + opt (W1) | General post-hoc selection frameworks as the problem |
| UQ example (1)(2) only (W2) | Broad \(\tilde A(D;\xi)\), \(\theta_{\tilde S}\in C_{\tilde S}\) as live object |
| Selected object = \(\hat\theta(D)\) only | CREDO core, CREME/CREAM core, Woody HT discrete-boundary class |
| Part I: LOO of (2) + assumptions on \(\hat f,\hat g\) (W3) | Dual \(\Phi_{\mathrm{idx}}/\Phi_{\mathrm{dec}}\); co-equal \(z\) |
| Part II: goals (i)–(iii) on (1) at \(\hat\theta\) (W3) | Recalibrating \(\mathcal{C}\) as answer to (iii) |
| (iii) = data-randomize / no recalibration (W5) | Dual path “recalibrate OR randomize” |
| Method brainstorm: PTO, structured noise + inverse opt, Tijana line (W5) | Treating those papers as the problem definition |

---

## File Map (create under `research/`)

| Path | Responsibility |
| --- | --- |
| `literature/00_reading_queue.md` | Ordered reading list with extract targets |
| `literature/patterns_stability_to_validity.md` | Pattern: stability ⇒ coverage correction / post-selection validity |
| `literature/patterns_randomization_noise.md` | Pattern: noise / randomization ⇒ stability certificates |
| `literature/patterns_inverse_opt_structured_noise.md` | Pattern: inverse opt ⇒ structured perturbation (methods only) |
| `literature/digest_zrnic_jordan_stability.md` | Digest: Post-Selection Inference via Algorithmic Stability |
| `literature/digest_winners_curse_defense.md` | Digest: Flexible Defense Against Winner’s Curse |
| `literature/digest_angelopoulos_crc.md` | Digest: Conformal Risk Control (methods / validity template) |
| `literature/digest_credo_methods_only.md` | Digest: CREDO — extract inverse/structured-noise *techniques*, mark OUT-OF-PROBLEM |
| `literature/digest_creme_cream_methods_only.md` | Digest: CREAM — extract techniques only; mark OUT-OF-PROBLEM |
| `notes/notation_quarantine.md` | Unresolved \(y\) vs \(Y\); \(\alpha\) vs \(\theta\) slot; do not rewrite writeup |
| `notes/assumption_ledger.md` | Running list of assumptions with warrant + risk if false |
| `notes/method_candidates_w5.md` | PTO / data-randomize / structured noise mapped to (iii) only |
| `formal/part_i_stability.tex` | Part I definitions + lemmas (source of truth) |
| `formal/part_ii_posthoc.tex` | Part II validity + randomized selection map |
| `formal/common_setup.tex` | Shared objects: \(D\), \(\hat f,\hat g\), \(\hat\theta\), \(\mathcal{C}\), \(\alpha\) |
| `proofs/part_i_sketches.md` | Proof sketches for Part I lemmas |
| `proofs/part_ii_sketches.md` | Proof sketches for Part II theorems |
| `proofs/tighten_log.md` | Each tighten pass: claim → gap → fix |
| `proofs/sol_gaps/README.md` | When/why Sol was called; prompts; outputs |
| `experiments/loo_stability_demo.py` | Tiny assertable LOO / perturbation demo |
| `experiments/validity_inflation_demo.py` | Tiny coverage-gap demo under unstable vs randomized selection |
| `audit/TEMPLATE.md` | 4-gate audit template |
| `audit/GATE_LOG.md` | Append-only gate results after each deliverable |
| `audit/YYYY-MM-DD_<deliverable>_audit.md` | Per-deliverable audits |

---

## Continuous Audit Protocol (runs after EVERY deliverable)

Copy `research/audit/TEMPLATE.md`. Four parallel gates (swarm agents or sequential if solo):

1. **Wenbin coverage** — Does this deliverable advance (1)(2), goals (i)–(iii)/W5, Part I and/or Part II as written? Quote the writeup line it serves.
2. **Scope creep** — Any CREDO/CREME/CREAM/Woody-HT/general-\(\hat S\) object treated as live math? FAIL if yes.
3. **Assumption warrant** — Each new assumption: named, used where, falsifiable, weaker alternative considered?
4. **Math correctness** — Definitions match across files; lemma hypotheses used in proofs; no silent notation “fixes.”

**Pass rule:** All four PASS (or FAIL with explicit fix task). Append one line to `research/audit/GATE_LOG.md`. Do not start the next phase task until the prior deliverable’s audit is logged.

---

## Phase 0 — Literature Pattern Mining

**Success criteria:** Three pattern docs + five digests exist; each pattern names (a) hypotheses, (b) stability notion, (c) inference/validity conclusion, (d) what transfers to \(\hat\theta\) from (2), (e) what must NOT be imported as problem expansion. Audit PASS.

### Task 0.0: Scaffold audit + reading queue

**Files:**
- Create: `research/audit/TEMPLATE.md`
- Create: `research/audit/GATE_LOG.md`
- Create: `research/literature/00_reading_queue.md`
- Create: `research/notes/notation_quarantine.md`

- [ ] **Step 1:** Write audit template with the four gates above and PASS/FAIL checkboxes.
- [ ] **Step 2:** Initialize `GATE_LOG.md` with header columns: `date | deliverable | coverage | creep | assumptions | math | notes`.
- [ ] **Step 3:** Write reading queue (exact PDFs under frozen `context/papers/` — **read-only**):

```text
1. context/papers/01_priority_current/Post-Selection Inference via Algorithmic Stability.pdf
2. context/papers/01_priority_current/A Flexible Defense Against the Winner's Curse.pdf
3. context/papers/03_background/Conformal Risk Control.pdf
4. context/papers/02_lab_algorithmic/Calibrating Decision Robustness via Inverse Conformal Risk Control.pdf  # methods only
5. context/papers/02_lab_algorithmic/Conformalized Decision Risk Assessment.pdf  # methods only
6. Optional skim: Prediction-Powered-Inference.pdf (priority but not required for (1)(2) formalization)
```

- [ ] **Step 4:** Seed `notation_quarantine.md` with: (a) \(\mathcal{C}(\cdot,\alpha)\) def vs \(\mathcal{C}(\cdot,\theta)\) in (1); (b) \(\hat f(y;\theta)\) vs \(Y\); (c) rule = preserve + flag.
- [ ] **Step 5:** Audit this scaffolding deliverable; log to `GATE_LOG.md`.

### Task 0.1: Digest Zrnic/Jordan-line stability → post-selection validity

**Files:**
- Create: `research/literature/digest_zrnic_jordan_stability.md`
- Create: `research/literature/patterns_stability_to_validity.md`

**Source (read-only):** `context/papers/01_priority_current/Post-Selection Inference via Algorithmic Stability.pdf`

- [ ] **Step 1:** Extract: stability definition(s) \((\eta,\tau,\nu)\) or paper’s native form; main theorem linking stability to CI/coverage correction; proof outline in ≤15 bullets.
- [ ] **Step 2:** Map to our objects: selector \(A(D)\mapsto\hat\theta(D)\); “parameter of selected model” ↔ UQ hyperparameter \(\theta\); what would play the role of corrected level / inflation for (1).
- [ ] **Step 3:** Write pattern card in `patterns_stability_to_validity.md`:

```markdown
## Pattern: Stable selector ⇒ valid post-selection inference
- Inputs: ...
- Stability notion: ...
- Conclusion: ...
- Transfer to (2)→θ̂: ...
- Non-transfer / do-not-import: ...
```

- [ ] **Step 4:** Audit; log.

### Task 0.2: Digest Winner’s Curse defense (randomization / noise for stability)

**Files:**
- Create: `research/literature/digest_winners_curse_defense.md`
- Create: `research/literature/patterns_randomization_noise.md`

**Source:** `context/papers/01_priority_current/A Flexible Defense Against the Winner's Curse.pdf`

- [ ] **Step 1:** Extract: how randomization / noise / stabilization is injected; what certificate it buys; cost (power / width).
- [ ] **Step 2:** Pattern card: “noise ⇒ stability ⇒ validity” with hooks for W5 data-randomize of **selection** (not of \(\mathcal{C}\)).
- [ ] **Step 3:** Explicit red line: any procedure that recalibrates scores / thresholds of \(\mathcal{C}\) is **out** for goal (iii) in this project (may note as contrast only).
- [ ] **Step 4:** Audit; log.

### Task 0.3: Digest CRC (validity template) + CREDO/CREAM as methods-only

**Files:**
- Create: `research/literature/digest_angelopoulos_crc.md`
- Create: `research/literature/digest_credo_methods_only.md`
- Create: `research/literature/digest_creme_cream_methods_only.md`
- Create: `research/literature/patterns_inverse_opt_structured_noise.md`

**Sources:** CRC PDF; CREDO PDF; CREAM PDF under `context/papers/{03_background,02_lab_algorithmic}/`

- [ ] **Step 1:** CRC digest: risk-control / monotone threshold structure that makes (1)-style validity hold for **prespecified** \(\theta\). Pull only what justifies the writeup’s assumption (1).
- [ ] **Step 2:** CREDO digest with banner at top:

```markdown
# METHODS ONLY — NOT PROBLEM SCOPE
Do not import π_ε, inverse region, decision-risk as live problem objects.
Extract: structured noise / inverse conformal ideas usable to randomize θ̂ selection.
```

- [ ] **Step 3:** CREAM digest with same banner; extract risk-assessment / conformalized decision patterns usable as **analogy** for deviation bounds (goal ii), not as new equations in the problem.
- [ ] **Step 4:** Pattern card `patterns_inverse_opt_structured_noise.md`: how inverse-opt view suggests **structured** (not isotropic) noise on the selection map; candidate forms for \(\tilde\theta(D;\xi)\) affecting **selection only**.
- [ ] **Step 5:** Audit all Phase 0 literature deliverables as a batch; log. **Phase 0 exit gate:** patterns cite concrete theorem numbers from PDFs; no CREDO/CREAM symbols in `formal/` yet (formal does not exist — ensure notes do not redefine the problem).

---

## Phase 1 — Formalization of Part I (LOO stability of (2))

**Success criteria:** `formal/common_setup.tex` + `formal/part_i_stability.tex` define \(\hat\theta(D)\), LOO (and optional neighboring) stability, list structural assumptions on \(\hat f,\hat g\), and state ≥3 candidate lemmas with precise hypotheses. Assumption ledger populated. Audit PASS. No Part II claims yet beyond “will consume Part I.”

### Task 1.1: Common setup (freeze objects)

**Files:**
- Create: `research/formal/common_setup.tex`
- Create: `research/notes/assumption_ledger.md`

- [ ] **Step 1:** Formalize (read-only quote of writeup, then research-side definitions):

```tex
% Objects (research formalization; writeup remains frozen)
% Data D; miscoverage level \alpha; hyperparameter \theta;
% Uncertainty set C(X; D, \theta) with validity (1) for any fixed \theta;
% Measurable \hat f, \hat g with \sigma(\hat f),\sigma(\hat g) \subseteq \sigma(D);
% Program (2): min_\theta \hat f(y;\theta) s.t. \hat g(\theta) \le 0;
% Output \hat\theta(D).
```

- [ ] **Step 2:** In `assumption_ledger.md`, open rows for: i.i.d. data (if assumed); uniqueness of minimizer; convexity/Lipschitz of \(\hat f,\hat g\); how \(\hat f,\hat g\) are estimated from \(D\) (empirical risk, plug-in, etc.) — each marked `warrant: unstated | literature | necessary for lemma X`.
- [ ] **Step 3:** Cross-link `notation_quarantine.md` (do not resolve \(y\) vs \(Y\) by editing writeup; pick a research convention and document it).
- [ ] **Step 4:** Audit; log.

### Task 1.2: Stability notions for \(\hat\theta(D)\)

**Files:**
- Create: `research/formal/part_i_stability.tex`
- Modify: `research/notes/assumption_ledger.md`

- [ ] **Step 1:** Define leave-one-out replace-one stability for the **optimizer output**:

```tex
% Candidate definitions (choose primary after literature map):
% (LOO-θ) E[ d(\hat\theta(D), \hat\theta(D^{\setminus i})) ] ≤ ε_n
% (LOO-TV / soft) distributional stability if randomized later
% (Argmax-gap) uniqueness gap ⇒ Lipschitz of argmin
```

Primary target per Wenbin W3: **if dataset changes by one point, how much does \(\hat\theta(D)\) change?** Prefer a metric \(d\) on \(\Theta\) stated explicitly.

- [ ] **Step 2:** State structural assumptions package `A_opt`:
  - How \(\hat f,\hat g\) depend on \(D\) (e.g., additive empirical averages; leave-one-out change \(O(1/n)\)).
  - Regularity of (2): convexity, Slater, strong convexity / PL, Lipschitz gradients, constraint qualification.
  - Identifiability: unique \(\hat\theta\) or measurable selection rule.
- [ ] **Step 3:** Candidate lemmas (names locked for later proofs):

| ID | Claim (informal) | Depends on |
| --- | --- | --- |
| L1.1 | Under `A_opt`, \(\|\hat\theta(D)-\hat\theta(D^{\setminus i})\|\le \kappa/n\) a.s. or in expectation | strong convexity + LOO of \(\hat f,\hat g\) |
| L1.2 | If \(\hat f,\hat g\) are \(\beta\)-LOO stable as maps \(D\mapsto(\hat f,\hat g)\), then \(\hat\theta\) is \(\kappa(\beta)\)-LOO stable | implicit-function / perturbation of KKT |
| L1.3 | Without uniqueness, only set-valued Hausdorff stability holds; need tie-break or randomization | counterexample sketch |

- [ ] **Step 4:** Write each lemma in `part_i_stability.tex` with full hypothesis list (even if proof comes later).
- [ ] **Step 5:** Audit; log. **Phase 1 exit gate:** W3 questions are literally answered as definitions + lemma statements; no validity claims.

---

## Phase 2 — Formalization of Part II (post-hoc validity + randomized selection)

**Success criteria:** `formal/part_ii_posthoc.tex` states (i) conditions for (1) at \(\hat\theta\); (ii) explicit inflation / deviation bound; (iii) a randomized selection map \(\tilde\theta(D;\xi)\) that restores (1) **without** changing the construction of \(\mathcal{C}(\cdot;\cdot,\theta)\) for fixed \(\theta\). Method candidates file maps W5 → (iii). Audit PASS.

### Task 2.1: Goals (i)–(ii) — plug-in validity and deviation

**Files:**
- Create: `research/formal/part_ii_posthoc.tex`
- Modify: `research/notes/assumption_ledger.md`

- [ ] **Step 1:** Define plug-in coverage:

```tex
Cov(\hat\theta) := P( Y \in C(X; D, \hat\theta(D)) ).
```

Goal (i): find conditions s.t. \(\mathrm{Cov}(\hat\theta)\ge 1-\alpha\).
Goal (ii): bound \(\bigl((1-\alpha) - \mathrm{Cov}(\hat\theta)\bigr)_+\) or equivalent inflation \(\alpha\mapsto\alpha+\Delta\).

- [ ] **Step 2:** Candidate theorems:

| ID | Claim | Uses |
| --- | --- | --- |
| T2.1 | If \(\hat\theta\) is independent of \(D\) used in \(\mathcal{C}\), then (1) holds (baseline; usually false under shared \(D\)) | — |
| T2.2 | If \(\hat\theta\) is \(\varepsilon\)-LOO stable and \(\mathcal{C}\) is Lipschitz in \(\theta\) in appropriate sense, then \(\mathrm{Cov}(\hat\theta)\ge 1-\alpha-\Delta(\varepsilon)\) | L1.1–L1.2 + lit pattern |
| T2.3 | Unstable \(\hat\theta\) can break (1) by \(\Omega(1)\) — minimal counterexample setting | experiments later |

- [ ] **Step 3:** Make \(\Delta(\varepsilon)\)’s functional form a named target (do not leave as “some Delta”). Prefer forms parallel to Zrnic–Jordan-style corrections, specialized to coverage of \(\mathcal{C}\).
- [ ] **Step 4:** Audit; log.

### Task 2.2: Goal (iii) — randomized selection map (W5)

**Files:**
- Modify: `research/formal/part_ii_posthoc.tex`
- Create: `research/notes/method_candidates_w5.md`

- [ ] **Step 1:** Define selection-only randomization:

```tex
\tilde\theta(D;\xi) = \mathcal{R}(\hat\theta(D), D, \xi)
% \xi ~ known noise; \mathcal{R} does not alter C(·;·,θ) for fixed θ
% Validity target: P(Y ∈ C(X; D, \tilde\theta(D;\xi))) ≥ 1-α
```

Hard constraint in the formal file header comment: **Forbidden for (iii):** any map that recomputes conformal scores, thresholds, or risk-control levels of \(\mathcal{C}\) using a second pass (“recalibration”).

- [ ] **Step 2:** In `method_candidates_w5.md`, three rows only:

| Candidate | Mechanism on selection | Stability aimed | Validity route | Out-of-scope if… |
| --- | --- | --- | --- | --- |
| Data-randomize (primary) | \(\xi\) perturbs (2) or softens argmin | LOO / distributional | T2.2-style | it edits \(\mathcal{C}\) |
| Structured noise / inverse opt | \(\xi\) shaped by inverse of (2) | certifiable \(\varepsilon\) | W5 “our paper” pointer | imports CREDO decision-risk objects |
| PTO-style data-driven policy | policy = solution of opt; randomize policy params | policy stability | analogy only until reduced to \(\tilde\theta\) | becomes SPO paper clone |

- [ ] **Step 3:** State theorem T2.4: under noise level \(\sigma_n\) large enough vs instability, \(\tilde\theta\) is \(\varepsilon_n\)-stable and T2.2 applies with \(\Delta(\varepsilon_n)\le 0\) or absorbed into \(\alpha\) **without** touching \(\mathcal{C}\)’s fixed-\(\theta\) guarantee.
- [ ] **Step 4:** Audit; log. **Phase 2 exit gate:** (iii) text in formal file matches W5 verbs; zero “recalibrate \(\mathcal{C}\)” procedures marked as solutions.

---

## Phase 3 — Proof Sketches → Tighten → Self-Checks

**Success criteria:** Every lemma/theorem in `formal/` has a sketch in `proofs/`; at least one Part I and one Part II claim has a runnable self-check (Python assert demo or Lean stub); `tighten_log.md` shows ≥2 tighten passes on the main chain L1.x → T2.2 → T2.4. Audit PASS after each major proof file.

### Task 3.1: Part I sketches + LOO demo

**Files:**
- Create: `research/proofs/part_i_sketches.md`
- Create: `research/experiments/loo_stability_demo.py`
- Create: `research/proofs/tighten_log.md`

- [ ] **Step 1:** For L1.1–L1.3, write sketch: assumptions used → key inequality → conclusion; mark `GAP:` lines explicitly.
- [ ] **Step 2:** Implement minimal demo: synthetic strongly convex (2) with empirical \(\hat f,\hat g\); assert mean LOO displacement scales as \(O(1/n)\) on a grid of \(n\).

```python
# research/experiments/loo_stability_demo.py
# Self-check: mean ||θ̂(D) - θ̂(D^{-i})|| * n is bounded for large n
# Exit 0 on pass; assert fails on misspecified non-strongly-convex control
```

- [ ] **Step 3:** Run: `python research/experiments/loo_stability_demo.py` — expect exit 0.
- [ ] **Step 4:** First tighten pass on L1.1; log in `tighten_log.md`.
- [ ] **Step 5:** Audit; log.

### Task 3.2: Part II sketches + validity inflation demo

**Files:**
- Create: `research/proofs/part_ii_sketches.md`
- Create: `research/experiments/validity_inflation_demo.py`

- [ ] **Step 1:** Sketch T2.1–T2.4; wire which Part I lemma each step needs.
- [ ] **Step 2:** Demo: shared-calibration selection of \(\theta\) that overfits; show empirical coverage \(<1-\alpha\); apply selection noise \(\xi\); show coverage recovers toward \(1-\alpha\) **without** rebuilding \(\mathcal{C}\)'s fixed-\(\theta\) rule (only \(\theta\) fed into it changes).
- [ ] **Step 3:** Run demo; exit 0.
- [ ] **Step 4:** Tighten T2.2/T2.4; log.
- [ ] **Step 5:** Audit; log.

### Task 3.3: Optional Lean stubs (only if lemma is tiny)

**Files:**
- Create (optional): `research/proofs/lean/LooLipschitz.lean`

- [ ] **Step 1:** Only if a purely analytic inequality (e.g., Lipschitz of argmin under strong convexity) is isolated — encode that inequality alone. Do not attempt full measure-theoretic coverage in Lean.
- [ ] **Step 2:** If Lean not worth it, write `research/proofs/lean/README.md` stating deferred + Python demos are the self-check. Audit; log.

---

## Phase 4 — Continuous Multi-Agent Audit Gates

**Success criteria:** Every completed Task above has a matching `research/audit/YYYY-MM-DD_<tag>_audit.md` and a `GATE_LOG.md` row. Any FAIL spawns a fix task before proceeding. No silent scope drift across phases.

### Task 4.1: Institutionalize gate swarm

**Files:**
- Create: `research/audit/agent_prompts.md`

- [ ] **Step 1:** Write four reusable agent prompts (Coverage / Scope creep / Assumption warrant / Math correctness) that **only** read `writeup/Problem_Writeup.tex`, `writeup/AUDIT_Wenbin_Narrowing.md`, and the deliverable under `research/`.
- [ ] **Step 2:** After each future deliverable, run all four (parallel Task agents allowed; **no fast-mode** models). Merge into one audit file.
- [ ] **Step 3:** Weekly (or every 5 deliverables): run a **regression audit** comparing `formal/*.tex` against Wenbin ceiling table in this plan; output `research/audit/regression_wenbin_ceiling.md`.

**Gate failure handling:**
- Coverage FAIL → add missing lemma/definition or explicitly defer with mentor question in `research/notes/`.
- Creep FAIL → delete/quarantine offending objects to `research/notes/out_of_scope_holding.md`; never into `formal/`.
- Assumptions FAIL → weaken or mark `ponytail:`-style ceiling in formal comments.
- Math FAIL → open Sol gap (Phase 5) or fix sketch.

---

## Phase 5 — Sol / Codex CLI Reserved for Hardest Proof Gaps

**Success criteria:** Sol is not used for literature summaries, audits, or routine algebra. Each call has a gap ID, minimal formal snippet, and logged output. Cursor OpenAI credits are **not** spent (use Codex CLI per workspace rule).

### Task 5.1: Gap protocol

**Files:**
- Create: `research/proofs/sol_gaps/README.md`
- Create: `research/proofs/sol_gaps/GAP_TEMPLATE.md`

**When to call Sol (only if all hold):**
1. Gap blocks T2.2 or T2.4 (main validity chain) or L1.2 (KKT/perturbation core).
2. Local sketch has a precise missing inequality / interchange / measurability step.
3. Two tighten passes failed to close it.
4. Self-check cannot even state the claim as an assert.

**When NOT to call Sol:** reading PDFs; rewriting digests; scope debates; generating new problem formulations; anything answerable by Zrnic/CRC pattern cards already mined.

- [ ] **Step 1:** For an eligible gap, write `research/proofs/sol_gaps/GAP_XXX.md` with: claim, hypotheses, failed attempts, exact question (≤40 lines of formal math).
- [ ] **Step 2:** Run:

```bash
codex exec --ephemeral -s read-only -m gpt-5.6-sol "$(cat research/proofs/sol_gaps/GAP_XXX.md)" </dev/null
```

- [ ] **Step 3:** Save raw output to `research/proofs/sol_gaps/GAP_XXX_sol_out.md`; integrate only verified steps into `proofs/*_sketches.md` and `formal/`.
- [ ] **Step 4:** If CLI fails, record exact error and stop — do **not** fall back to Cursor-hosted Sol. Audit the integration; log.

---

## Phase 6 — Method Integration for (iii) Only

**Success criteria:** One primary randomized selection mechanism is specified end-to-end (inputs, noise law, stability lemma used, validity theorem used) in `formal/part_ii_posthoc.tex` + `notes/method_candidates_w5.md`; alternatives listed as backups; still no \(\mathcal{C}\) recalibration; final audit PASS.

### Task 6.1: Lock primary (iii) mechanism

**Files:**
- Modify: `research/formal/part_ii_posthoc.tex`
- Modify: `research/notes/method_candidates_w5.md`
- Create: `research/notes/open_questions_for_mentors.md`

- [ ] **Step 1:** Choose primary mechanism (default bias: **data-randomize selection** with structured noise if Part I shows isotropic noise is wasteful). Document rejection reasons for recalibration.
- [ ] **Step 2:** Write algorithm box: how to sample \(\xi\), how to solve randomized (2), how to report \(\mathcal{C}(X;D,\tilde\theta)\) unchanged in form.
- [ ] **Step 3:** List mentor questions only if blocked (e.g., unresolved \(y\) vs \(Y\); whether W4 principal reformulation should replace UQ example). Do not edit writeup.
- [ ] **Step 4:** Final full-ceiling regression audit; log. **Plan complete when:** L1.x + T2.2 + T2.4 chain is stated, sketched, self-checked, and audited; (iii) has a concrete randomized selection procedure.

---

## Ordered Master Task List (swarm execution order)

| Order | Task | Output path(s) |
| --- | --- | --- |
| 1 | 0.0 Scaffold | `audit/TEMPLATE.md`, `audit/GATE_LOG.md`, `literature/00_reading_queue.md`, `notes/notation_quarantine.md` |
| 2 | 0.1 Stability→validity digest | `literature/digest_zrnic_jordan_stability.md`, `literature/patterns_stability_to_validity.md` |
| 3 | 0.2 Randomization digest | `literature/digest_winners_curse_defense.md`, `literature/patterns_randomization_noise.md` |
| 4 | 0.3 CRC + CREDO/CREAM methods-only | `literature/digest_angelopoulos_crc.md`, `literature/digest_credo_methods_only.md`, `literature/digest_creme_cream_methods_only.md`, `literature/patterns_inverse_opt_structured_noise.md` |
| 5 | 1.1 Common setup | `formal/common_setup.tex`, `notes/assumption_ledger.md` |
| 6 | 1.2 Part I formal | `formal/part_i_stability.tex` |
| 7 | 2.1 Part II (i)(ii) | `formal/part_ii_posthoc.tex` (partial) |
| 8 | 2.2 Part II (iii) W5 | `formal/part_ii_posthoc.tex`, `notes/method_candidates_w5.md` |
| 9 | 3.1 Part I proofs + demo | `proofs/part_i_sketches.md`, `experiments/loo_stability_demo.py`, `proofs/tighten_log.md` |
| 10 | 3.2 Part II proofs + demo | `proofs/part_ii_sketches.md`, `experiments/validity_inflation_demo.py` |
| 11 | 3.3 Lean optional | `proofs/lean/*` |
| 12 | 4.x Audits continuous | `audit/*` after every row above |
| 13 | 5.x Sol gaps on-demand | `proofs/sol_gaps/GAP_*.md` |
| 14 | 6.1 Lock (iii) mechanism | `notes/method_candidates_w5.md`, `notes/open_questions_for_mentors.md` |

After **every** row 1–11 and 14: run Phase 4 gates before starting the next row.

---

## Success Criteria by Phase (checklist)

| Phase | Done when |
| --- | --- |
| 0 | Pattern cards answer: how stability/noise/inverse-opt transfer to \(\hat\theta\) from (2); CREDO/CREAM quarantined |
| 1 | LOO stability of (2) is a mathematical object; assumptions on \(\hat f,\hat g\) explicit; L1.1–L1.3 stated |
| 2 | (i) conditions, (ii) \(\Delta(\varepsilon)\), (iii) \(\tilde\theta(D;\xi)\) with no \(\mathcal{C}\) recalibration |
| 3 | Sketches exist; demos exit 0; tighten log nonempty on main chain |
| 4 | `GATE_LOG.md` complete for all deliverables; regression ceiling audit clean |
| 5 | Sol used ≤ hard gaps; each gap integrated or explicitly still open |
| 6 | Primary (iii) algorithm written; mentor questions (if any) isolated |

---

## What NOT to Do

1. **Do not edit** `writeup/**` or `context/**`.
2. **Do not widen** to general post-hoc selection, dual index/decision maps, or Woody HT as live equations.
3. **Do not treat CREDO/CREME/CREAM as the problem** — methods literature only; banner every digest.
4. **Do not answer (iii) by recalibrating \(\mathcal{C}\)** (W5). Contrast notes allowed; solutions that recalibrate are out.
5. **Do not silently fix** writeup notation (\(y\)/\(Y\), \(\alpha\)/\(\theta\) slot).
6. **Do not spend Cursor OpenAI/Sol credits** for gaps — Codex CLI only; skip Sol for non-gaps.
7. **Do not use fast-mode agents.**
8. **Do not invent a second uncertainty-set construction** “to make validity easier.”
9. **Do not equate** this plan’s frozen writeup with the missing July 2 Overleaf.
10. **Do not start Part II validity theorems** before Part I stability definitions exist (W3 order).

---

## Execution Handoff

Plan complete and saved to:

`/Users/nicholasmino/Desktop/Research/Formulation/research/plans/2026-07-27-wenbin-uq-research-plan.md`

**Two execution options:**

1. **Subagent-Driven (recommended)** — Fresh subagent per task row; Phase 4 four-gate audit between tasks; use `superpowers:subagent-driven-development`.
2. **Inline Execution** — Same session, batch with checkpoints; use `superpowers:executing-plans`.

Which approach?
