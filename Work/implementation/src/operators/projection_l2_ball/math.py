"""Projection onto the l2 ball - feasible-ball identity (Real, limited)."""
from __future__ import annotations

OPERATOR = "projection-l2-ball"
THEOREM_ID = "projection-l2-ball-feasible-ball-identity"
EVALUATION_METHOD = "PROJECTION_L2_BALL_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ("If proj fixes InSet pointwise and the closed epsilon-ball about x lies in InSet, then for all |x'-x|<=epsilon one has proj(x')=x' and proj(x)=x (Projection onto the l2 ball: feasible-ball identity, Mathlib Real).")
SHARPNESS_STATEMENT = ('If some y in the epsilon-ball is infeasible, the universal feasible-ball hypothesis fails (sharpness of the interior premise).')

def proj_id(z: float) -> float:
    return z

def ball_feasible(x: float, eps: float, inset) -> bool:
    # sample endpoints + center on R as computational proxy of Int ball
    for y in (x - eps, x, x + eps):
        if not inset(y):
            return False
    return True
