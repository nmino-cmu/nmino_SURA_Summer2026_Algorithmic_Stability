# Audit: Part II posthoc + Sol set-valued Thm2 transfer

Deliverable: Part II formal draft + Sol-derived set-valued ZJ transfer  
Path(s): `research/formal/part_ii_posthoc.tex`, `research/proofs/sol_gaps/2026-07-27_setvalued_thm2.txt`  
Date: 2026-07-27  
Auditor: subagent (4-gate)  
Ceiling: `writeup/Problem_Writeup.tex`

Special checks requested:
1. Does Cor vanish correctly implement W5 (iii) without recalibrating \(\mathcal{C}\)?
2. Is \(e^\eta\) level change correctly labeled as NOT (iii)?
3. Any CREDO/CREME live creep?
4. Are assumptions FV / ST / OV warranted?

---

## Gate 1 — Wenbin coverage
Advances (1)(2), goals (i)–(iii)/W5, Part I and/or Part II?

- Quote writeup line served:
  - Validity (1) / selected object \(\hat\theta\) from (2): writeup ll.45–61.
  - Goals (i)–(iii): writeup ll.72–80; goal (iii) override Remark ll.83–87 (“no recalibration, strategy: data-randomize”).
  - W5: writeup ll.111–119 (“data-randomize the selection… (no recalibration of \(\mathcal{C}\))”).
  - Part II: writeup ll.104–106 (post-hoc validity of \(\mathcal{C}\) after plug-in).

- Evidence in deliverable:
  - Thm set-valued: (i) transfer under (ST)+(OV)/(FV); Infl Def: (ii) excess under fixed \(q=\alpha\).
  - Remark “Goals (i)–(ii) vs (iii)”: correctly forks level inflation vs selection randomization.
  - Cor vanish + randomized selection map + forbidden repairs: intended (iii)/W5 path.
  - Remaining problem: instantiate via Part I noisy/soft near-minimizer — Part I bridge named, not faked.

- Special check (1): **FAIL.** Cor vanish’s primary display still uses
  \[
  C^{(\alpha e^{-\eta_r})}
  \]
  (sol_gaps ll.209–219; `part_ii` Cor.~\ref{cor:vanish}). That is **level recalibration of \(\mathcal{C}\)**, the Thm-2 correction path for (i)–(ii), not W5/(iii).
  - Writeup (iii)/W5 require restoring validity of (1) **without** recalibrating \(\mathcal{C}\), by randomizing selection only.
  - The correct (iii) display from Thm set-valued with **fixed** \(q=\alpha\) is
    \[
    \mathbb{P}\{Y\notin C^{(\alpha)}(X;D,A_r(D))\}
    \le e^{\eta_r}\alpha+\tau_r+\nu_r,
    \]
    hence \(\mathrm{Infl}\le(e^{\eta_r}-1)\alpha+\tau_r+\nu_r\to 0\) when \(\eta_r,\tau_r+\nu_r\to 0\) and the fixed-\(\theta\) map of \(C\) is unchanged.
  - Zero-stability clause (“If \(\eta=\tau=\nu=0\), classical (1)…”) is fine but is the limit point, not a substitute for the finite-\(r\) (iii) statement.
  - sol_gaps prose “without … recalibrating the family \(C\)” while displaying \(C^{(\alpha e^{-\eta_r})}\) is self-contradictory.

- [ ] PASS
- [x] FAIL — fix: rewrite Cor vanish (both files) to keep \(C^{(\alpha)}\) fixed; put vanishing excess / Infl→0 as the (iii) claim. Move \(C^{(\alpha e^{-\eta_r})}\) (or \(\delta e^{-\eta}\)) exclusively under (i)–(ii) / Infl.

---

## Gate 2 — Scope creep
Any CREDO/CREME/CREAM/Woody-HT/general-ÂŜ treated as live math?

- Evidence: neither path mentions CREDO, CREME, CREAM, Woody-HT, or a general \(\hat S\) estimand. Live objects are \(A(D)=\hat\theta\), \(C^{(q)}\), and ZJ \((\eta,\tau,\nu)\)-stability. Forbidden-repairs Cor marks sample-splitting / threshold recalibration as contrast-only.

- Special check (3): **PASS** — no CREDO/CREME live creep.

- [x] PASS (none)
- [ ] FAIL — remove:

