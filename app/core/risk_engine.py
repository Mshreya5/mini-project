"""The risk aggregation engine.

Design decisions worth knowing when reading this file:

1. Module confidences are never added together. A confidence of 0.9 from the ML
   module and a score of 0.9 from the URL module mean different things and are
   not comparable, so each module output is first reduced to named indicators.
2. Every indicator carries a fixed severity from the rule set. The engine sums
   severity points, never raw model scores.
3. Deterministic override rules run first and can lift the level on their own,
   which guarantees that a high-confidence scam verdict or a malicious link is
   never diluted by a clean result from the other module.
4. Per-module caps stop one module from dominating the total on its own.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.models import (
    Assessment,
    Contribution,
    Indicator,
    PREDICTION_SCAM,
    URL_MALICIOUS,
)
from app.settings import RiskConfig

LEVEL_ORDER: dict[str, int] = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}


def highest_level(*levels: str | None) -> str:
    """Return the most severe of the given levels."""
    candidates = [level for level in levels if level]
    if not candidates:
        return "LOW"
    return max(candidates, key=lambda level: LEVEL_ORDER.get(level, 0))


@dataclass(frozen=True)
class OverrideContext:
    """Everything an override rule is allowed to look at."""

    prediction: str
    confidence: float | None
    url_level: str | None
    has_link: bool


class RiskEngine:
    """Turns indicators plus an override context into one risk level."""

    def __init__(self, config: RiskConfig) -> None:
        self._config = config

    def assess(
        self,
        indicators: list[Indicator],
        *,
        prediction: str,
        confidence: float | None,
        url_level: str | None,
        has_link: bool,
        floor: str | None = None,
        degraded: bool = False,
    ) -> Assessment:
        context = OverrideContext(
            prediction=prediction,
            confidence=confidence,
            url_level=url_level,
            has_link=has_link,
        )

        collected = list(indicators)
        overrides = self._apply_overrides(context, collected)
        level = highest_level(overrides["level"])

        contributions, score, raw_score, capped = self._score(collected)
        scored_level = self._level_for_score(score)
        level = highest_level(level, scored_level)

        if floor is not None:
            level = highest_level(level, floor)

        reasons = list(overrides["reasons"])
        if not overrides["level"]:
            reasons.append(
                f"Indicator points reached {score}, which maps to {scored_level} "
                f"at the configured thresholds."
            )
        if floor is not None and LEVEL_ORDER.get(floor, 0) > LEVEL_ORDER.get(scored_level or "LOW", 0):
            reasons.append(
                f"A required module did not answer, so the level was raised to "
                f"{level}. An unfinished check is never reported as safe."
            )

        return Assessment(
            level=level,
            score=score,
            raw_score=raw_score,
            indicators=collected,
            contributions=contributions,
            overrides=overrides["ids"],
            reasons=reasons,
            capped_sources=capped,
            degraded=degraded,
        )

    def _apply_overrides(
        self, context: OverrideContext, indicators: list[Indicator]
    ) -> dict[str, object]:
        """Evaluate deterministic rules and register their indicators."""
        matched_level: str | None = None
        matched_ids: list[str] = []
        reasons: list[str] = []

        for rule in self._config.overrides:
            indicator_ids = {indicator.id for indicator in indicators}
            if not self._matches(rule.when, context, indicator_ids):
                continue

            matched_level = highest_level(matched_level, rule.level)
            matched_ids.append(rule.id)
            reasons.append(f"{rule.id}: {rule.reason}")

            if rule.indicator not in indicator_ids:
                indicator = self._config.resolve(rule.indicator)
                if indicator is not None:
                    indicators.append(indicator)

        return {"level": matched_level, "ids": matched_ids, "reasons": reasons}

    def _matches(
        self, when: dict[str, object], context: OverrideContext, indicator_ids: set[str]
    ) -> bool:
        for key, expected in when.items():
            if key == "prediction_in":
                if context.prediction not in expected:  # type: ignore[operator]
                    return False
            elif key == "confidence_gte":
                if context.confidence is None or context.confidence < float(expected):  # type: ignore[arg-type]
                    return False
            elif key == "url_risk_in":
                if context.url_level not in expected:  # type: ignore[operator]
                    return False
            elif key == "has_link":
                if bool(context.has_link) is not bool(expected):
                    return False
            elif key == "indicators_all":
                if not set(expected).issubset(indicator_ids):  # type: ignore[arg-type]
                    return False
            elif key == "indicators_any":
                if not set(expected).intersection(indicator_ids):  # type: ignore[arg-type]
                    return False
            else:  # pragma: no cover - guarded by config validation
                raise ValueError(f"Unsupported override condition: {key}")
        return True

    def _score(
        self, indicators: list[Indicator]
    ) -> tuple[list[Contribution], int, int, list[str]]:
        """Sum severity points with a per-source cap."""
        remaining = {
            source: cap for source, cap in self._config.module_caps.items()
        }
        contributions: list[Contribution] = []
        score = 0
        raw_score = 0
        capped_sources: list[str] = []

        for indicator in indicators:
            if indicator.decisive:
                continue

            points = self._config.severity_points.get(indicator.severity, 0)
            raw_score += points

            source = indicator.source
            if source in remaining:
                applied = min(points, max(remaining[source], 0))
                remaining[source] -= applied
                if applied < points and source not in capped_sources:
                    capped_sources.append(source)
            else:
                applied = points

            score += applied
            contributions.append(
                Contribution(
                    indicator_id=indicator.id,
                    label=indicator.label,
                    source=source,
                    severity=indicator.severity,
                    points=points,
                    applied_points=applied,
                )
            )

        return contributions, score, raw_score, capped_sources

    def _level_for_score(self, score: int) -> str:
        thresholds = self._config.thresholds
        if score >= thresholds["high"]:
            return "HIGH"
        if score >= thresholds["medium"]:
            return "MEDIUM"
        return "LOW"


def is_decisive_scam(context: OverrideContext) -> bool:
    """Small helper used by tests and tooling to explain a decision."""
    return context.prediction == PREDICTION_SCAM and context.url_level == URL_MALICIOUS
