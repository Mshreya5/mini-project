import re
import unicodedata
from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

from ai_module.src.config import (
    TFIDF_MAX_FEATURES,
    TFIDF_MIN_DF,
    TFIDF_NGRAM_RANGE,
    TFIDF_SUBLINEAR_TF,
)


def normalize_text(text: Optional[str]) -> str:
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    normalized = unicodedata.normalize("NFKC", text)

    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", " ", normalized)

    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def create_tfidf_vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        ngram_range=TFIDF_NGRAM_RANGE,
        max_features=TFIDF_MAX_FEATURES,
        sublinear_tf=TFIDF_SUBLINEAR_TF,
        min_df=TFIDF_MIN_DF,
        strip_accents="unicode",
        lowercase=True,
    )


def build_pipeline(classifier) -> Pipeline:
    vectorizer = create_tfidf_vectorizer()
    return Pipeline(
        steps=[
            ("tfidf", vectorizer),
            ("classifier", classifier),
        ]
    )
