"""Constraint-threshold conjunction - threshold constraint via MultiThreshold pass-count core."""
from __future__ import annotations
from operators.multi_threshold.math import adversarial_flip, multi_stable, multi_threshold_count

OPERATOR = "constraint-threshold-conjunction"
THEOREM_ID = "constraint-threshold-conjunction-conjunction-preservation"
EVALUATION_METHOD = "CONSTRAINT_THRESHOLD_CONJUNCTION_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ('Under coordinatewise epsilon-stability of each threshold, the multi-threshold pass-count is preserved; hence the conjunction (all-pass) bit is preserved (Constraint-threshold conjunction).')
SHARPNESS_STATEMENT = ('Multi-threshold sharpness: a near-cut coordinate admits an epsilon move changing the pass-count (hence the conjunction bit may flip).')
