# Wave 1/2 — Overview assumption attacker

Agent: [Overview attacker](6819b02b-8634-4d08-aafb-0b33dec32e60)

## FINDINGS (severity-ranked)

### CRITICAL

**1. “July 2 Overleaf = H2” is false / unsupported — overview asserts it anyway**

- Timeline: `E1; companion = H2` (line 279).
- Missing evidence: “Exact July~2 Overleaf … (H2 is the best available stand-in)” (line 591) — **stand-in ≠ identity**.
- E1 lists “The actual July~2 Overleaf problem setup” as **missing companion evidence** and says attachments + Overleaf text are “essential.”
- H2 PDF `/CreationDate` = `D:20260726211151Z` (**26 Jul 2026**), same day as Downloads `-8`, **not** 2 Jul.
- E1 authorizes methodologies for Wenbin’s **Overleaf** draft; nothing equates that draft to the July 26 `-8`/H2 binary.

**Verdict:** Equating them is the overview’s worst overclaim. At best: *candidate descendant / best available stand-in; identity unproven.*

---

**2. “H2 is highest authority” / “Advisor-authored narrowing” — overstated and partly wrong**

| Overview claim | Primary reality |
|---|---|
| Highest for current math problem | E1 Takeaway: ground in **July 2 Overleaf + June 29 discussion** — Overleaf **absent**; H2 is a later hybrid |
| “Advisor-authored narrowing” (line 92) | Authors: **Nicholas Mino, Wenbin Zhou, and Shixiang Zhu**; Abstract **TBA** |
| Controlling formulation | pp.1–2 = student general-framework language; p.2 = **Meeting 3 Woody notes pasted as unfinished text**; p.3 = Wenbin UQ comments; §§3.2–3.4 **empty stubs** |

Putting incomplete H2 **above** Meeting 3 (Woody, faculty, current-plan speech) and above the **missing** Overleaf is editorial inflation. Wenbin’s `[Wenbin]:` UQ block is high-authority **commentary**, not a finished advisor-approved theorem statement. H2 itself says the setting “may be modified.”

---

### HIGH

**3. `papers/` “out of scope / not formulation history” — packaging rule sold as epistemic fact**

- Out-of-scope: “PDFs themselves beyond citation / role in the timeline … library, not formulation history” (lines 78–79).
- Same document: PPI + algorithmic/post-selection stability “**changed the active question**” (Literature integration).
- T1 Meeting 3: Woody makes those papers **priority reading** and constitutive of the current plan.

**Verdict:** Fine as “don’t dump paper PDFs into `history/`.” **Wrong** as “papers aren’t part of formulation history.” The pivot is paper-driven per T1.

---

**4. Idea abandonment statuses — editorial hardening beyond transcript speech**

| Idea | Overview | Primaries |
|---|---|---|
| **A Quantization** | “Superseded / **abandoned** as primary”; Open problems: “**Abandoned**” | T1: Woody redirected; “NO LONGER THE PLAN as a **primary**”; remnant as model-error special case. No advisor “abandon forever.” |
| **B Adaptive regret** | “No longer the plan”; also “later **abandoned** as the active agenda” | T1: Meeting 3 does **not** say “we abandon adaptive regret.” Pivot by reframing. Supersession rests on **editorial** `\PlanNote` boxes (T1 admits those are not transcript). Supported as *not active*; “abandoned” is stronger than spoken evidence. |
| **C Sequential CREAM / solver error** | “Abandoned as active / Unknown if permanently discarded” | T1: “**Backup only; not active**”; “unless later explicitly revived.” “Abandoned” overstates permanence. |

---

**5. Silent sanitization of H2 math**

H2 writes: “Let \(C(X;D,\alpha)\) denote … hyperparameter \(\theta\)” then uses \(C(X;D,\theta)\) in (1). Overview prints clean \(C(X;D,\theta)\) only — hides a primary inconsistency.

---

### MEDIUM

**6. Chronology: H1 as “earlier version” vs H2**

Evolution section: “Earlier version (H1 / June~25)” → H2. H1 PDF is dated **26 Jul 2026** (same day as H2 compile). June 25 email is earlier; the H1 **artifact** is not. Downloads `-2` is dated **29 Jun** (Meeting 3 day) — a survey existed then; overview collapses email / Meeting 3 slides / July 26 PDF.

**7. “Narrowed by advisors” (plural) to UQ**

Meeting 3: Woody → optimization-induced **policies** + hypothesis-testing trust. H2: Wenbin → **UQ hyperparameter** example. UQ specialization is Wenbin’s, not co-approved by Woody in-corpus.

**8. “post-hoc inference” as advisor requirement**

E1: Nick says he added the phrase per Wenbin’s suggestion; Wenbin never writes the phrase in-thread. “Wenbin’s suggestion (student-attested)” ≠ “advisor-authored mandate in email body.”

**9. Status “Current with revisions” for H2**

Abstract TBA; §§3.2–3.4 empty. More accurately: **draft / incomplete controlling *comments*, not a finished current writeup.**

