# Audit: Part I randomized design (η,τ,ν) rates for noisy (2)

Deliverable: Part I design lemmas + proof sketch + noisy-objective self-check  
Path(s): `research/formal/part_i_randomized_design.tex`, `research/proofs/part_i_randomized_design_sketch.md`, `research/experiments/noisy_objective_stability_demo.py`  
Date: 2026-07-27  
Auditor: subagent (4-gate)  
Ceiling: `writeup/Problem_Writeup.tex` — \(\hat\theta\) from (2); goal (iii) = data-randomize selection, **no** \(\mathcal{C}\) recalibration.

Special checks requested:
1. Do rates feed Cor vanish at **fixed** \(C^{(\alpha)}\) (small \(\eta\)), not \(e^\eta\)-level recalibration?
2. No LASSO-PoSI / CREDO / CREME live import?
3. Are Ass.\ diam / Lip / conc / uniq warranted, with gaps flagged?
4. Is the math of \(b=2\varepsilon/\eta\) and \(\beta=\eta/(2\varepsilon)\) sound?

---

## Gate 1 — Wenbin coverage
Advances (1)(2), goals (i)–(iii)/W5, Part I and/or Part II?

- Quote writeup line served:
  - Selected object from constrained opt (2): writeup ll.50–61.
  - Goal (iii) / no recalibration: writeup ll.78–80, Remark ll.83–87.
  - W5 data-randomize selection: writeup ll.115–116.
  - Part I studies (2); rates here are the **randomized** design bridge that Part II Cor.\ vanish consumes (not LOO displacement — that sits in `part_i_stability.tex`).

- Evidence in deliverable:
  - Setup is writeup (2) with selected object \(\tilde\theta\) (randomized version of \(\hat\theta\)).
  - Cor.\ small-η: sequence \(\eta_r\to 0\), \(\tau_r+\nu_r\to 0\) feeds Part II Cor.\ vanish at **fixed classical level of \(\mathcal{C}\)** (no recalibration); \(e^\eta\)-inflation of \(\mathcal{C}\) labeled goals (i)–(ii) only (`part_i_randomized_design.tex` Cor.~\ref{cor:small-eta}, Remark “What is not claimed”).
  - Sketch §Corollary small-η and demo docstring match: randomize selection only; do not touch \(\mathcal{C}\).
  - Demo run OK (`noisy_objective_stability_demo: OK`).

- Special check (1): **PASS.** Design knobs are \(\eta\) (via \(b\) or \(\beta\)); packaging is small-\(\eta\) → Infl\(\to 0\) at fixed \(C^{(\alpha)}\), not level change.

- [x] PASS
- [ ] FAIL — fix:

---

## Gate 2 — Scope creep
Any CREDO/CREME/CREAM/Woody-HT/general-ÂŜ treated as live math?

- Evidence: no CREDO, CREME, CREAM, Woody-HT, or general \(\hat S\). Live object is noisy / soft selection of \(\tilde\theta\) for writeup (2).
- LASSO / PoSI appear only as **negative** citations (“does **not** import”; “remapped from LASSO to general (2)”; sketch “Non-import”). ZJ Props.\ 2/4 / Ex.\ 1 used as rate **templates** only.
- Special check (2): **PASS.**

- [x] PASS (none)
- [ ] FAIL — remove:

---

## Gate 3 — Assumption warrant
Each new assumption named, used where, falsifiable?

| Assumption | Named? | Used where | Falsifiable / scoped? |
|---|---|---|---|
| Ass.\ diam | Yes | Lem.\ lin-lap optional dual-Lap branch (“scaled by diameter \(D\)”) | On good event; finite \(D\) in fixed norm. **Not** needed for finite RNM / Gibbs rates. |
| Ass.\ Lip (\(L\)) | Yes | Pulled in by Ass.\ diam–uniq range on Lem.\ lin-lap; **\(L\) never appears in any displayed rate** | Falsifiable Lipschitz claim, but **unused** in proofs/rates as written. Sketch says “used only where stated” — nowhere stated in a rate step. |
| Ass.\ conc | Yes | All three lemmas (good event \(E\); \(\varepsilon,\nu\)) | Strong form \(\Theta_0=\{g^\star\le 0\}\); tex flags Hausdorff weakening. Concrete \(\varepsilon(n),\nu(n)\) for project \(\hat f,\hat g\) **deferred** (sketch Gap / Status) — honest, not smuggled. |
| Ass.\ uniq | Yes | RNM / lin-lap (well-defined argmin r.v.); soft only if argmax post-process | Soft-argmin sampling from \(\pi_\beta\) does not need uniqueness of \(\arg\min\hat f\) — correctly softened in Lem.\ soft. |

