import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Algebra.Order.Field.Basic

namespace Research.Operators.Argmax.Basic

/-- Index `i` is a maximizer of real scores `s`. -/
def IsMaximizer {m : Nat} (s : Fin m → ℝ) (i : Fin m) : Prop :=
  ∀ j : Fin m, s j ≤ s i

/-- `i` is the unique maximizer (maximizer + strict over others). -/
def IsUniqueMaximizer {m : Nat} (s : Fin m → ℝ) (i : Fin m) : Prop :=
  IsMaximizer s i ∧ ∀ j : Fin m, j ≠ i → s j < s i

/-- ∞-ball: `‖δ‖_∞ ≤ ε` for real perturbations. -/
def LinfBall {m : Nat} (δ : Fin m → ℝ) (ε : ℝ) : Prop :=
  ∀ i : Fin m, |δ i| ≤ ε

theorem unique_implies_maximizer {m : Nat} {s : Fin m → ℝ} {i : Fin m}
    (h : IsUniqueMaximizer s i) : IsMaximizer s i :=
  h.1

/-- `|x| ≤ ε` ↔ `-ε ≤ x ∧ x ≤ ε`. -/
theorem abs_le_iff (x ε : ℝ) : |x| ≤ ε ↔ -ε ≤ x ∧ x ≤ ε :=
  abs_le

end Research.Operators.Argmax.Basic
