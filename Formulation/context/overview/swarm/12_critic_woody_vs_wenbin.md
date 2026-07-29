# Wave 2 Critic — Woody vs Wenbin authority

Agent: [Woody vs Wenbin](44f8f894-20eb-4183-bfd2-ffbbb2fe0df5)

## Verdict

**A and B both win on different axes; neither is “highest overall.”** H2 and Meeting 3 **specialize**, they do not conflict. The overview’s flat ranking is the main error: it collapses problem statement, research agenda, and methodology into one stack, then crowns H2.

---

## Contested claims (attack → reconcile)

| Claim | Status | Why |
|---|---|---|
| **A** H2 highest for current math | **Partially true, overclaimed** | Best *available written math object*; not proven = July 2 Overleaf; Parts I/II empty; mid-edit |
| **B** M3 Woody = current plan | **True for agenda/vision** | Woody sets class of problem + end product; does **not** fix the UQ equations |
| **C** July 2 authorizes methods | **True, narrowly** | Methods for Wenbin’s Overleaf setup — not a blank check, not identity with H2 PDF |
| **D** Woody outranks Wenbin | **True institutionally, false as document rank** | Faculty veto ≠ day-to-day math authorship |

---

## 1. H2 vs Meeting 3: SPECIALIZE, not conflict

**Meeting 3 (Woody) — class + agenda**

> “the policy is … not just like a random data-dependent selection algorithm, it is a solution to an optimization problem”
>
> “one of the top priorities is to formally define the stability of the policy induced by an optimization problem”
>
> “should I trust this decision or not? … end product I could envision”
>
> Challenge: “discontinuity induced by the optimization structure”

**H2 (Wenbin) — instance + theorems**

- Object: \(C(X;D,\theta)\) with validity (1); \(\hat\theta(D)=\arg\min \hat f\) s.t. \(\hat g\le 0\) (2)
- Goals (i)–(iii): when (1) survives \(\hat\theta(D)\); miscoverage; restore validity
- Decompose: (I) stability of constrained opts; (II) post-hoc inference on top
- Narrow: “one specific objective (UQ example)”

**Mapping (specialization, not contradiction)**

| M3 directive | H2 specialization |
|---|---|
| Policy = opt solution | \(\hat\theta(D)\) from constrained program (2) |
| Define stability of that class | Part I: one-point change / assumptions on \(\hat f,\hat g\) |
| Stabilization → valid inference | Goals (i)–(iii) + Part II |
| AI → optimizer; “trust this decision?” | Application frame; math lands as UQ validity after data-dependent \(\hat\theta\) |
| Discontinuity challenge | Structural reason Part I is hard (not contradicted) |

**Only soft tensions (not M3↔H2 war):**
- Internal H2: goal (iii) says “recalibrate”; Comment E prefers **no recalibration / data-randomize**
- Product framing: M3 = HT trust question; H2 = coverage/miscoverage — related, not identical
- M3 notation \(\theta/\tilde s\) was incomplete; H2 is the later formalization attempt (stubs still empty)

Meeting forensic already flags the right question: *“judge whether specialization or conflict”* → **specialization**.

---

## 2. Who controls what

| Layer | Controller | Evidence |
|---|---|---|
| **Research agenda / vision / end product** | **Woody (M3)** | Policy-as-opt, discontinuity, AI+optimizer, HT “trust this decision?” |
| **Written mathematical problem statement** | **Wenbin (July 2 Overleaf; H2 as stand-in)** | “aligns closer to what we intended”; H2 [Wenbin] comments |
| **Methodology phase authorization** | **Wenbin July 2 email** | “begin brainstorming the methodologies we could use to approach **this** problem” |
| **Institutional direction / veto** | **Woody (faculty)** | Title page: Faculty mentor Woody; Graduate mentor Wenbin; M2: present formulation **to Woody** before finalizing |
| **Operational narrowing / day-to-day math** | **Wenbin** | July 2 rewrite; H2 inline comments; “setting may be modified if a more principal version appears” |
| **Student proposals (H1, June 25)** | **Subordinate** | Email forensic: no approval of primitive-operation framework; Woody receipt ≠ endorsement |

