"""Projection onto interval - interval clamp nonexpansiveness (Real)."""
from __future__ import annotations
import random

OPERATOR = "projection-interval"
THEOREM_ID = "projection-interval-clamp-stability"
EVALUATION_METHOD = "PROJECTION_INTERVAL_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ("Let lo<=hi and |x'-x|<=epsilon. Then |clamp(x';lo,hi)-clamp(x;lo,hi)|<=epsilon (Projection onto interval is 1-Lipschitz / nonexpansive on Int).")
SHARPNESS_STATEMENT = ('For every epsilon>=1 there exist x,y,lo,hi with lo<=hi attaining |clamp x - clamp y| = |x-y| = epsilon (Lipschitz constant 1 is sharp).')

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(x, hi))

def nonexpansive(x: float, y: float, lo: float, hi: float) -> bool:
    return abs(clamp(x, lo, hi) - clamp(y, lo, hi)) <= abs(x - y) + 1e-12

def stable(x: float, lo: float, hi: float, eps: float) -> bool:
    return abs(clamp(x + eps, lo, hi) - clamp(x, lo, hi)) <= eps + 1e-12 and abs(
        clamp(x - eps, lo, hi) - clamp(x, lo, hi)
    ) <= eps + 1e-12
