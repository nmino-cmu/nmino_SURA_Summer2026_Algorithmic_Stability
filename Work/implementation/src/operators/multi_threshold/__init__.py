"""Multi-threshold operator research package."""

from operators.multi_threshold.math import (
    EVALUATION_METHOD,
    OPERATOR,
    SHARPNESS_STATEMENT,
    THEOREM_ID,
    THEOREM_STATEMENT,
    MultiThresholdInstance,
    adversarial_flip,
    multi_stable,
    multi_threshold_count,
    stability_margin,
)
from operators.multi_threshold.verify import (
    claim_is_multi_threshold_preservation,
    verify_multi_threshold_preservation,
)
from operators.multi_threshold.workflow import run_multi_threshold_preservation_workflow

__all__ = [
    "EVALUATION_METHOD",
    "OPERATOR",
    "SHARPNESS_STATEMENT",
    "THEOREM_ID",
    "THEOREM_STATEMENT",
    "MultiThresholdInstance",
    "adversarial_flip",
    "claim_is_multi_threshold_preservation",
    "multi_stable",
    "multi_threshold_count",
    "run_multi_threshold_preservation_workflow",
    "stability_margin",
    "verify_multi_threshold_preservation",
]
