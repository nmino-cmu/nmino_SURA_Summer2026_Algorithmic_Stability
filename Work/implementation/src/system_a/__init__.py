"""system_a public API."""

from system_a.fsm import CLOSED_STATES, DiscoverySession, IllegalTransition, State, replay_control
from system_a.ir import ArtifactVersion, DiscoveryIR, ImmutableError, OwnershipError
from system_a.gates import GateDecision, GateNumber
from system_a.packager import compile_branch
from system_a.orchestrator import DiscoveryOrchestrator
from system_a.ownership import CLASS_OWNER

__all__ = [
    "DiscoverySession",
    "State",
    "IllegalTransition",
    "CLOSED_STATES",
    "replay_control",
    "DiscoveryIR",
    "ArtifactVersion",
    "OwnershipError",
    "ImmutableError",
    "GateDecision",
    "GateNumber",
    "compile_branch",
    "DiscoveryOrchestrator",
    "CLASS_OWNER",
]
