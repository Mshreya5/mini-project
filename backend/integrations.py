"""
Integration Client for External Microservices
Member 4: Risk Aggregation, Warning Logic and System Integration

Handles communication with Member 2 (ML Scam API) and Member 3 (URL Analysis API).
Includes robust timeout handling, connection retries, and graceful degradation.
"""
import re
import logging
from typing import Tuple, List
import requests
from backend.config import settings
from backend.schemas import (
    Member2MLResponse,
    Member3URLResponse,
    MessagePrediction,
    URLRiskLevel
)

logger = logging.getLogger("silvershield.integrations")

# Standard regex to detect presence of URLs
URL_PATTERN = re.compile(
    r"(?:https?:\/\/|ftp:\/\/|www\.)[^\s/$.?#].[^\s]*",
    re.IGNORECASE
)


class IntegrationClient:
    """
    Robust HTTP client interfacing with Member 2 and Member 3 APIs.
    """

    def __init__(self, timeout: float = None):
        self.timeout = timeout or settings.REQUEST_TIMEOUT_SECONDS
        self.ml_url = settings.MEMBER2_ML_API_URL
        self.url_analysis_url = settings.MEMBER3_URL_API_URL

    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """Extracts any URLs found within raw message string."""
        return URL_PATTERN.findall(text)

    def call_member2_ml(self, message: str) -> Tuple[Member2MLResponse, bool]:
        """
        Calls Member 2 ML scam classification API.
        Returns (Member2MLResponse, is_available: bool).
        """
        payload = {"text": message}
        try:
            response = requests.post(
                self.ml_url,
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                parsed = Member2MLResponse(
                    prediction=data.get("prediction", MessagePrediction.SUSPICIOUS.value),
                    confidence=float(data.get("confidence", 0.5)),
                    detected_triggers=data.get("detected_triggers", [])
                )
                return parsed, True
            else:
                logger.warning(f"Member 2 returned HTTP {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            logger.warning(f"Member 2 ML API timed out after {self.timeout}s")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Member 2 ML API connection error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error calling Member 2 ML API: {e}")

        # Graceful degradation fallback
        fallback = Member2MLResponse(
            prediction=MessagePrediction.UNVERIFIED,
            confidence=0.5,
            detected_triggers=["ML Scam Classification Service Offline (Safe Fallback Active)"]
        )
        return fallback, False

    def call_member3_url(self, message: str) -> Tuple[Member3URLResponse, bool]:
        """
        Calls Member 3 URL Security & Privacy Analysis API.
        Returns (Member3URLResponse, is_available: bool).
        """
        extracted = self.extract_urls(message)

        # If no URLs exist in message, do not waste network call
        if not extracted:
            return Member3URLResponse(
                urls_found=[],
                url_risk=URLRiskLevel.NO_URL,
                indicators=[],
                privacy_redacted=True
            ), True

        payload = {
            "text": message,
            "urls": extracted,
            "anonymize_pii": True
        }

        try:
            response = requests.post(
                self.url_analysis_url,
                json=payload,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                parsed = Member3URLResponse(
                    urls_found=data.get("urls_found", extracted),
                    url_risk=data.get("url_risk", URLRiskLevel.SUSPICIOUS.value),
                    indicators=data.get("indicators", []),
                    privacy_redacted=data.get("privacy_redacted", True)
                )
                return parsed, True
            else:
                logger.warning(f"Member 3 returned HTTP {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            logger.warning(f"Member 3 URL API timed out after {self.timeout}s")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Member 3 URL API connection error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error calling Member 3 URL API: {e}")

        # Graceful degradation fallback: URLs were present, but service failed to inspect
        fallback = Member3URLResponse(
            urls_found=extracted,
            url_risk=URLRiskLevel.UNVERIFIED,
            indicators=["URL Security Inspection Service Offline (Link Present but Unverified)"],
            privacy_redacted=True
        )
        return fallback, False
