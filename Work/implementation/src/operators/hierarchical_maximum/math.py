"""Hierarchical maximum - unique-max Argmax-margin reduction (Real)."""
from __future__ import annotations
from operators.argmax.math import ArgmaxInstance, adversarial_break, invariance_holds

OPERATOR = "hierarchical-maximum"
THEOREM_ID = "hierarchical-maximum-margin"
EVALUATION_METHOD = "HIERARCHICAL_MAXIMUM_MARGIN_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ('Let m>=2 and let scores be constructed by (hierarchical stage scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Hierarchical maximum reduces to Argmax margin).')
SHARPNESS_STATEMENT = ('If gamma<=2*epsilon with unique maximizer i*, some ||delta||_inf<=epsilon destroys uniqueness of i* (Argmax margin sharpness).')

def select_winner(scores):
    return ArgmaxInstance(scores).unique_maximizer()

def stable(scores, epsilon):
    return invariance_holds(scores, epsilon)
