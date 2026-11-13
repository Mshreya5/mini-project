"""Tests for URL risk indicator analysis.

Member 3: Privacy, Cybersecurity and URL Analysis.
"""

from __future__ import annotations

from url_analysis.analyzer import analyze_url


def test_clean_url_not_suspicious():
    # bbc.co.uk is a legitimate multi-label ccTLD — one subdomain indicator may fire
    # but it must NOT be marked suspicious (requires >= 2 indicators)
    result = analyze_url("https://www.bbc.co.uk/news")
    assert result.suspicious is False


def test_ip_based_url_flagged():
    result = analyze_url("http://192.168.1.1/login")
    assert any("IP address" in ind for ind in result.risk_indicators)


def test_url_shortener_flagged():
    result = analyze_url("https://bit.ly/3xYzAbc")
    assert any("shortener" in ind.lower() for ind in result.risk_indicators)


def test_suspicious_tld_flagged():
    result = analyze_url("https://free-prize.xyz/claim")
    assert any(".xyz" in ind for ind in result.risk_indicators)


def test_brand_impersonation_flagged():
    result = analyze_url("https://paypal-secure-login.com/verify")
    assert any("paypal" in ind.lower() for ind in result.risk_indicators)


def test_excessive_subdomains_flagged():
    result = analyze_url("https://a.b.c.d.example.com/page")
    assert any("subdomain" in ind.lower() for ind in result.risk_indicators)


def test_suspicious_path_keywords_flagged():
    result = analyze_url("https://example.com/account/verify")
    assert any("path" in ind.lower() for ind in result.risk_indicators)


def test_long_url_flagged():
    long_url = "https://example.com/" + "a" * 200
    result = analyze_url(long_url)
    assert any("long" in ind.lower() for ind in result.risk_indicators)


def test_at_symbol_in_url_flagged():
    result = analyze_url("https://legitimate.com@evil.com/path")
    assert any("@" in ind for ind in result.risk_indicators)


def test_single_indicator_not_suspicious():
    """One indicator alone must NOT set suspicious=True."""
    result = analyze_url("https://bit.ly/abc")
    # shortener is 1 indicator — not enough
    assert result.risk_score >= 1
    assert result.suspicious is False


def test_two_indicators_marks_suspicious():
    """Two or more indicators must set suspicious=True."""
    # IP + suspicious path = 2 indicators
    result = analyze_url("http://192.168.1.1/login/verify")
    assert result.suspicious is True
    assert result.risk_score >= 2


def test_query_string_stripped_from_output():
    """Query strings must not appear in the returned URL for privacy."""
    result = analyze_url("https://example.com/page?token=secret123&user=alice")
    assert "token=secret123" not in result.url
    assert "user=alice" not in result.url


def test_explanation_present():
    result = analyze_url("https://example.com")
    assert isinstance(result.explanation, str)
    assert len(result.explanation) > 10
