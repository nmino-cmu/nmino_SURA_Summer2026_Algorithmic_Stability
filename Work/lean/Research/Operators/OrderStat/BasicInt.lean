import Research.Operators.Argmax.BasicInt

namespace Research.Operators.OrderStat.BasicInt

open Research.Operators.Argmax.BasicInt

/-- Count of coordinates `< v`, recursive on `n`. -/
def countLT : {n : Nat} → (Fin n → Int) → Int → Nat
  | 0, _, _ => 0
  | n + 1, s, v =>
      let s' : Fin n → Int := fun i => s i.castSucc
      countLT s' v + (if s (Fin.last n) < v then 1 else 0)

/-- Count of coordinates `≤ v`. -/
def countLE : {n : Nat} → (Fin n → Int) → Int → Nat
  | 0, _, _ => 0
  | n + 1, s, v =>
      let s' : Fin n → Int := fun i => s i.castSucc
      countLE s' v + (if s (Fin.last n) ≤ v then 1 else 0)

theorem natAbs_sub_comm (a b : Int) : Int.natAbs (a - b) = Int.natAbs (b - a) := by
  have h : b - a = -(a - b) := by omega
  rw [h, Int.natAbs_neg]

end Research.Operators.OrderStat.BasicInt
