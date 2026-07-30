"""DraftCRP / CompileError payloads (S-INT-DRAFT)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from art_int.crp import CrpPayload, normalize_profile_hint
from art_int.enums import CrpProfile
from art_int.errors import SchemaVersionError

SCHEMA_DRAFT = "ARTINT.DRAFT.v1"


@dataclass
class DraftCRPPayload:
    branch_id: str
    profile_hint: str
    math_scope_pin_digest: str
    tip_pins: list[str]
    dep_closure_digest: str
    payload: CrpPayload
    compile_ok: bool = True
    member_id: str | None = None
    missing_required: list[str] = field(default_factory=list)
    prior_draft_version_id: str | None = None
    created_at: str = ""
    schema_version: str = SCHEMA_DRAFT

    def normalized_profile(self) -> CrpProfile:
        return normalize_profile_hint(self.profile_hint)

    def to_wire(self) -> dict[str, Any]:
        d = asdict(self)
        d["payload"] = self.payload.to_wire()
        for k in ("member_id", "prior_draft_version_id"):
            if d.get(k) is None:
                d.pop(k, None)
        if not d.get("missing_required"):
            d.pop("missing_required", None)
        return d

    def validate_schema(self) -> None:
        if self.schema_version != SCHEMA_DRAFT:
            raise SchemaVersionError(f"unsupported draft schema: {self.schema_version}")
        self.normalized_profile()


@dataclass
class CompileErrorPayload:
    branch_id: str
    error_codes: list[str]
    message: str
    created_at: str = ""
    member_id: str | None = None
    profile_hint: str | None = None
    missing_required: list[str] = field(default_factory=list)
    schema_version: str = SCHEMA_DRAFT

    def to_wire(self) -> dict[str, Any]:
        d = asdict(self)
        for k in ("member_id", "profile_hint"):
            if d.get(k) is None:
                d.pop(k, None)
        if not d.get("missing_required"):
            d.pop("missing_required", None)
        return d
