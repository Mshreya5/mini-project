"""Unit tests for URL discovery and normalisation."""

from __future__ import annotations

import pytest

from app.core.urls import extract_first_url, extract_urls, normalise_url, redact_url


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Pay here: https://bank-verify.xyz/login now", "https://bank-verify.xyz/login"),
        ("visit www.example.com today", "www.example.com"),
        ("click on secure-bank.com/pay", "secure-bank.com/pay"),
        ("no link at all here", None),
        ("", None),
    ],
)
def test_extract_first_url(text, expected) -> None:
    assert extract_first_url(text) == expected


def test_extract_urls_deduplicates() -> None:
    text = "See https://a.com and again https://a.com plus https://b.com"
    assert extract_urls(text) == ["https://a.com", "https://b.com"]


def test_extract_urls_strips_trailing_punctuation() -> None:
    assert extract_urls("Go to https://example.com/page.") == ["https://example.com/page"]


def test_normalise_url_adds_scheme() -> None:
    assert normalise_url("example.com/x") == "https://example.com/x"


def test_normalise_url_rejects_unsupported_schemes() -> None:
    assert normalise_url("javascript:alert(1)") is None
    assert normalise_url("ftp://example.com/file") is None
    assert normalise_url("") is None


def test_redact_url_keeps_host_and_drops_query() -> None:
    assert redact_url("https://a.bank.com/pay?token=secret") == "https://a.bank.com/"