---

## Gate 3 — Assumption warrant
Each new assumption named, used where, falsifiable?

| Assumption | Named? | Used where | Falsifiable / scoped? |
|---|---|---|---|
| (FV) joint fixed-\(\theta\) validity | Yes (`part_ii` Ass.; sol Case A) | Implies (OV) under \(A_0\perp W\); hyp for Cor vanish | Scoped: joint over same \((D,X,Y)\); conditional-on-\(D\) or independent-copy \(D\) explicitly **not** automatic |
| (ST) \((\eta,\tau,\nu)\)-stability (ZJ Def.~2) | Yes (Thm hyp; tagged (ST) in sol) | Thm bound (2); Cor vanish sequence | Design property of \(A\); rates left to Part I instantiation (Remaining problem) |
| (OV) oracle validity | Yes (Thm hyp; sol) | Direct hyp of transfer | Falsifiable classical claim; (FV) sufficient when \(A_0\perp W\) |
| Common Markov kernel / no unaccounted \(A\)-\(C\) coupling | Yes (Thm; sol Case B) | Proof sketch second line | Case B gives OV′ / enlarged-output alternative if violated |
| Randomized \(A_r\) leaves fixed-\(\theta\) map of \(C\) unchanged | Yes (Cor vanish) | Goal-(iii) path | Explicit structural constraint matching W5 |

- Special check (4): **PASS** — FV/ST/OV are warranted, named, and used; Case A/B scoping is honest. Instantiation of rates and project-\(\mathcal{C}\) (FV) correctly deferred to Remaining problem (not smuggled as proved).

- [x] PASS
- [ ] FAIL — list:

---

## Gate 4 — Math correctness
Defs consistent; hypotheses used; no silent notation fixes?

- Thm set-valued: failure section \(B_q(w)\); (ST) on data-dependent sections; \(\nu\)-mass of \(G^c\); \(A_0\perp W\) + common kernel → (2); \(q=\delta e^{-\eta}\) → (3). Proof sketch matches hypotheses. Bound math **correct**.
- Notation: \(C^{(q)}(X;D,\theta)\) keeps \(\theta\) in the third slot; level is the superscript \(q\) — respects writeup Notation Remark (α vs θ).
- Def Infl with fixed \(q=\alpha\) is the right (ii) object; Thm ⇒ \(\mathrm{Infl}\le(e^\eta-1)\alpha+\tau+\nu\).
- Special check (2): Remark “Goals (i)–(ii) vs (iii)” **correctly** labels \(C^{(\delta e^{-\eta})}\) as level inflation / **not** (iii). **PASS** for the Remark.
- Same special check, Cor vanish: **undermines** the Remark — Goal-(iii) section primary formula is exactly the form the Remark forbids. sol_gaps “Goal-(iii) corollary” title + “without recalibrating” claim are false for the displayed inequality (math true as (i)–(ii) consequence; wrong goal tag).

- [ ] PASS
- [x] FAIL — list:
  1. Relabel / rewrite Cor vanish so (iii) uses fixed \(C^{(\alpha)}\) + vanishing Infl (see Gate 1).
  2. Delete or rephrase sol_gaps claim “without … recalibrating the family \(C\)” wherever the display still changes the level \(q\).
  3. Keep \(e^\eta\) level change only in Thm (3) / Goal (ii) Infl path (Remark already correct).

---

## Overall
- [ ] ALL PASS — may proceed
- [x] FAIL — open fix task before next phase work

**Fix task (minimal):** In both `part_ii_posthoc.tex` and `2026-07-27_setvalued_thm2.txt`, change Cor vanish to:

- Hypothesis unchanged: \(\eta_r\to0\), \(\tau_r+\nu_r\to0\), fixed-\(\theta\) map of \(C\) unchanged, (FV).
- Display: \(\mathbb{P}\{Y\notin C^{(\alpha)}(X;D,A_r(D))\}\le e^{\eta_r}\alpha+\tau_r+\nu_r\) (or Infl→0).
- Keep \(C^{(\delta e^{-\eta})}\) / \(C^{(\alpha e^{-\eta_r})}\) only under (i)–(ii).

**Notes:** Thm transfer + FV/ST/OV warrant + Remark fork + no CREDO/CREME are solid. Only the Goal-(iii)/W5 packaging of Cor vanish fails the ceiling.
