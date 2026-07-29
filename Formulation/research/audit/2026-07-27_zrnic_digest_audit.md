# Audit: Zrnic–Jordan stability digest + pattern

Deliverable: literature digest + stability→validity pattern (Zrnic & Jordan, arXiv:2011.09462v2)  
Path(s): `research/literature/digest_zrnic_jordan_stability.md`, `research/literature/patterns_stability_to_validity.md`  
Date: 2026-07-27  
Auditor: subagent (4-gate)  
Ceiling: `writeup/Problem_Writeup.tex`

Special checks requested:
- (a) wrongly treat \(e^\eta\) CI inflation as answering goal (iii)?
- (b) CREDO/CREME as live math?
- (c) LOO vs Def. 2 conflation marked?

---

## Gate 1 — Wenbin coverage
Advances (1)(2), goals (i)–(iii)/W5, Part I and/or Part II?

- Quote writeup line served:
  - Validity (1) / constrained opt (2): writeup ll.45–61 (“selected object … only \(\hat\theta(\mathcal{D})\)”).
  - Goals (i)–(iii): writeup ll.72–80; goal (iii) override Remark ll.83–87 (“no recalibration, strategy: data-randomize”).
  - W5: writeup ll.111–119 (“data-randomize the selection… algorithmic stability (Tijana line…)”).
  - Part II: writeup ll.104–106 (post-hoc inference on \(\mathcal{C}\) after plug-in); Part I LOO named only as a *non*-identity with Def. 2 (gap marked, not pretended away).

- Evidence in deliverable:
  - Digest §4 map table: \(A(D)\leftrightarrow\hat\theta(D)\), classical fixed-\(S\) CI ↔ (1) for prespecified \(\theta\), inflation role when plugging into (1).
  - Patterns “Transfer to (2)→\(\hat\theta\)” + “Goal (iii) alignment”: randomize selection so \(\eta\to 0\), keep form of \(\mathcal{C}\) fixed.
  - Patterns Non-transfer: PoSI/\(\hat M\)/\(\beta_{\hat M}\) not imported as live estimand.

- [x] PASS
- [ ] FAIL — fix:

---

## Gate 2 — Scope creep
Any CREDO/CREME/CREAM/Woody-HT/general-ÂŜ treated as live math?

- Evidence:
  - Digest ceiling line: “No CREDO/CREME as problem objects.”
  - Patterns Non-transfer: “Do **not** import CREDO/CREME … as the selected target; writeup selected object is only \(\hat\theta\) from (2).”
  - No CREAM / Woody-HT / general-\(\hat S\) as live problem objects; \(\hat S\) appears only as paper-native notation with explicit remap \(A\leftrightarrow\hat\theta\), and model-support \(\hat M=\mathrm{post}(\hat\theta)\) flagged as non-transfer (digest §4 last paragraph; patterns Non-transfer bullets).

- Special check (b): CREDO/CREME appear only as quarantine / do-not-import — **not** live math. PASS.

- [x] PASS (none)
- [ ] FAIL — remove:

---

## Gate 3 — Assumption warrant
Each new assumption named, used where, falsifiable?

| Assumption | Named? | Used where | Falsifiable / scoped? |
|---|---|---|---|
| \((\eta,\tau,\nu)\)-stability (Def. 2) | Yes (digest §1; patterns Stability notion) | Lemma 1, Thm 2, Cor. 1–2 | Design property via Lap / noisy FW; user-chosen budget |
| Classical fixed-\(S\) validity of \(\mathrm{CI}^{(\alpha)}_S\) (or (1) for fixed \(\theta\)) | Yes | Thm 2 hypothesis; patterns Inputs | Standard classical claim; transferred only as analogy |
| Error split \(\delta+\tau+\nu\) targeting overall \(\alpha\) | Yes (digest Thm 2 recipe) | Operational Thm 2 | Explicit parameter choice |
| Gaussian \(y\), known \(\sigma\) (Algs 2–3, Cor. 2) | Yes | Instantiation only | Patterns: “Do **not** assume … part of the pattern core” |
| Constrained FW LASSO \(\|\theta\|_1\le C_1\) | Yes | Structural echo of (2), not identity | Flagged “not a license to treat \(\hat\theta_{\mathrm{LASSO}}\) as writeup \(\hat\theta\)” |

- [x] PASS
- [ ] FAIL — list:

---

## Gate 4 — Math correctness
Defs consistent; hypotheses used; no silent notation fixes?

- Def. 1 / Def. 2 / Lemma 1 / Theorem 2 stated with paper-native form and PDF page pins; proof outline uses Def. 2 → Lemma 1 → classical conditional miscoverage \(\le\delta e^{-\eta}\) → cancel \(e^\eta\) — hypotheses of Thm 2 are used, not elided.
- Writeup notation Remark respected: \(\mathcal{C}(\cdot;\mathcal{D},\theta)\) keeps \(\theta\) in the third slot; no silent rewrite to \(\alpha\)-in-third-slot.
- Special check (a): **does not** treat \(e^\eta\) CI inflation as the answer to goal (iii).
  - Digest §4: “Using a large \(\eta\) and compensating with a more conservative \(\mathcal{C}\) is their Thm 2 ‘correction’ path — closer to answering (i)–(ii) / PoSI inflation than to goal (iii).” Goal (iii) path = drive \(\eta\to 0\) by randomizing selection so classical \(\mathcal{C}\) needs essentially no recalibration.
  - Patterns Non-transfer: “Do **not** treat Thm 2’s \(e^\eta\)-inflated / widened \(\mathrm{CI}\) as the answer to goal (iii): that is recalibrating the inferential object.”
- Special check (c): LOO vs Def. 2 conflation **marked**.
  - Digest §1: “**Not their notion:** classical leave-one-out / uniform stability… Stability here is **distributional indistinguishability of the selection law**.”
  - Patterns Transfer: “Part I … asks leave-one-out movement of \(\hat\theta\); this pattern instead asks for **Def. 2**… Bridging requires…”
  - Patterns Non-transfer: “Do **not** equate Def. 2 with Part I leave-one-out stability…”
- Minor wording nit (non-blocking): patterns Conclusion says classical validity after selection “iff” nominal miscoverage inflated by \(e^\eta\); Thm 2 is **sufficient**, not necessary. Does not reverse the goal-(iii) fork or smuggle a notation fix.

- [x] PASS
- [ ] FAIL — list:

---

## Overall
- [x] ALL PASS — may proceed
- [ ] FAIL — open fix task before next phase work

**Notes:** Special checks (a)(b)(c) all clear. Optional polish (not a gate fail): soften patterns “iff” → “if” / “sufficiently when.”
