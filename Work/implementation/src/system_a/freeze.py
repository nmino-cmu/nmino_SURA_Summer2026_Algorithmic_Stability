"""Deep-freeze / thaw helpers for append-only IR/event payloads."""

from __future__ import annotations

from copy import deepcopy
from types import MappingProxyType
from typing import Any


def deep_freeze(obj: Any) -> Any:
    """Always copy then freeze; never return a live proxy as-is."""
    if isinstance(obj, MappingProxyType):
        return deep_freeze(dict(obj))
    if isinstance(obj, dict):
        return MappingProxyType({k: deep_freeze(v) for k, v in deepcopy(obj).items()})
    if isinstance(obj, (list, tuple)):
        return tuple(deep_freeze(x) for x in deepcopy(list(obj)))
    if isinstance(obj, set):
        return frozenset(deep_freeze(x) for x in obj)
    return obj


def deep_thaw(obj: Any) -> Any:
    """Plain JSON-friendly structure for wire serialization."""
    if isinstance(obj, MappingProxyType):
        return {k: deep_thaw(v) for k, v in obj.items()}
    if isinstance(obj, dict):
        return {k: deep_thaw(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [deep_thaw(x) for x in obj]
    if isinstance(obj, frozenset):
        return [deep_thaw(x) for x in obj]
    return obj
