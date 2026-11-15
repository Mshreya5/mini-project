"""Runtime settings and the loadable risk rule set.

Two kinds of configuration exist on purpose:

* :class:`Settings` - deployment details (where the other modules live, timeouts).
* :class:`RiskConfig` - the assessment policy (weights, caps, thresholds, wording).

Keeping the policy in ``config/risk_config.json`` means the team can tune the
engine during evaluation without touching code, and can show the exact thresholds
to anyone reviewing a decision.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.core.models import Indicator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "risk_config.json"

Severity = Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]

ALLOWED_OVERRIDE_CONDITIONS = frozenset(
    {
        "prediction_in",
        "confidence_gte",
        "url_risk_in",
        "has_link",
        "indicators_all",
        "indicators_any",
    }
)


class IndicatorConfig(BaseModel):
    """Rule-set entry describing one risk indicator."""

    label: str
    severity: Severity
    source: str
    actions: list[str] = Field(default_factory=list)
    decisive: bool = False


class OverrideRule(BaseModel):
    """Deterministic rule that can lift the level regardless of the score."""

    id: str
    level: RiskLevel
    indicator: str
    when: dict[str, Any]
    reason: str


class RiskConfig(BaseModel):
    """The assessment policy."""

    version: str
    severity_points: dict[str, int]
    module_caps: dict[str, int]
    thresholds: dict[str, int]
    scam_confidence: dict[str, float]
    degraded_floor: RiskLevel = "MEDIUM"
    max_actions: int = 4
    indicators: dict[str, IndicatorConfig]
    signal_map: dict[str, str]
    url_flag_map: dict[str, str]
    actions: dict[str, str]
    action_priority: list[str]
    baseline_actions: dict[str, list[str]]
    warnings: dict[str, str]
    degraded_warnings: dict[str, str]
    overrides: list[OverrideRule]

    def resolve(self, indicator_id: str) -> Indicator | None:
        """Build the runtime indicator for a configured id, if it exists."""
        entry = self.indicators.get(indicator_id)
        if entry is None:
            return None
        return Indicator(
            id=indicator_id,
            label=entry.label,
            severity=entry.severity,
            source=entry.source,
            actions=tuple(entry.actions),
            decisive=entry.decisive,
        )

    def unknown_override_conditions(self) -> set[str]:
        """Condition keys used by the rule set that the engine cannot evaluate."""
        used: set[str] = set()
        for rule in self.overrides:
            used.update(rule.when.keys())
        return used - ALLOWED_OVERRIDE_CONDITIONS


class Settings(BaseModel):
    """Deployment configuration, read from environment variables."""

    scam_api_url: str = "http://127.0.0.1:8001/predict"
    url_api_url: str = "http://127.0.0.1:8002/analyze-url"
    request_timeout_seconds: float = Field(default=4.0, gt=0)
    max_retries: int = Field(default=1, ge=0, le=3)
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    @classmethod
    def from_env(cls) -> "Settings":
        origins = os.getenv("CORS_ORIGINS", "*")
        return cls(
            scam_api_url=os.getenv("SCAM_API_URL", cls.model_fields["scam_api_url"].default),
            url_api_url=os.getenv("URL_API_URL", cls.model_fields["url_api_url"].default),
            request_timeout_seconds=float(
                os.getenv("REQUEST_TIMEOUT_SECONDS", "4.0")
            ),
            max_retries=int(os.getenv("MAX_RETRIES", "1")),
            cors_origins=[origin.strip() for origin in origins.split(",") if origin.strip()],
        )


def load_risk_config(path: str | Path | None = None) -> RiskConfig:
    """Read the rule set from disk and fail loudly if it is inconsistent."""
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not config_path.is_file():
        raise FileNotFoundError(f"Risk configuration not found at {config_path}")

    with config_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    config = RiskConfig.model_validate(payload)

    mapped_ids = set(config.signal_map.values()) | set(config.url_flag_map.values())
    missing = {indicator_id for indicator_id in mapped_ids if indicator_id not in config.indicators}
    if missing:
        raise ValueError(f"Rule set maps to unknown indicators: {sorted(missing)}")

    unknown_conditions = config.unknown_override_conditions()
    if unknown_conditions:
        raise ValueError(
            f"Rule set uses override conditions the engine cannot evaluate: "
            f"{sorted(unknown_conditions)}"
        )

    for rule in config.overrides:
        if rule.indicator not in config.indicators:
            raise ValueError(f"Override {rule.id} points at unknown indicator {rule.indicator}")

    unknown_actions = {
        action
        for entry in config.indicators.values()
        for action in entry.actions
        if action not in config.actions
    }
    unknown_actions.update(
        action
        for actions in config.baseline_actions.values()
        for action in actions
        if action not in config.actions
    )
    if unknown_actions:
        raise ValueError(f"Rule set uses undefined action texts: {sorted(unknown_actions)}")

    return config


@lru_cache(maxsize=4)
def get_risk_config(path: str | None = None) -> RiskConfig:
    """Cached loader so the file is parsed once per process."""
    return load_risk_config(os.getenv("RISK_CONFIG_PATH") or path)
