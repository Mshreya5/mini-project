"""Member 3: URL Analysis and Privacy Module.

Provides:
- URL extraction from raw message text (`url_analysis.extractor`)
- Structural/lexical URL risk indicator detection (`url_analysis.analyzer`)
- Privacy gate and message sanitization (`url_analysis.privacy`)
- Pydantic request/response schemas (`url_analysis.models`)
"""

from url_analysis.extractor import extract_urls
from url_analysis.analyzer import analyze_url, AnalysisResult
from url_analysis.models import AnalyzeRequest, AnalyzeResponse, PrivacyInfoResponse

__all__ = [
    "extract_urls",
    "analyze_url",
    "AnalysisResult",
    "AnalyzeRequest",
    "AnalyzeResponse",
    "PrivacyInfoResponse",
]
