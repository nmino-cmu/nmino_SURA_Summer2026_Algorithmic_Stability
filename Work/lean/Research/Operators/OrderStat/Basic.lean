import Mathlib.Data.Real.Basic

noncomputable section

namespace Research.Operators.OrderStat.Basic

/-- Count of coordinates `< v`, recursive on `n`. -/
def countLT : {n : Nat} → (Fin n → ℝ) → ℝ → Nat
  | 0, _, _ => 0
  | n + 1, s, v =>
      let s' : Fin n → ℝ := fun i => s i.castSucc
      countLT s' v + (if s (Fin.last n) < v then 1 else 0)

/-- Count of coordinates `≤ v`. -/
def countLE : {n : Nat} → (Fin n → ℝ) → ℝ → Nat
  | 0, _, _ => 0
  | n + 1, s, v =>
      let s' : Fin n → ℝ := fun i => s i.castSucc
      countLE s' v + (if s (Fin.last n) ≤ v then 1 else 0)

end Research.Operators.OrderStat.Basic
