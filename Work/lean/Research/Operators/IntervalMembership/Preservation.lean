import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Argmax.Basic

namespace Research.Operators.IntervalMembership.Preservation

open Research.Operators.Argmax.Basic

/-- Closed interval membership. -/
def inInterval (x L U : ℝ) : Prop :=
  L ≤ x ∧ x ≤ U

/- STATEMENT_BEGIN -/
def IntervalMembershipPreservationProp : Prop :=
  ∀ (x L U ε x' : ℝ),
    L ≤ U →
    0 ≤ ε →
    |x' - x| ≤ ε →
    ((L + ε ≤ x ∧ x ≤ U - ε → inInterval x' L U) ∧
     ((x < L - ε ∨ U + ε < x) → ¬ inInterval x' L U))

def IntervalMembershipSharpnessProp : Prop :=
  ∀ (x L U ε : ℝ),
    L ≤ U →
    0 ≤ ε →
    (L ≤ x ∧ x < L + ε) →
    ∃ x' : ℝ, |x' - x| ≤ ε ∧ ¬ inInterval x' L U
/- STATEMENT_END -/

theorem interval_membership_preservation : IntervalMembershipPreservationProp := by
  intro x L U ε x' hLU hε hball
  have hb := (abs_le_iff (x' - x) ε).mp hball
  refine And.intro ?pass ?fail
  · intro ⟨hlo, hhi⟩
    exact ⟨by linarith, by linarith⟩
  · intro h
    intro ⟨hxL, hxU⟩
    cases h with
    | inl hL => linarith
    | inr hU => linarith

theorem interval_membership_sharpness : IntervalMembershipSharpnessProp := by
  intro x L U ε hLU hε ⟨hxlo, hxhi⟩
  refine ⟨x - ε, ?_, ?_⟩
  · simp [abs_of_nonneg hε]
  · intro ⟨h1, _h2⟩
    linarith

end Research.Operators.IntervalMembership.Preservation
