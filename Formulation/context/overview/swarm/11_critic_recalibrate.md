# Wave 2 Critic — Recalibrate vs randomize

Agent: [Recalibrate vs randomize](19e7c822-30bd-4a4d-bd19-9ab9908e4258)

## Verdict

**(iii) vs Comment E = unresolved mid-edit with an authorial override that never updated the goal text.** Not a clean refinement (refinement would rewrite (iii)). Not a pure logical contradiction either (Wenbin maps E → “answers (iii)”). Nick must not collapse them into one settled sentence.

---

### 1. Is (iii) vs Comment E contradiction / refinement / mid-edit?

**Unresolved mid-edit.** Quote the clash:

> **(iii)** “what kind of procedure can be deployed to **recalibrate the uncertainty set** to satisfy (1).”

> **Comment E:** “Data-driven policy (e.g., PTO), **no recalibration**, strategy: **data-randomize** to achieve validity guarantee, **this answers (iii)**.”

If you take the words seriously:

| Reading | Why it fails |
|---|---|
| Pure contradiction | Wenbin says E *answers* (iii), so he thinks they cohere. |
| Clean refinement | Then (iii) would now say “randomize / stabilize,” not “recalibrate.” It doesn’t. |
| Mid-edit | Goal block still uses recalibration language; Comment E forbids recalibration and substitutes a different mechanism. Same paragraph stack, incompatible verbs, no rewrite. |

Adversarial punch: **Comment E does not refine (iii); it answers a different question under (iii)’s label.** (iii) asks for a procedure on the *uncertainty set*. E answers with a procedure on the *data/policy* (randomize selection). Calling that “answers (iii)” is authorial fiat, not textual consistency. Until (iii) is rewritten, treating “recalibration” as live research language is a Nick error.

The swarm note softens this to “Tension: (iii) says ‘recalibrate’ but Comment E prefers no recalibration.” That understates it. Prefer: **goal text and strategy comment are out of sync; E overrides method, (iii) still dirty.**

---

### 2. CURRENT INTENT for methods (what Nick should treat as live)

From **Wenbin comments only**, not Nick prose:

1. **Narrow UQ setting** — “focusing on one specific objective (e.g., uncertainty quantification).”
2. **No recalibration** — explicit.
3. **Method class:** data-driven policy (e.g. PTO); **data-randomize** for validity; paper direction = **structured noise** via **inverse optimization**; cite Tijana / winner’s curse / algorithm stability.
4. **Decompose:** (I) stability of constrained opts under one-point change (assumptions on \(\hat f,\hat g\)); (II) post-hoc inference on top.
5. **Provisional:** “We may modify the problem setting… if we find there are more principal versions.”

So current method intent is: **stabilize / randomize the selection (policy), not recalibrate \(C\)**. Goals (i)–(ii) remain live; (iii) is live only as “restore (1),” **not** as “recalibrate \(C\).”

---

### 3. Must be labeled INCOMPLETE — not Current

| Artifact | Why incomplete |
|---|---|
| **Abstract** | “TBA” |
| **§3.2 Common Setup** | Empty heading |
| **§3.3 Part I … Problem Formulation** | Empty |
| **§3.4 Part II … Problem Formulation** | Empty |
| **pp.1–2 + §3.1 “general framework”** | Nick draft; contradicts Wenbin “narrow” |
| **Goal (iii) wording** | Still says recalibrate; superseded by Comment E |
| **Notation** | `C(X;D, α)` introduced, `θ` in the sentence and in (1) |
| **Treating H2 as “complete formulation”** | Bodies of Parts I/II do not exist |

Calling the swarm file “Wave 1 — Wenbin H2 problem setup **(complete)**” is false advertising relative to the PDF. H2 is a **later annotated draft**, not a finished formulation.

---

### 4. Corrections required in overview language

Fix `03_wenbin_H2.md` (and any Nick summary that mirrors it):

1. **Drop “(complete)”** from the title. Replace with mid-edit / stubbed Parts I–II.
2. **Do not write** “(iii) restore validity” as if that healed the conflict. Write:  
   **(iii) as written = recalibrate \(C\); Comment E override = no recalibration, data-randomize answers (iii).** Status: unresolved mid-edit.
3. **Methods Current Intent** must quote Comment E’s bans and positives, not Nick’s “convert into a stable selection algorithm” general-framework pitch.
4. **Label explicitly Incomplete:** Abstract TBA; empty Part I/II; Nick “general/genedoral framework” prose on pp.1–2 and §3.1.
5. **Notation bug — record as error, not soft note:**  
   > “Let \(C(X;D,\alpha)\) denote an uncertainty set constructed with … hyperparameter \(\theta\)”  
   then (1) uses \(C(X;D,\theta)\). Overview should say: **introducer uses \(\alpha\), definition and (1) use \(\theta\) — fix to one argument.**
6. **Narrow vs general:** Wenbin: “We need to **narrow**…” vs Nick still on page 1/4: “finding a **general framework**…” Overview must mark Nick prose as **non-authoritative / superseded**, not parallel Absolute Truth.
7. **Empty stubs vs “pursue i–iii”:** “Next Nick actions: Fill Part I then Part II” is fine; implying H2 already *is* the filled formulation is not.

---

**Bottom line Nick should act on:** Method intent = **no recalibration; randomize/stabilize the data-driven policy (structured noise / inverse opt)**. Goal (iii)’s word “recalibrate” is stale text. Parts I/II and the general-framework intro are **INCOMPLETE stubs**, not current theory.