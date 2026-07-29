"""ART-21b canonicalization and digests (ART-INT I-INT-40)."""

from __future__ import annotations

import hashlib
import json
import unicodedata
from typing import Any

CANON_VERSION = "ART21b.CANON.v1"
BOT_TOKEN = "⊥"  # allowed typed absence token where schemas permit


def normalize_unicode(s: str) -> str:
    """NFC normalization for interface math/text strings (I-INT-40)."""
    return unicodedata.normalize("NFC", s)


def _prepare(obj: Any) -> Any:
    if obj is None:
        raise ValueError("null values forbidden in normative fields; omit key or use ⊥")
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, int) and not isinstance(obj, bool):
        return obj
    if isinstance(obj, float):
        raise ValueError("floats forbidden in normative fields")
    if isinstance(obj, str):
        return normalize_unicode(obj)
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k in sorted(obj.keys(), key=lambda x: x.encode("utf-8")):
            v = obj[k]
            if v is None:
                continue  # omit-absent
            out[k] = _prepare(v)
        return out
    if isinstance(obj, (list, tuple)):
        return [_prepare(x) for x in obj]
    raise TypeError(f"unsupported type for canonicalization: {type(obj)!r}")


def canonical_serialization(obj: Any) -> bytes:
    """I-CAN-01: UTF-8 compact JSON, sorted keys, omit nulls."""
    prepared = _prepare(obj)
    return json.dumps(prepared, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )


def H(data: bytes) -> str:
    """I-H-01: SHA-256 hex lowercase."""
    return hashlib.sha256(data).hexdigest()


def H_tagged(*args: Any) -> str:
    """I-H-03: H(canonical_serialization([a0,…,an]))."""
    return H(canonical_serialization(list(args)))


def digest_object(obj: Any) -> str:
    """I-CAN-02 top-level object digest with canon version domain tag."""
    body = canonical_serialization(obj)
    return H(CANON_VERSION.encode("utf-8") + b"\x00" + body)