**10. Authority stack ranks emails below Meeting 3, but treats July 2 email as authorizing H2**

Internal tension: email is #3, yet July 2 is used to crown H2 as #1.

---

### LOW (still real)

- “Presented in spirit at Meeting 3” for H1 — weasel; Meeting 3 had an example compilation (possibly Downloads `-2`), not necessarily July 26 H1.
- “H2 replaces” Meeting 2 Overleaf path — replacement agent is **Meeting 3 pivot**, not H2 text (H2 never mentions CREAM/regret).
- Angelopoulos vs Zrnic attribution follows T1 ASR; H1 correctly cites Zrnic–Jordan — overview hedges, still inherits Woody’s mis-speak without flagging.

---

## SUPPORTED CLAIMS (with citations)

| Claim | Evidence |
|---|---|
| H1 = Downloads `-5`/`-6`/`-7` (byte-identical) | MD5 `00964d53…` all match; overview triplicate note OK |
| H2 = Downloads `-8` | MD5 `40509c2e…` match |
| Meeting 3 = current spoken plan: stability of optimization-induced policies; AI+optimizer; trust as HT; PPI + post-selection stability reading | T1 Meeting 3 Woody turns + Plan Evolution table |
| Adaptive regret was active at Meeting 2, not active after Meeting 3 | T1 M2 plan + M3 current plan / editorial superseded tags |
| Quantization redirected away from primary engineering plan | T1 M2 Nick recount + PlanNote |
| Sequential CREAM / model-solver error = Wenbin **backups**, not M3 direction | T1 Wenbin “backup plans” |
| June 25 = student primitive/stabilized-selection proposal | E1 Nick email 25 Jun |
| July 2: Wenbin drafted Overleaf setup “aligns closer to what we intended”; Nick to brainstorm methodologies | E1 Wenbin 2 Jul; Nick 3 Jul ack |
| “post-hoc inference” added after Wenbin suggestion (Nick’s attestation) | E1 12 Jun Nick email |
| Wenbin H2 comments: intersection; narrow to one objective (UQ eg.); Part I/II decompose; setting may change; PTO/structured noise notes | H2 p.1, p.3 `[Wenbin]:` blocks |
| H2 goals (i)–(iii) and eqs. conceptually matching (1)–(2) | H2 p.3 (modulo \(C(X;D,\alpha)\) typo) |
| §§3.2–3.4 stubs / incomplete | H2 pp.5–7 empty |
| H1 template \(\hat S=A(D)\), \(\tilde S=\tilde A(D;\xi)\), certificates; primitives; best-first proposed theorem | H1 §§3, 8.1–8.4 |
| Missing: exact July 2 Overleaf, July 2 attachments, June 11 notes | E1 Missing Companion Evidence; overview correctly echoes gaps (then undermines them via “companion = H2”) |

---

## REQUIRED CORRECTIONS

1. **Delete or rewrite “companion = H2.”**  
   Replace with: *July 2 Overleaf text missing; H2 (Downloads `-8`, compiled 26 Jul 2026) is an unverified stand-in / later hybrid — do not treat as identical.*

2. **Demote absolute “H2 = highest authority.”**  
   Split authority:
   - **Direction / agenda:** Meeting 3 (Woody) + July 2 email authorization  
   - **UQ working math + Wenbin comments:** H2 p.3 `[Wenbin]:`  
   - **Controlling Overleaf text:** **MISSING**  
   Rank H2 as *best available annotated draft*, not apex law.

3. **Stop calling H2 “Advisor-authored.”**  
   Use: *co-authored draft (Nick/Wenbin/Woody) with inline Wenbin commentary; body mixes student template, Meeting 3 notes, and Wenbin UQ setup.*

4. **`papers/`:**  
   Keep as *not duplicated into `history/`*; remove “not formulation history.” Say: *priority/pivot papers are in-scope for evolution; PDFs live in `papers/`.*

5. **Idea statuses — match T1 vocabulary:**  
   - A: *Redirected / no longer primary* (remnant: model error)  
   - B: *No longer the active plan (as of M3); explicit abandonment not spoken*  
   - C: *Backup only; not adopted; revive status unknown*  
   Drop bare “Abandoned” unless quoting editorial tags and labeling them editorial.

6. **Flag H2 notation bug** \(C(X;D,\alpha)\) vs \(\theta\); don’t silently “fix” it.

7. **Separate June 25 proposal / M3 survey / July 26 H1 PDF** in the timeline; don’t call the July 26 H1 PDF “earlier than H2.”

8. **Attribute UQ narrowing to Wenbin (H2),** not “advisors” plural; keep Woody’s M3 scope (policy stability + trust HT) as co-equal current vision until Woody endorses the UQ specialization in a primary.

---

**Bottom line:** The overview’s spine — *H2 crowns the project because it is the July 2 Overleaf* — fails primary-source attack. H2 is a **26 Jul hybrid draft**; the authorized Overleaf is **missing**; Meeting 3 and Wenbin comments are strong; the hierarchy as written is overconfident.