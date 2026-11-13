"""HTTP adapters for the collaborating modules.

Member 2 owns scam classification, Member 3 owns URL analysis. This package
contains only transport and response normalisation - no model and no URL
reputation logic is duplicated here.
"""

from app.clients.base import JsonApiClient
from app.clients.scam_detector import ScamDetectorClient
from app.clients.url_analyzer import UrlAnalyzerClient

__all__ = ["JsonApiClient", "ScamDetectorClient", "UrlAnalyzerClient"]
