"""Tests for URL extraction from raw message text.

Member 3: Privacy, Cybersecurity and URL Analysis.
"""

from __future__ import annotations

from url_analysis.extractor import extract_urls


def test_extracts_https_url():
    urls = extract_urls("Check this out: https://example.com/page")
    assert "https://example.com/page" in urls


def test_extracts_http_url():
    urls = extract_urls("Visit http://example.com now!")
    assert "http://example.com" in urls or any("example.com" in u for u in urls)


def test_extracts_bare_www_url():
    urls = extract_urls("Go to www.example.com for details.")
    assert any("example.com" in u for u in urls)


def test_extracts_multiple_urls():
    text = "First: https://site1.com and then https://site2.org/path"
    urls = extract_urls(text)
    assert len(urls) == 2


def test_deduplicates_repeated_urls():
    text = "https://example.com https://example.com"
    urls = extract_urls(text)
    assert urls.count("https://example.com") == 1


def test_strips_trailing_punctuation():
    urls = extract_urls("See https://example.com.")
    assert all(not u.endswith(".") for u in urls)


def test_empty_string_returns_empty():
    assert extract_urls("") == []


def test_no_url_in_text_returns_empty():
    assert extract_urls("Hello, how are you today?") == []


def test_ip_based_url_extracted():
    urls = extract_urls("Click http://192.168.1.1/login to proceed.")
    assert any("192.168.1.1" in u for u in urls)


def test_url_with_path_and_query_extracted():
    urls = extract_urls("https://bank-secure.xyz/verify?token=abc123")
    assert any("bank-secure.xyz" in u for u in urls)
