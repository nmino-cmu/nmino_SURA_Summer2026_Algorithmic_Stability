# Re-audit: Part II posthoc + Sol set-valued Thm2 (post Cor-vanish fix)

Deliverable: Part II formal draft + Sol-derived set-valued ZJ transfer (after W5/(iii) packaging fix)  
Path(s): `research/formal/part_ii_posthoc.tex`, `research/proofs/sol_gaps/2026-07-27_setvalued_thm2.txt`  
Date: 2026-07-27  
Auditor: subagent (4-gate re-audit)  
Ceiling: `writeup/Problem_Writeup.tex`  
Prior FAIL: `2026-07-27_part_ii_sol_audit.md` — Cor vanish used \(C^{(\alpha e^{-\eta})}\) under (iii).

Special checks (re-verify):
1. Cor vanish primary display is \(C^{(\alpha)}\), **not** \(C^{(\alpha e^{-\eta})}\).
2. W5/(iii) packaging: fixed classical level + Infl→0 via \(\eta,\tau,\nu\to0\); \(e^\eta\) level change only under (i)–(ii).
3. No CREDO/CREME live creep.
4. FV / ST / OV still warranted.

---

## Gate 1 — Wenbin coverage
Advances (1)(2), goals (i)–(iii)/W5, Part I and/or Part II?

- Quote writeup line served (unchanged from prior audit):
  - Validity (1) / selected \(\hat\theta\) from (2): writeup ll.45–61.
  - Goals (i)–(iii): writeup ll.72–80; (iii) override Remark ll.83–87.
  - W5: writeup ll.111–119 (data-randomize selection; no recalibration of \(\mathcal{C}\)).
  - Part II: writeup ll.104–106.

- Evidence in deliverable:
  - Thm set-valued: (i) transfer; Infl Def: (ii) excess at fixed \(q=\alpha\).
  - Remark “Goals (i)–(ii) vs (iii)”: forks level inflation vs selection randomization — intact.
  - **Cor vanish (fixed):** primary display is now
    \[
    \mathbb{P}\{Y\notin C^{(\alpha)}(X;D,A_r(D))\}
    \le e^{\eta_r}\alpha+\tau_r+\nu_r,
    \]
    hence \(\mathrm{Infl}_r\le(e^{\eta_r}-1)\alpha+\tau_r+\nu_r\to0\)
    (`part_ii` Cor.~\ref{cor:vanish} ll.100–108; sol_gaps ll.211–219).
  - Explicit anti-recalibration: “same classical level \(\alpha\)… **no** level change”; optional \(C^{(\delta e^{-\eta})}\) “belongs only under goals (i)–(ii); **not** the (iii) mechanism” (`part_ii` ll.96–97, 112–113).
  - sol_gaps post-audit note (ll.229–232) records the prior FAIL and the correct W5 path.
  - Remaining problem still names Part I instantiation — not faked.

- Special check (1)+(2): **PASS.** Primary (iii) object is \(C^{(\alpha)}\); no primary \(C^{(\alpha e^{-\eta_r})}\) under Cor vanish. \(C^{(\delta e^{-\eta})}\) appears only in Thm (3) / Remark fork / optional-path disclaimer.

- [x] PASS
- [ ] FAIL — fix:

---

## Gate 2 — Scope creep
Any CREDO/CREME/CREAM/Woody-HT/general-ÂŜ treated as live math?

- Evidence: neither path mentions CREDO, CREME, CREAM, Woody-HT, or a general \(\hat S\). Live objects remain \(A(D)=\hat\theta\), \(C^{(q)}\), ZJ \((\eta,\tau,\nu)\)-stability. Forbidden-repairs Cor still contrast-only.

- Special check (3): **PASS**.

- [x] PASS (none)
- [ ] FAIL — remove:

---

## Gate 3 — Assumption warrant
Each new assumption named, used where, falsifiable?

| Assumption | Named? | Used where | Falsifiable / scoped? |
|---|---|---|---|
| (FV) joint fixed-\(\theta\) validity | Yes | Implies (OV); hyp for Cor vanish | Joint over same \((D,X,Y)\); conditional/independent-copy \(D\) not automatic |
| (ST) \((\eta,\tau,\nu)\)-stability | Yes | Thm (2); Cor vanish sequence | Design property of \(A\); rates deferred to Remaining |
| (OV) oracle validity | Yes | Direct hyp of transfer | Classical claim; (FV) sufficient if \(A_0\perp W\) |
| Common Markov kernel / no unaccounted \(A\)-\(C\) coupling | Yes | Proof sketch | Case B: OV′ / enlarged output if violated |
| Randomized \(A_r\) leaves fixed-\(\theta\) map **and** classical level \(\alpha\) unchanged | Yes (Cor vanish; sol minimal assump 6) | Goal-(iii)/W5 | Matches W5 no-recalibration |

- Special check (4): **PASS** — packaging now matches warrant: (FV) for unchanged \(C^{(\alpha)}\) map, not a recalibrated family.

- [x] PASS
- [ ] FAIL — list:

---

## Gate 4 — Math correctness
Defs consistent; hypotheses used; no silent notation fixes?

- Thm set-valued: \(B_q(w)\); (ST) on data-dependent sections; \(\nu\) of \(G^c\); \(A_0\perp W\) + common kernel → (2); \(q=\delta e^{-\eta}\) → (3). Bound math correct; (3) correctly remains the (i)–(ii) level-change consequence.
- Def Infl at fixed \(q=\alpha\): \(\mathrm{Infl}\le(e^\eta-1)\alpha+\tau+\nu\) — consistent with Cor vanish finite-\(r\) bound.
- Cor vanish: applies Thm with **\(q=\alpha\)** (not \(q=\alpha e^{-\eta_r}\)); Infl→0 under \(\eta_r\to0\), \(\tau_r+\nu_r\to0\). Matches W5/(iii).
- Notation: level in superscript, \(\theta\) in third slot — intact.
- Remark fork and Cor vanish no longer contradict each other (prior FAIL root cause closed).
- sol_gaps mention of \(C^{(\alpha e^{-\eta_r})}\) is only in the historical post-audit note labeling the bug — not the live corollary display.

- [x] PASS
- [ ] FAIL — list:

---

## Overall
- [x] ALL PASS — may proceed
- [ ] FAIL — open fix task before next phase work

**Verdict:** Prior FAIL is closed. Cor vanish primary display is \(C^{(\alpha)}\) with Infl→0; \(e^\eta\) level change stays under (i)–(ii) only. W5/(iii) packaging is correct.
