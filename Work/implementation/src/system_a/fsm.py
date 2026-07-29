"""Discovery session FSM (ART-A-03). Mutations only via owning DiscoveryOrchestrator instance."""

from __future__ import annotations

import weakref
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TYPE_CHECKING

from art_int.errors import ProvenanceError
from art_int.feedback import VerifierFeedbackExport, validate_feedback_for_prior
from system_a.freeze import deep_freeze
from system_a.ownership import CLOSE_REASONS, DS91_REASONS

if TYPE_CHECKING:
    from system_a.orchestrator import DiscoveryOrchestrator


class State(str, Enum):
    DS00 = "DS00"
    DS01 = "DS01"
    DS02 = "DS02"
    DS03 = "DS03"
    DS04 = "DS04"
    DS05 = "DS05"
    DS06 = "DS06"
    DS07 = "DS07"
    DS08 = "DS08"
    DS09 = "DS09"
    DS10 = "DS10"
    DS11 = "DS11"
    DS12 = "DS12"
    DS13 = "DS13"
    DS90 = "DS90"
    DS91 = "DS91"


CLOSED_STATES = frozenset({State.DS13, State.DS90, State.DS91})
ACTIVE_STATES = frozenset(s for s in State if s not in CLOSED_STATES)

_EDGE_LIST = [
    (State.DS00, State.DS01),
    (State.DS00, State.DS90),
    (State.DS00, State.DS91),
    (State.DS01, State.DS02),
    (State.DS01, State.DS90),
    (State.DS02, State.DS03),
    (State.DS02, State.DS13),
    (State.DS02, State.DS90),
    (State.DS03, State.DS04),
    (State.DS03, State.DS05),
    (State.DS03, State.DS90),
    (State.DS04, State.DS05),
    (State.DS04, State.DS03),
    (State.DS04, State.DS13),
    (State.DS04, State.DS04),
    (State.DS04, State.DS90),
    (State.DS05, State.DS04),
    (State.DS05, State.DS06),
    (State.DS05, State.DS07),
    (State.DS05, State.DS03),
    (State.DS05, State.DS13),
    (State.DS05, State.DS90),
    (State.DS06, State.DS07),
    (State.DS06, State.DS05),
    (State.DS06, State.DS13),
    (State.DS06, State.DS06),
    (State.DS06, State.DS90),
    (State.DS07, State.DS08),
    (State.DS07, State.DS05),
    (State.DS07, State.DS13),
    (State.DS07, State.DS90),
    (State.DS08, State.DS09),
    (State.DS08, State.DS05),
    (State.DS08, State.DS13),
    (State.DS09, State.DS10),
    (State.DS09, State.DS07),
    (State.DS09, State.DS05),
    (State.DS09, State.DS13),
    (State.DS09, State.DS09),
    (State.DS09, State.DS90),
    (State.DS10, State.DS11),
    (State.DS10, State.DS09),
    (State.DS10, State.DS90),
    (State.DS11, State.DS12),
    (State.DS11, State.DS13),
    (State.DS11, State.DS91),
    (State.DS11, State.DS90),
    (State.DS12, State.DS13),
    (State.DS12, State.DS05),
    (State.DS12, State.DS90),
]
for _s in ACTIVE_STATES:
    _EDGE_LIST.append((_s, State.DS91))
    _EDGE_LIST.append((_s, State.DS90))

LEGAL_EDGES: frozenset[tuple[State, State]] = frozenset(_EDGE_LIST)
del _EDGE_LIST

# Exits from gate states require apply_gate* authorization in the same call
_GATE_EXIT_EDGES = frozenset(
    {
        (State.DS04, State.DS05),
        (State.DS04, State.DS03),
        (State.DS04, State.DS13),
        (State.DS06, State.DS07),
        (State.DS06, State.DS05),
        (State.DS06, State.DS13),
        (State.DS09, State.DS10),
        (State.DS09, State.DS07),
        (State.DS09, State.DS05),
        (State.DS09, State.DS13),
    }
)


class IllegalTransition(Exception):
    pass


