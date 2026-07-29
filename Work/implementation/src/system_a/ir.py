"""Discovery IR store — append-only versions, frozen ownership, freeze (ART-A-02/A-04)."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4

from art_int.canon import digest_object
from system_a.freeze import deep_freeze
from system_a.ownership import CLASS_OWNER


class OwnershipError(Exception):
    pass


class ImmutableError(Exception):
    pass


@dataclass(frozen=True)
class ArtifactVersion:
    lineage_id: str
    version_id: str
    artifact_class: str
    session_id: str
    owner_module: str
    created_at: str
    parents: tuple[str, ...]
    payload: Any


@dataclass(frozen=True)
class BranchRecord:
    branch_id: str
    tip_pins: tuple[str, ...]
    label: str
    version: int
    abandoned: bool = False


@dataclass(frozen=True)
class DepLinkRecord:
    link_id: str
    from_version_id: str
    to_version_id: str
    link_kind: str


@dataclass(frozen=True)
class LifecycleRecord:
    subject_id: str
    state: str
    artifact_class: str
    seq: int


class DiscoveryIR:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.closed = False
        self._versions: dict[str, ArtifactVersion] = {}
        self._lineages: dict[str, list[str]] = {}
        self._branches: dict[str, BranchRecord] = {}
        self._branch_history: list[BranchRecord] = []
        self._deps: list[DepLinkRecord] = []
        self._lifecycle: list[LifecycleRecord] = []
        self._lifecycle_head: dict[str, str] = {}
        self._conflicts_open: set[frozenset[str]] = set()
        self._life_seq = 0

    @property
    def versions(self) -> Mapping[str, ArtifactVersion]:
        return MappingProxyType(self._versions)

    @property
    def branches(self) -> Mapping[str, BranchRecord]:
        return MappingProxyType(self._branches)

    @property
    def deps(self) -> tuple[DepLinkRecord, ...]:
        return tuple(self._deps)

    @property
    def lifecycle(self) -> tuple[LifecycleRecord, ...]:
        return tuple(self._lifecycle)

    def lifecycle_state(self, version_id: str) -> str:
        return self._lifecycle_head.get(version_id, "ACTIVE")

    def mint(
        self,
        *,
        artifact_class: str,
        caller_module: str,
        payload: dict[str, Any],
        lineage_id: str | None = None,
        parents: list[str] | None = None,
        created_at: str = "",
        owner_module: str | None = None,
    ) -> ArtifactVersion:
        if self.closed:
            raise ImmutableError("IR closed; no mint")
        if artifact_class not in CLASS_OWNER:
            raise OwnershipError(f"unknown artifact class: {artifact_class}")
        expected = CLASS_OWNER[artifact_class]
        if owner_module is not None and owner_module != expected:
            raise OwnershipError(f"{artifact_class} owner must be {expected}, not {owner_module}")
        if expected == "DISCOVERY_IR":
            if caller_module not in ("DISCOVERY_IR", "DISCOVERY_ORCHESTRATOR"):
                raise OwnershipError(f"{caller_module} cannot mint {artifact_class}")
        elif caller_module != expected:
            raise OwnershipError(f"{caller_module} cannot mint {artifact_class} owned by {expected}")

        lid = lineage_id or str(uuid4())
        raw = deepcopy(payload)
        frozen_payload = deep_freeze(raw)
        body = {
            "lineage_id": lid,
            "artifact_class": artifact_class,
            "session_id": self.session_id,
            "owner_module": expected,
            "parents": parents or [],
            "payload": deepcopy(payload),
        }
        vid = digest_object(body)
        if vid in self._versions:
            return self._versions[vid]
        av = ArtifactVersion(
            lineage_id=lid,
            version_id=vid,
            artifact_class=artifact_class,
            session_id=self.session_id,
            owner_module=expected,
            created_at=created_at or "t0",
            parents=tuple(parents or []),
            payload=frozen_payload,
        )
        self._versions[vid] = av
        self._lineages.setdefault(lid, []).append(vid)
        self._life_seq += 1
        self._lifecycle.append(LifecycleRecord(vid, "ACTIVE", artifact_class, self._life_seq))
        self._lifecycle_head[vid] = "ACTIVE"
        return av

    def get(self, version_id: str) -> ArtifactVersion:
        return self._versions[version_id]

    def mutate_payload(self, version_id: str, new_payload: dict[str, Any]) -> None:
        raise ImmutableError("version payloads are immutable; mint a new version")

    def abandon(self, version_id: str) -> None:
        if self.closed:
            raise ImmutableError("IR closed")
        cls = self._versions[version_id].artifact_class
        self._life_seq += 1
        self._lifecycle.append(LifecycleRecord(version_id, "ABANDONED", cls, self._life_seq))
        self._lifecycle_head[version_id] = "ABANDONED"

    def add_dep(self, from_version_id: str, to_version_id: str, link_kind: str) -> DepLinkRecord:
        if self.closed:
            raise ImmutableError("IR closed")
        if from_version_id not in self._versions or to_version_id not in self._versions:
            raise ImmutableError("dep endpoints must exist")
        link = DepLinkRecord(str(uuid4()), from_version_id, to_version_id, link_kind)
        self._deps.append(link)
        return link

    def open_conflict(self, a: str, b: str) -> None:
        if self.closed:
            raise ImmutableError("IR closed")
        self._conflicts_open.add(frozenset({a, b}))

    def upsert_branch(
        self, branch_id: str, tip_pins: list[str], label: str = "", *, abandoned: bool = False
    ) -> BranchRecord:
        if self.closed:
            raise ImmutableError("IR closed")
        ver = 0
        if branch_id in self._branches:
            ver = self._branches[branch_id].version + 1
        rec = BranchRecord(branch_id, tuple(tip_pins), label, ver, abandoned=abandoned)
        self._branches[branch_id] = rec
        self._branch_history.append(rec)
        return rec

    def close(self) -> None:
        self.closed = True
