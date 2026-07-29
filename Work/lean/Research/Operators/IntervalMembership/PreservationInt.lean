import Research.Operators.Argmax.BasicInt

namespace Research.Operators.IntervalMembership.PreservationInt

open Research.Operators.Argmax.BasicInt

/-- Closed interval membership. -/
def inInterval (x L U : Int) : Bool :=
  decide (L ≤ x ∧ x ≤ U)

/- STATEMENT_BEGIN -/
def IntervalMembershipPreservationProp : Prop :=
  ∀ (x L U : Int) (ε : Nat) (x' : Int),
    L ≤ U →
    Int.natAbs (x' - x) ≤ ε →
    ((L + (ε : Int) ≤ x ∧ x ≤ U - (ε : Int) → inInterval x' L U = true) ∧
     ((x < L - (ε : Int) ∨ U + (ε : Int) < x) → inInterval x' L U = false))

/-- Sharpness near the left endpoint on the pass side: `L ≤ x < L+ε` ⇒ push down fails. -/
def IntervalMembershipSharpnessProp : Prop :=
  ∀ (x L U : Int) (ε : Nat),
    L ≤ U →
    (L ≤ x ∧ x < L + (ε : Int)) →
    ∃ x' : Int, Int.natAbs (x' - x) ≤ ε ∧ inInterval x' L U = false
/- STATEMENT_END -/

theorem interval_membership_preservation : IntervalMembershipPreservationProp := by
  intro x L U ε x' hLU hball
  have hb := (natAbs_le_iff (x' - x) ε).mp hball
  refine And.intro ?pass ?fail
  · intro ⟨hlo, hhi⟩
    have : L ≤ x' ∧ x' ≤ U := by omega
    simp [inInterval, this]
  · intro h
    have : ¬ (L ≤ x' ∧ x' ≤ U) := by
      cases h with
      | inl hL => omega
      | inr hU => omega
    simp [inInterval, this]

theorem interval_membership_sharpness : IntervalMembershipSharpnessProp := by
  intro x L U ε hLU ⟨hxlo, hxhi⟩
  refine ⟨x - (ε : Int), ?_, ?_⟩
  · have : x - (ε : Int) - x = - (ε : Int) := by omega
    simp [this, Int.natAbs_neg]
  · have : ¬ (L ≤ x - (ε : Int) ∧ x - (ε : Int) ≤ U) := by omega
    simp [inInterval, this]

end Research.Operators.IntervalMembership.PreservationInt
