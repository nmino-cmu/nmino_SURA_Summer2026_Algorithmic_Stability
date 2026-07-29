"""Feasible-subset maximum - unique-max Argmax-margin reduction (Real)."""
from __future__ import annotations
from operators.argmax.math import ArgmaxInstance, adversarial_break, invariance_holds

OPERATOR = "feasible-subset-maximum"
THEOREM_ID = "feasible-subset-maximum-margin"
EVALUATION_METHOD = "FEASIBLE_SUBSET_MAXIMUM_MARGIN_COMPUTATIONAL_V1"
THEOREM_STATEMENT = ('Let m>=2 and let scores be constructed by (feasible-subset scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Feasible-subset maximum reduces to Argmax margin).')
SHARPNESS_STATEMENT = ('If gamma<=2*epsilon with unique maximizer i*, some ||delta||_inf<=epsilon destroys uniqueness of i* (Argmax margin sharpness).')

def select_winner(scores):
    return ArgmaxInstance(scores).unique_maximizer()

def stable(scores, epsilon):
    return invariance_holds(scores, epsilon)