So: Woody owns **what kind of project**; Wenbin owns **which equations are live**; July 2 owns **permission to invent methods for those equations**.

---

## 3. Corrected layered authority model

```
L0  Institutional
    Woody (faculty mentor)  >  Wenbin (graduate mentor)  >  Nick
    Veto / agenda-setting; does NOT auto-rank every PDF above every other PDF

L1  Research agenda (spoken current plan)
    Meeting 3 Woody directives
    = optimization-induced policy stability; discontinuity; AI→optimizer;
      HT end product “trust this decision?”
    Survives unless Woody revises in a later meeting/email

L2  Mathematical problem statement (written object)
    July 2 Overleaf (authoritative when recovered)
    H2 PDF = best available stand-in, NOT proven identical
      CreationDate 2026-07-26; Parts I/II empty; mid-edit
    Controls: UQ θ̂ via constrained opt; goals i–iii; Part I/II program

L3  Methodology authorization
    Wenbin 2 Jul 2026 email ONLY for methods on L2 setup
    Does not resurrect H1 as controlling framework

L4  Terminology / process constraints
    “post-hoc inference” (Nick-attested Wenbin suggestion, 12 Jun)
    Flexible: H2 Comment — may modify setting if more principal

L5  Historical / reference only
    H1 catalog; M1–M2 plans; June 25 student proposal; adaptive regret; quantization
```

**Conflict rule:** L1 constrains *class*; L2 fills *instance*. If H2 ever leaves “policy = opt solution,” L1 (Woody) wins until Woody accepts the departure. If someone asserts a general selector framework against L2’s UQ narrowing, L2 wins for theorems-in-progress. Methods must target L2 (L3).

---

## 4. Errors in the overview’s flat ranking

The overview §Authority hierarchy ranks for “the current mathematical problem”:

1. H2 → 2. Meeting 3 → 3. Emails → 4. H1 → 5. earlier meetings

**Failures:**

1. **Wrong question for a flat list.** Agenda ≠ math statement ≠ methods. Ranking them as one tower forces a fake winner.
2. **Puts M3 under H2 for everything.** M3 is *higher* for agenda/end product; H2 is *higher* only for written equations. The overview’s own §Current state already separates these correctly (“Problem: H2” / “Motivation: Meeting 3” / “Immediate work: E1”) — that layered model contradicts the flat §Authority list.
3. **Equates H2 with July 2.** Timeline says `companion = H2`; email forensic: *“Emails do NOT prove identity.”* H2 CreationDate is July 26, Parts empty — stand-in, not crown.
4. **Central rule overreach:** “Wenbin’s annotated problem setup controls what the project is currently trying to prove” — true for L2 theorems; false if read as erasing Woody’s HT/discontinuity/policy-as-opt constraints.
5. **“Highest formulation authority” on an incomplete draft.** Empty Part I/II cannot be absolute authority for finished math; it is authority for *direction of formalization*.
6. **Claim D smuggled into document rank.** Woody outranks Wenbin as mentor; that does not put M3 transcript above Wenbin’s written setup for equation-level control after Woody delegated formulation work and did not contradict the July 2 handoff in-record.

---

## Settled answers to your four questions

1. **Specialize.** M3 = class/agenda; H2 = UQ constrained-opt instance + goals i–iii. Soft internal H2 tension on recalibrate vs randomize; not M3 vs H2.
2. **Controls:** agenda→Woody/M3; math statement→Wenbin Overleaf/H2 stand-in; methods→July 2 email for that setup; institutional veto→Woody.
3. **Layered model above** (L0–L5), not a single ranking.
4. **Overview error:** one stack crowned H2; ignore provenance gap; contradict its own better “Current state” layering.

**Practical rule for Nick:** prove theorems against **H2’s (1)(2)/(i)–(iii)**; keep them inside Woody’s **opt-induced policy** class; invent methods only under the **July 2** authorization; treat H1 as scrapbook.