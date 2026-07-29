namespace Research.Operators.Argmax.BasicInt

/-- Index `i` is a maximizer of `s`. -/
def IsMaximizer {m : Nat} (s : Fin m → Int) (i : Fin m) : Prop :=
  ∀ j : Fin m, s j ≤ s i

/-- `i` is the unique maximizer (maximizer + strict over others). -/
def IsUniqueMaximizer {m : Nat} (s : Fin m → Int) (i : Fin m) : Prop :=
  IsMaximizer s i ∧ ∀ j : Fin m, j ≠ i → s j < s i

/-- ∞-ball: `‖δ‖_∞ ≤ ε`. -/
def LinfBall {m : Nat} (δ : Fin m → Int) (ε : Nat) : Prop :=
  ∀ i : Fin m, Int.natAbs (δ i) ≤ ε

theorem unique_implies_maximizer {m : Nat} {s : Fin m → Int} {i : Fin m}
    (h : IsUniqueMaximizer s i) : IsMaximizer s i :=
  h.1

private theorem neg_le_natAbs (a : Int) : -a ≤ ↑a.natAbs := by
  cases a with
  | ofNat n => simp [Int.natAbs]; omega
  | negSucc n => simp [Int.natAbs]; omega

/-- `natAbs ≤ ε` ↔ bounds in `ℤ`. -/
theorem natAbs_le_iff (x : Int) (ε : Nat) :
    Int.natAbs x ≤ ε ↔ -(ε : Int) ≤ x ∧ x ≤ (ε : Int) := by
  constructor
  · intro h
    have hx : x ≤ ↑x.natAbs := Int.le_natAbs
    have hnx : -x ≤ ↑x.natAbs := neg_le_natAbs x
    have hε : (↑x.natAbs : Int) ≤ ↑ε := Int.ofNat_le.mpr h
    exact ⟨by omega, by omega⟩
  · intro ⟨hlo, hhi⟩
    cases x with
    | ofNat n =>
      simp only [Int.natAbs]
      exact Int.ofNat_le.mp hhi
    | negSucc n =>
      simp only [Int.natAbs]
      -- goal: n+1 ≤ ε from -ε ≤ -n-1
      omega

end Research.Operators.Argmax.BasicInt
