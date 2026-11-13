"""Elderly friendly warning and recommended action generation.

Rules of thumb applied here:

* One short sentence per warning, no jargon, no scores, no module names.
* Actions are concrete: what not to do, and what to do instead.
* Actions are derived from the indicators that actually fired, so the guidance
  always matches the reason. A fixed list for every message trains people to
  ignore it.
"""

from __future__ import annotations

from app.core.models import Indicator
from app.settings import RiskConfig


def build_warning(config: RiskConfig, level: str, degraded: bool = False) -> str:
    """Pick the warning text for a level, with an honesty note when degraded."""
    templates = config.degraded_warnings if degraded else config.warnings
    return templates.get(level, templates.get("LOW", ""))


def build_actions(
    config: RiskConfig, level: str, indicators: list[Indicator]
) -> list[str]:
    """Ordered, de-duplicated, human readable safety actions."""
    action_ids: list[str] = list(config.baseline_actions.get(level, []))
    for indicator in indicators:
        action_ids.extend(indicator.actions)

    priority = {action_id: index for index, action_id in enumerate(config.action_priority)}
    ordered: list[str] = []
    for action_id in sorted(
        dict.fromkeys(action_ids), key=lambda value: priority.get(value, len(priority))
    ):
        text = config.actions.get(action_id)
        if text and text not in ordered:
            ordered.append(text)

    return ordered[: config.max_actions]


def describe_indicators(indicators: list[Indicator]) -> list[str]:
    """Plain language labels for the API's ``risk_indicators`` field."""
    labels: list[str] = []
    for indicator in indicators:
        if indicator.label not in labels:
            labels.append(indicator.label)
    return labels