@dataclass(frozen=True)
class SessionEvent:
    event_id: str
    session_id: str
    event_kind: str
    seq: int
    at: str
    payload: Any


@dataclass
class DiscoverySession:
    session_id: str
    state: State = State.DS00
    _events: list[SessionEvent] = field(default_factory=list)
    gate1_required: bool = False
    gate2_required: bool = False
    gate1_cleared: bool = True
    gate2_cleared: bool = True
    seal_set: tuple[str, ...] = ()
    sealed_draft_ids: tuple[str, ...] = ()
    close_reason: str | None = None
    policy_unrecoverable_transport_to_ds91: bool = False
    draft_ok_count: int = 0
    sealed_digests: tuple[str, ...] = ()
    sealed_snapshot_version_ids: tuple[str, ...] = ()
    receipt_refs: tuple[str, ...] = ()
    attested_foreign_seals: tuple[tuple[str, str], ...] = ()
    gate_records: tuple[dict[str, Any], ...] = ()
    scope_binding_version: int = 0
    _event_seq: int = 0
    _frozen: bool = False
    _ir_close_hook: Any = None
    _owner_ref: Any = None  # weakref.ref[DiscoveryOrchestrator]
    _gate_exit_authorized: bool = False

    def bind_owner(self, orch: DiscoveryOrchestrator) -> None:
        self._owner_ref = weakref.ref(orch)

    @property
    def events(self) -> tuple[SessionEvent, ...]:
        return tuple(self._events)

    @property
    def is_closed(self) -> bool:
        return self.state in CLOSED_STATES

    def _append(self, kind: str, payload: dict[str, Any] | None = None, at: str = "") -> SessionEvent:
        if self._frozen and kind not in ("ArchivalReceiptLinked",):
            raise IllegalTransition("session event log frozen")
        self._event_seq += 1
        ev = SessionEvent(
            event_id=f"{self.session_id}:{self._event_seq}",
            session_id=self.session_id,
            event_kind=kind,
            seq=self._event_seq,
            at=at or f"t{self._event_seq}",
            payload=deep_freeze(dict(payload or {})),
        )
        self._events.append(ev)
        return ev

    def _commit(self, orch: DiscoveryOrchestrator, to: State, *, reason: str = "", at: str = "") -> SessionEvent:
        owner = self._owner_ref() if self._owner_ref else None
        if owner is None or orch is not owner:
            raise IllegalTransition("only owning DISCOVERY_ORCHESTRATOR instance may commit FSM transitions")
        if self.is_closed:
            raise IllegalTransition(f"session closed in {self.state.value}; cannot transition")
        edge = (self.state, to)
        if edge not in LEGAL_EDGES:
            self._append("TransitionRejected", {"from": self.state.value, "to": to.value, "reason": reason})
            raise IllegalTransition(f"illegal {self.state.value} → {to.value}")
        if edge in _GATE_EXIT_EDGES and not self._gate_exit_authorized:
            self._append("TransitionRejected", {"reason": "gate exit requires GateRecord decision"})
            raise IllegalTransition("gate-state exit requires apply_gate*")
        self._gate_exit_authorized = False

        if to == State.DS07:
            if self.gate1_required and not self.gate1_cleared:
                self._append("TransitionRejected", {"reason": "gate1_required blocks DS07"})
                raise IllegalTransition("→DS07 forbidden while gate1_required uncleared")
            if self.gate2_required and not self.gate2_cleared and self.state != State.DS06:
                self._append("TransitionRejected", {"reason": "gate2_required blocks DS07"})
                raise IllegalTransition("→DS07 forbidden while gate2_required; use DS06")
        if to == State.DS05 and self.state == State.DS03 and self.gate1_required and not self.gate1_cleared:
            self._append("TransitionRejected", {"reason": "gate1_required forces DS04"})
            raise IllegalTransition("DS03→DS05 forbidden while gate1_required")
        if to == State.DS10 and not self.seal_set:
            self._append("TransitionRejected", {"reason": "empty seal_set"})
            raise IllegalTransition("DS09→DS10 requires nonempty seal_set")
        if to == State.DS09 and self.draft_ok_count < 1 and self.state == State.DS08:
            self._append("TransitionRejected", {"reason": "no DraftCRP"})
            raise IllegalTransition("DS08→DS09 requires ≥1 DraftCRP")
        if to == State.DS11 and self.state == State.DS10:
            if len(self.seal_set) != len(self.sealed_draft_ids):
                self._append("TransitionRejected", {"reason": "incomplete seal wave"})
                raise IllegalTransition("DS10→DS11 requires bijection seal_set ↔ sealed drafts")
            if set(self.seal_set) != set(self.sealed_draft_ids):
                self._append("TransitionRejected", {"reason": "incomplete seal wave"})
                raise IllegalTransition("DS10→DS11 requires bijection seal_set ↔ sealed drafts")

        if to == State.DS91:
            if reason not in DS91_REASONS:
                self._append("TransitionRejected", {"reason": "DS91 reason not allowlisted"})
                raise IllegalTransition(f"DS91 only for allowlisted reasons, not {reason!r}")
            if reason == "store_init_failure" and self.state != State.DS00:
                raise IllegalTransition("store_init_failure only from DS00")
            if reason == "unrecoverable_transport":
                if self.state != State.DS11 or not self.policy_unrecoverable_transport_to_ds91:
                    raise IllegalTransition("unrecoverable_transport requires DS11 + SessionPolicy")

        if to == State.DS13 and reason not in CLOSE_REASONS:
            self._append("TransitionRejected", {"reason": "invalid close_reason"})
            raise IllegalTransition(f"invalid close_reason: {reason!r}")

        frm = self.state
        self.state = to
        if to == State.DS13:
            self.close_reason = reason
            ev = self._append("SessionClosed", {"from": frm.value, "to": to.value, "close_reason": reason}, at=at)
            self._freeze_terminal()
            return ev
        if to == State.DS90:
            self.close_reason = reason or "cancelled"
            ev = self._append(
                "SessionCancelled",
                {"from": frm.value, "to": to.value, "reason": self.close_reason},
                at=at,
            )
            self._freeze_terminal()
            return ev
        if to == State.DS91:
            self.close_reason = reason
            ev = self._append("SessionFailed", {"from": frm.value, "to": to.value, "reason": reason}, at=at)
            self._freeze_terminal()
            return ev
        return self._append(
            "Transition",
            {"from": frm.value, "to": to.value, "reason": reason},
            at=at,
        )

    def _freeze_terminal(self) -> None:
        self._frozen = True
        if self._ir_close_hook:
            self._ir_close_hook()

    def _skip_gate(self, orch: DiscoveryOrchestrator, gate: int) -> SessionEvent:
        owner = self._owner_ref() if self._owner_ref else None
        if owner is None or orch is not owner:
            raise IllegalTransition("orchestrator only")
        if gate == 1:
            if self.gate1_required and not self.gate1_cleared:
                raise IllegalTransition("cannot skip required Gate 1")
            if self.state not in (State.DS03, State.DS05):
                raise IllegalTransition("Gate 1 skip only at DS03/DS05 evaluation")
        if gate == 2:
            if self.gate2_required and not self.gate2_cleared:
                raise IllegalTransition("cannot skip required Gate 2")
            if self.state != State.DS05:
                raise IllegalTransition("Gate 2 skip only at DS05 evaluation")
        return self._append("GateSkipped", {"gate": gate, "reason": "NOT_REQUIRED"})

    def _mint_verifier_prior(
        self,
        orch: DiscoveryOrchestrator,
        export: VerifierFeedbackExport,
        *,
        source_session_id: str | None = None,
        active: bool = True,
        authorized_import: bool = False,
    ) -> dict[str, Any]:
        owner = self._owner_ref() if self._owner_ref else None
        if owner is None or orch is not owner:
            raise IllegalTransition("orchestrator only")
        if active and self.is_closed:
            raise IllegalTransition("no active VerifierPrior into closed session")
        if active and self.state != State.DS12 and not authorized_import:
            raise IllegalTransition("active prior only in DS12 or authorized import")
        if not export.export_digest or not export.content_digest:
            raise ProvenanceError("feedback must be finalized (content_digest + export_digest)")
        validate_feedback_for_prior(export, expected_crp_digest=export.crp_digest)
        src = source_session_id or self.session_id
        known_local = export.sealed_digest in self.sealed_digests or export.crp_digest in self.sealed_digests
        known_foreign = (src, export.sealed_digest) in self.attested_foreign_seals or (
            src,
            export.crp_digest,
        ) in self.attested_foreign_seals
        if src != self.session_id:
            if not known_foreign:
                raise ProvenanceError("cross-session prior requires attested foreign sealed_digest")
        elif authorized_import and not known_local and not known_foreign:
            raise ProvenanceError("authorized import requires attested or local sealed_digest")
        elif not authorized_import and not known_local:
            raise ProvenanceError("export sealed_digest not known to this session")
        if export.receipt_digest is not None and export.receipt_digest not in self.receipt_refs and src == self.session_id:
            raise ProvenanceError("receipt_digest not known to this session")
        if active and not (export.sealed_digest or export.receipt_digest):
            raise ProvenanceError("active prior requires sealed_digest or receipt_ref")
        prior = {
            "session_id": self.session_id,
            "source_session_id": src,
            "sealed_digest": export.sealed_digest,
            "receipt_ref": export.receipt_digest,
            "export_ref": export.export_digest,
            "content_digest": export.content_digest,
            "active": bool(active and not self.is_closed),
        }
        if prior["active"]:
            self._append("FeedbackImported", {"export_ref": export.export_digest, "source_session_id": src})
        else:
            self._append("ArchivalReceiptLinked", {"export_ref": export.export_digest})
        return prior


