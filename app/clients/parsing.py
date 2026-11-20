"""Tolerant helpers for reading upstream JSON.

The collaborating modules are built by other team members and their field names
may drift. These helpers accept a documented set of aliases and nested wrappers
so a small naming change does not break integration, while still failing loudly
when the payload genuinely cannot be understood.
"""

from __future__ import annotations

from typing import Any, Iterator, Mapping

_WRAPPER_KEYS = ("data", "result", "analysis", "response", "payload")


def candidate_dicts(payload: Mapping[str, Any]) -> Iterator[Mapping[str, Any]]:
    """Yield the payload and any single-level wrapper objects inside it."""
    yield payload
    for key in _WRAPPER_KEYS:
        nested = payload.get(key)
        if isinstance(nested, Mapping):
            yield nested


def first_present(payload: Mapping[str, Any], keys: tuple[str, ...]) -> Any | None:
    """Return the first non-empty value found under any of ``keys``."""
    for candidate in candidate_dicts(payload):
        lowered = {str(key).lower(): value for key, value in candidate.items()}
        for key in keys:
            value = lowered.get(key.lower())
            if value is None:
                continue
            if isinstance(value, str) and not value.strip():
                continue
            if isinstance(value, (list, tuple, dict)) and len(value) == 0:
                continue
            return value
    return None


def normalise_token(value: Any) -> str | None:
    """Lowercase a keyword/flag into the snake_case form used by the rule set."""
    if not isinstance(value, str):
        return None
    token = value.strip().lower()
    for separator in (" ", "-", "/"):
        token = token.replace(separator, "_")
    token = "_".join(part for part in token.split("_") if part)
    return token or None


def as_text_list(value: Any) -> tuple[str, ...]:
    """Normalise a list of strings or objects into lowercased tokens."""
    if value is None:
        return ()

    items = [value] if isinstance(value, (str, Mapping)) else list(value)
    tokens: list[str] = []
    for item in items:
        raw: Any = item
        if isinstance(item, Mapping):
            raw = first_present(
                item,
                ("name", "token", "id", "label", "code", "type", "signal", "reason"),
            )
        token = normalise_token(raw)
        if token and token not in tokens:
            tokens.append(token)
    return tuple(tokens)


def as_confidence(value: Any) -> float | None:
    """Coerce a confidence to 0..1, accepting percentages and numeric strings."""
    if value is None or isinstance(value, bool):
        return None
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return None

    if confidence > 1.0:
        confidence = confidence / 100.0 if confidence <= 100.0 else 1.0
    return max(0.0, min(1.0, round(confidence, 4)))


def as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "yes", "1"):
            return True
        if lowered in ("false", "no", "0"):
            return False
    return None
