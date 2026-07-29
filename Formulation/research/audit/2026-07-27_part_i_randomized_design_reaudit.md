# Re-audit: Part I randomized design (post Lip / lin-lap fix)

Deliverable: Part I design lemmas (after Ass.\ Lip + Lem.\ lin-lap hygiene fix)  
Path(s): `research/formal/part_i_randomized_design.tex` (re-read only; sketch/demo unchanged since prior audit)  
Date: 2026-07-27  
Auditor: subagent (4-gate re-audit)  
Ceiling: `writeup/Problem_Writeup.tex` — \(\hat\theta\) from (2); goal (iii) = data-randomize selection, **no** \(\mathcal{C}\) recalibration.  
Prior FAIL: `2026-07-27_part_i_randomized_design_audit.md` —
1. Ass.\ Lip named but unused;
2. Lem.\ lin-lap claimed extreme-point for nonlinear \(\hat f\).

Special checks (re-verify prior FAIL only):
1. Ass.\ Lip labeled reserved / unused in rates (not a live hyp of rate lemmas).
2. Lem.\ lin-lap requires linear \(\hat f\) / LMO **before** extreme-point claim.
3. Prior PASSes still hold: fixed \(C^{(\alpha)}\) packaging; no CREDO/PoSI live; \(b\)/\(\beta\) sound.

---

## Gate 1 — Wenbin coverage
Advances (1)(2), goals (i)–(iii)/W5, Part I and/or Part II?

- Quote writeup line served (unchanged from prior audit):
  - Selected object from constrained opt (2): writeup ll.50–61.
  - Goal (iii) / no recalibration: writeup ll.78–80, Remark ll.83–87.
  - W5 data-randomize selection: writeup ll.115–116.
  - Part I studies (2); rates feed Part II Cor.\ vanish.

- Evidence in deliverable:
  - Setup still writeup (2) with selected \(\tilde\theta\); LASSO/PoSI still non-import.
  - Cor.\ small-η: \(\eta_r\to0\), \(\tau_r+\nu_r\to0\) at **fixed classical level of \(\mathcal{C}\)** (no recalibration); \(e^\eta\)-inflation of \(\mathcal{C}\) still goals (i)–(ii) only (`Cor.~\ref{cor:small-eta}`, Remark “What is not claimed”).
  - Fix scope did not touch packaging.

- Special check (3) packaging half: **PASS** (unchanged).

- [x] PASS
- [ ] FAIL — fix:

---

## Gate 2 — Scope creep
Any CREDO/CREME/CREAM/Woody-HT/general-ÂŜ treated as live math?

- Evidence: no CREDO/CREME/CREAM/Woody-HT/general \(\hat S\). LASSO/PoSI remain negative / remapping cites only. Live object still noisy / soft selection of \(\tilde\theta\) for (2).

- [x] PASS (none)
- [ ] FAIL — remove:

---

## Gate 3 — Assumption warrant
Each new assumption named, used where, falsifiable?

| Assumption | Named? | Used where | Falsifiable / scoped? |
|---|---|---|---|
| Ass.\ diam | Yes | Lem.\ lin-lap dual-Lap branch (scaled by \(D\)) | On good event; finite \(D\). Not needed for finite RNM / soft rates. |
| Ass.\ Lip (\(L\)) | Yes — title **“reserved / unused in rates”** | **Nowhere in live lemmas.** Body: “Not a hypothesis of Lemmas rnm–soft”; optional future utility; “Do not treat \(L\) as required for the \((\eta,0,\nu)\) rates.” No `\ref{ass:lip}` in any lemma hyp. Prior `Ass diam--uniq` pull-in of Lip is gone: lin-lap cites `Ass diam, conc--uniq` only. | Falsifiable Lipschitz claim, but explicitly reserved — not a rate hyp. |
| Ass.\ conc | Yes | All three lemmas (good event \(E\); \(\varepsilon,\nu\)) | Strong form flagged; concrete \(\varepsilon(n),\nu(n)\) still deferred — honest. |
| Ass.\ uniq | Yes | RNM / lin-lap; soft only if argmax post-process | Soft sampling correctly softened. |

- Special check (1) prior FAIL: **PASS.** Ass.\ Lip is labeled reserved/unused and is not a hypothesis of any rate lemma.

- [x] PASS
- [ ] FAIL — list:

---

## Gate 4 — Math correctness
Defs consistent; hypotheses used; no silent notation fixes?

- Defs.\ indistinguishability / \((\eta,\tau,\nu)\)-stability unchanged and sound.
- Scales \(b=2\varepsilon/\eta\), \(\beta=\eta/(2\varepsilon)\) unchanged — still sound (factor-2 density ratio).
- **Lem.\ lin-lap (prior FAIL closed):** hypothesis now states, **before** the extreme-point sentence, that \(\hat f\) is *linear* on \(\Theta_0\) **or** that \((2_\xi)\) is replaced by a single linear minimization oracle. Extreme-point attainment + RNM reduction follow only under that hyp. Explicit anti-claim: for nonlinear \(\hat f\), do **not** claim extreme-point attainment; use soft or discretize + RNM. Aligns with sketch (“linear (or FW-LMO)”).
- Notation: miscoverage \(\alpha\); optimized \(\theta\) / \(\tilde\theta\) — intact.

- Special check (2) prior FAIL: **PASS.**

- [x] PASS
- [ ] FAIL — list:

---

## Overall
- [x] ALL PASS — may proceed
- [ ] FAIL — open fix task before treating Part I design as closed

**Verdict:** Both prior FAIL items are closed. Ass.\ Lip is reserved/unused (not a live rate hyp). Lem.\ lin-lap requires linear \(\hat f\) / LMO before extreme-point. Packaging, scope, and \(b\)/\(\beta\) remain PASS.