def replay_control(events: tuple[SessionEvent, ...] | list[SessionEvent]) -> State:
    if not events:
        return State.DS00
    state = State.DS00
    seq = 0
    sid = events[0].session_id
    terminal = False
    for ev in events:
        if terminal and ev.event_kind in ("SessionClosed", "SessionCancelled", "SessionFailed", "Transition"):
            raise IllegalTransition("corrupted_event_history: event after terminal")
        if ev.session_id != sid:
            raise IllegalTransition("corrupted_event_history: mixed session_id")
        if ev.seq != seq + 1:
            raise IllegalTransition("corrupted_event_history: out-of-order seq")
        seq = ev.seq
        if ev.event_kind == "Transition":
            to = State(ev.payload["to"])
            frm = State(ev.payload["from"])
            if frm != state or (state, to) not in LEGAL_EDGES:
                raise IllegalTransition("corrupted_event_history: illegal transition")
            state = to
        elif ev.event_kind == "SessionClosed":
            frm = State(ev.payload["from"])
            if frm != state or (state, State.DS13) not in LEGAL_EDGES:
                raise IllegalTransition("corrupted_event_history: illegal close")
            if ev.payload.get("close_reason") not in CLOSE_REASONS:
                raise IllegalTransition("corrupted_event_history: bad close_reason")
            state = State.DS13
            terminal = True
        elif ev.event_kind == "SessionCancelled":
            frm = State(ev.payload["from"])
            if frm != state or (state, State.DS90) not in LEGAL_EDGES:
                raise IllegalTransition("corrupted_event_history: illegal cancel")
            state = State.DS90
            terminal = True
        elif ev.event_kind == "SessionFailed":
            frm = State(ev.payload["from"])
            reason = ev.payload.get("reason", "")
            if frm != state or (state, State.DS91) not in LEGAL_EDGES:
                raise IllegalTransition("corrupted_event_history: illegal fail")
            if reason not in DS91_REASONS:
                raise IllegalTransition("corrupted_event_history: DS91 reason not allowlisted")
            state = State.DS91
            terminal = True
        elif ev.event_kind == "TransitionRejected":
            continue
        elif ev.event_kind == "SessionOpened":
            if seq != 1:
                raise IllegalTransition("corrupted_event_history: SessionOpened not first")
    return state
