"""Tests for Argon2id Password Hashing and Verification.

Member 2 (Cybersecurity & Privacy) test suite.
"""

from __future__ import annotations

import pytest
from security.passwords import hash_password, needs_rehash, verify_password


def test_hash_password_uses_argon2id():
    """Verify that generated password hashes use the Argon2id scheme."""
    password = "SeniorSafetySecret2026!"
    hashed = hash_password(password)

    # Argon2id format check: $argon2id$v=19$m=65536,t=2,p=1$...
    assert hashed.startswith("$argon2id$")
    assert "m=65536" in hashed
    assert "t=2" in hashed
    assert "p=1" in hashed


def test_verify_password_correct():
    """Verify that correct password matches Argon2id hash."""
    password = "MySecurePassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    """Verify that incorrect password fails verification."""
    password = "MySecurePassword123"
    hashed = hash_password(password)
    assert verify_password("WrongPassword999", hashed) is False
    assert verify_password("", hashed) is False


def test_hash_password_empty_raises_error():
    """Verify that hashing empty or invalid input raises ValueError."""
    with pytest.raises(ValueError, match="Password cannot be empty"):
        hash_password("")


def test_unique_salts_produce_different_hashes():
    """Verify that identical passwords produce distinct hashes due to random salting."""
    password = "CommonPassword456!"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_needs_rehash_behavior():
    """Verify needs_rehash identifies valid current hashes versus outdated ones."""
    hashed = hash_password("TestPassword123!")
    assert needs_rehash(hashed) is False
    assert needs_rehash("") is True
