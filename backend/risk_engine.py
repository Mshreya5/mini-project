"""
Risk Aggregation Engine
Member 4: Risk Aggregation, Warning Logic and System Integration

Combines outputs from Member 2 (ML Scam API) and Member 3 (URL Analysis API)
alongside local heuristic safeguards to calculate a transparent, configurable
overall risk level (LOW, MEDIUM, HIGH) without naive score addition.
"""
import re
from typing import Dict, List, Tuple, Any
from backend.config import settings
from backend.schemas import OverallRiskLevel, MessagePrediction, URLRiskLevel


class RiskAggregationEngine:
    """
    Transparent multi-factor risk assessment engine designed for elderly safety.
    Implements rule-based escalation, weighted scoring, and fail-safe error handling.
    """

    # Critical patterns targeting elderly users
    HEURISTIC_RULES = [
        (
            r"\b(otp|one time password|verification code|security code)\b",
            "Urgent request for OTP or secret verification code",
            0.35,
            "OTP_SOLICITATION"
        ),
        (
            r"\b(password|pin|cvv|netbanking|card number|atm pin)\b",
            "Request for sensitive banking credentials",
            0.35,
            "CREDENTIAL_HARVESTING"
        ),
        (
            r"\b(account blocked|account suspended|deactivated|frozen|pan not updated|kyc expired|electricity will be disconnected)\b",
            "Frightening threat of account blockage or utility disconnection",
            0.30,
            "INTIMIDATION_URGENCY"
        ),
        (
            r"\b(police|cbi|ed|customs|digital arrest|arrest warrant|court notice)\b",
            "Impersonation of law enforcement or digital arrest intimidation",
            0.40,
            "AUTHORITY_IMPERSONATION"
        ),
        (
            r"\b(won|lottery|prize|cashback|bonus|claim reward|crore|lakh)\b",
            "Unsolicited prize or lottery claim reward",
            0.25,
            "PRIZE_LURE"
        ),
        (
            r"\b(anydesk|teamviewer|rustdesk|quicksupport|screen share|install this app|apk)\b",
            "Request to install remote desktop control software or unknown application",
            0.40,
            "REMOTE_ACCESS_RISK"
        ),
        (
            r"\b(send money|transfer now|pay immediately|urgent payment|upi pin)\b",
            "Pressure to send money or complete immediate payment",
            0.30,
            "FINANCIAL_PRESSURE"
        )
    ]

    def __init__(self, custom_settings=None):
        self.settings = custom_settings or settings

    def extract_local_heuristics(self, message: str) -> Tuple[List[str], float, List[str]]:
        """
        Scans message for critical high-danger elderly scam patterns.
        Returns (human_readable_indicators, total_heuristic_score, rule_codes).
        """
        indicators = []
        codes = []
        score = 0.0

        for pattern, description, weight, code in self.HEURISTIC_RULES:
            if re.search(pattern, message, re.IGNORECASE):
                indicators.append(description)
                codes.append(code)
                score += weight

        # Normalize score between 0.0 and 1.0
        normalized_score = min(1.0, score)
        return indicators, normalized_score, codes

    def evaluate_ml_subscore(
        self,
        prediction: str,
        confidence: float,
        is_available: bool
    ) -> float:
        """
        Maps ML prediction and confidence to a normalized risk subscore [0.0 - 1.0].
        """
        if not is_available or prediction == MessagePrediction.UNVERIFIED.value:
            # Fail-safe: service unavailable assumes cautious neutral risk
            return 0.45

        pred_upper = str(prediction).upper()
        if pred_upper == MessagePrediction.SCAM.value:
            # Scaled between 0.65 and 1.0 based on confidence
            return max(0.65, min(1.0, confidence))
        elif pred_upper == MessagePrediction.SUSPICIOUS.value:
            return max(0.40, min(0.70, confidence * 0.7))
        elif pred_upper == MessagePrediction.LEGITIMATE.value:
            # High confidence legitimate yields near-zero risk
            return max(0.0, (1.0 - confidence) * 0.25)
        
        return 0.30

    def evaluate_url_subscore(
        self,
        url_risk: str,
        is_available: bool,
        has_url: bool
    ) -> float:
        """
        Maps URL risk level to a normalized risk subscore [0.0 - 1.0].
        """
        if not has_url or url_risk == URLRiskLevel.NO_URL.value:
            return 0.0

        if not is_available or url_risk == URLRiskLevel.UNVERIFIED.value:
            # If URL was present in text but service failed, fail-safe cautious score
            return 0.60

        risk_upper = str(url_risk).upper()
        if risk_upper == URLRiskLevel.MALICIOUS.value:
            return 1.0
        elif risk_upper == URLRiskLevel.SUSPICIOUS.value:
            return 0.70
        elif risk_upper == URLRiskLevel.SAFE.value:
            return 0.05
        
        return 0.35

    def aggregate_risk(
        self,
        message: str,
        ml_prediction: str,
        ml_confidence: float,
        ml_triggers: List[str],
        ml_available: bool,
        url_risk: str,
        url_indicators: List[str],
        urls_found: List[str],
        url_available: bool
    ) -> Dict[str, Any]:
        """
        Primary aggregation method.
        Synthesizes all signals using multi-factor transparent logic and strict fail-safes.
        """
        # 1. Local heuristic analysis
        local_indicators, heuristic_score, heuristic_codes = self.extract_local_heuristics(message)

        # 2. Compute subscores
        ml_score = self.evaluate_ml_subscore(ml_prediction, ml_confidence, ml_available)
        has_url = len(urls_found) > 0 or url_risk != URLRiskLevel.NO_URL.value
        url_score = self.evaluate_url_subscore(url_risk, url_available, has_url)

        # 3. Dynamic weight adjustment if no URL present
        if not has_url:
            # Reallocate URL weight into ML and Heuristics
            w_ml = self.settings.WEIGHT_ML_SCAM + (self.settings.WEIGHT_URL_RISK * 0.6)
            w_heur = self.settings.WEIGHT_HEURISTIC_TRIGGERS + (self.settings.WEIGHT_URL_RISK * 0.4)
            w_url = 0.0
        else:
            w_ml = self.settings.WEIGHT_ML_SCAM
            w_url = self.settings.WEIGHT_URL_RISK
            w_heur = self.settings.WEIGHT_HEURISTIC_TRIGGERS

        # 4. Multi-factor composite score calculation
        composite_score = (w_ml * ml_score) + (w_url * url_score) + (w_heur * heuristic_score)
        composite_score = max(0.0, min(1.0, round(composite_score, 4)))

        # 5. Compile consolidated risk indicators
        all_indicators: List[str] = []
        for ind in ml_triggers:
            if ind and ind not in all_indicators:
                all_indicators.append(ind)
        for ind in url_indicators:
            if ind and ind not in all_indicators:
                all_indicators.append(ind)
        for ind in local_indicators:
            if ind and ind not in all_indicators:
                all_indicators.append(ind)

        # 6. Service degradation warnings
        if not ml_available:
            all_indicators.append("ML scam classification service was temporarily unavailable / unreachable")
        if not url_available and has_url:
            all_indicators.append("URL security inspection service was temporarily unavailable / unreachable")

        # 7. Escalation Overrides & Classification Logic
        # Rules:
        # HIGH RISK: Multiple strong suspicious indicators OR a high-confidence scam prediction
        # MEDIUM RISK: One or more suspicious indicators detected
        # LOW RISK: No major suspicious indicators detected
        
        is_high_scam_confidence = (
            ml_available
            and ml_prediction == MessagePrediction.SCAM.value
            and ml_confidence >= self.settings.SCAM_CONFIDENCE_HIGH_THRESHOLD
        )
        is_malicious_url = (url_risk == URLRiskLevel.MALICIOUS.value)
        is_suspicious_url_with_triggers = (
            url_risk in [URLRiskLevel.SUSPICIOUS.value, URLRiskLevel.MALICIOUS.value]
            and (len(local_indicators) > 0 or ml_prediction in [MessagePrediction.SCAM.value, MessagePrediction.SUSPICIOUS.value])
        )
        has_critical_credential_theft = (
            "OTP_SOLICITATION" in heuristic_codes or "CREDENTIAL_HARVESTING" in heuristic_codes
        ) and (ml_score >= 0.40 or url_score >= 0.50 or len(local_indicators) >= 2)

        has_multiple_strong_indicators = len(all_indicators) >= 2 and composite_score >= 0.55

        # Determine Overall Risk Level
        if (
            is_high_scam_confidence
            or is_malicious_url
            or is_suspicious_url_with_triggers
            or has_critical_credential_theft
            or has_multiple_strong_indicators
            or composite_score >= self.settings.HIGH_RISK_CUTOFF
        ):
            overall_risk = OverallRiskLevel.HIGH
            # Ensure composite score reflects high tier
            composite_score = max(composite_score, 0.75)

        elif (
            len(all_indicators) >= 1
            or composite_score >= self.settings.MEDIUM_RISK_CUTOFF
            or ml_prediction in [MessagePrediction.SUSPICIOUS.value, MessagePrediction.SCAM.value]
            or url_risk in [URLRiskLevel.SUSPICIOUS.value, URLRiskLevel.UNVERIFIED.value]
            or not ml_available  # Service down must NEVER be automatically LOW risk
            or (not url_available and has_url)
        ):
            overall_risk = OverallRiskLevel.MEDIUM
            composite_score = max(composite_score, 0.40)

        else:
            overall_risk = OverallRiskLevel.LOW
            composite_score = min(composite_score, 0.25)

        return {
            "overall_risk": overall_risk,
            "composite_score": composite_score,
            "risk_indicators": all_indicators,
            "local_heuristics": local_indicators,
            "subscores": {
                "ml_score": ml_score,
                "url_score": url_score,
                "heuristic_score": heuristic_score
            }
        }