- Special check (3): **FAIL** on warrant of Ass.\ Lip (named, unused). Diam / conc / uniq are warranted with gaps flagged; conc instantiation correctly open.

- [ ] PASS
- [x] FAIL — list:
  1. Drop Ass.\ Lip, or use \(L\) in a stated rate/utility bound, or mark it explicitly as unused / reserved (not a hyp of Lem.\ lin-lap via `Ass diam--uniq`).
  2. Keep conc gap as open instantiation (already flagged) — do not treat as proved.

---

## Gate 4 — Math correctness
Defs consistent; hypotheses used; no silent notation fixes?

- Defs.\ indistinguishability / \((\eta,\tau,\nu)\)-stability match ZJ Defs.\ 1–2; oracle \(A_0\) may depend on \(P\) not realized \(\mathcal{D}\).
- Writeup notation: miscoverage level stays \(\alpha\); optimized parameter is \(\theta\) / \(\tilde\theta\) — no silent α/θ swap.
- Special check (4) — scales:
  - **Soft:** on \(E\), \(|\hat f-f^\star|\le\varepsilon\) ⇒ pointwise density factor \(\le e^{\beta\varepsilon}\) and \(Z^\star/Z\le e^{\beta\varepsilon}\) ⇒ max divergence \(\le 2\beta\varepsilon\). Setting \(\beta=\eta/(2\varepsilon)\) ⇒ \((\eta,0)\) on \(E\) ⇒ \((\eta,0,\nu)\)-stable. **Sound.**
  - **RNM:** \(b=2\varepsilon/\eta\) matches the same exponential-mechanism / Gibbs factor-of-two (equivalently \(\beta=1/b\)). Classic Laplace report-noisy-max with per-coordinate change \(\le\varepsilon\) is often analyzed with \(b=\varepsilon/\eta\) (factor 1); the stated \(2\varepsilon/\eta\) is then **conservative but sound** (implies the claimed \(\eta\)-indistinguishability). Sketch’s density-ratio citation is consistent with the factor-2 bound. **Sound.**
- Demo: \(b=2\varepsilon/\eta\); more noise ⇒ less brittle; empirical max log-ratio \(\lesssim\eta\) with large MC slack — shape check only, not a proof. Ran successfully.
- **Lem.\ lin-lap overclaim:** tex asserts that for a.e.\ \(\xi\),
  \[
  \arg\min_{\theta\in\Theta_0}\{\hat f(y;\theta)+\langle\xi,\theta\rangle\}
  \]
  is attained at an extreme point whenever \(\Theta_0\) is a polytope — **false** for nonlinear \(\hat f\) (minimizer can be interior). Linearity / single LMO is required **before** that claim. The sketch already restricts to “linear (or FW-LMO)”; the formal lemma’s opening sentence does not. Rate conclusion under linearity/LMO is fine; the unrestricted extreme-point sentence is not.

- [ ] PASS
- [x] FAIL — list:
  1. In Lem.\ lin-lap, put “\(\hat f\) linear on \(\Theta_0\), or replace \((2_\xi)\) by one LMO” in the hypothesis **before** claiming extreme-point attainment (align tex with sketch).
  2. No change needed to \(b=2\varepsilon/\eta\) or \(\beta=\eta/(2\varepsilon)\) for soundness of the claimed \((\eta,0,\nu)\) rates.

---

## Overall
- [ ] ALL PASS — may proceed
- [x] FAIL — open fix task before treating Part I design as closed

**Fix task (minimal):**
1. Lem.\ lin-lap: require linear \(\hat f\) / LMO before extreme-point + RNM reduction.
2. Ass.\ Lip: remove from live hyps, or actually use \(L\), or label unused/reserved so `Ass diam--uniq` does not imply a used Lipschitz rate.

**Notes:** Special checks (1), (2), and the \(b\)/\(\beta\) half of (4) pass cleanly against the writeup ceiling (fixed \(C^{(\alpha)}\), no CREDO/CREME/LASSO-PoSI live import, scales sound). Failures are local warrant/claim hygiene, not a (iii)-packaging contradiction of the kind that failed the earlier Part II Cor-vanish audit.
