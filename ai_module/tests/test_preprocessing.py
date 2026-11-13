import pytest
from ai_module.src.preprocessing import build_pipeline, create_tfidf_vectorizer, normalize_text


def test_normalize_text_whitespace_and_newlines():
    raw = "   URGENT:   Please \n\n  pay \t now!   "
    cleaned = normalize_text(raw)
    assert cleaned == "URGENT: Please pay now!"


def test_normalize_text_none_and_empty():
    assert normalize_text(None) == ""
    assert normalize_text("") == ""
    assert normalize_text("   ") == ""


def test_normalize_text_unicode_normalization():
    fancy_text = "ＵＲＧＥＮＴ ｃａｌｌ"
    cleaned = normalize_text(fancy_text)
    assert cleaned == "URGENT call"


def test_create_tfidf_vectorizer_config():
    vec = create_tfidf_vectorizer()
    assert vec.ngram_range == (1, 2)
    assert vec.sublinear_tf is True
    assert vec.min_df == 2
    assert vec.lowercase is True


def test_vectorizer_transform_pipeline():
    corpus = [
        "Congratulations! You won a cash prize of 1000 dollars.",
        "Your bank account has been suspended urgently.",
        "Are we still meeting for lunch tomorrow at noon?",
        "Please confirm your OTP code immediately.",
        "You have won a prize reward claim it now.",
        "Your account has been suspended please verify urgently.",
    ]
    vec = create_tfidf_vectorizer()
    X = vec.fit_transform(corpus)
    assert X.shape[0] == 6
    assert X.shape[1] > 0
    vocab = vec.get_feature_names_out()
    assert any("prize" in word for word in vocab)
