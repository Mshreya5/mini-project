"""Password Hashing and Verification Module.

Member 2 (Cybersecurity & Privacy) module.
Implements state-of-the-art Argon2id password hashing complying with OWASP guidelines.
Argon2id provides optimal defense against both GPU cracking and side-channel attacks.
"""

from __future__ import annotations

import argon2
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

# Baseline OWASP-recommended parameters:
# time_cost: 2 iterations, memory_cost: 64 MiB (65536 KiB), parallelism: 1 thread
_password_hasher = argon2.PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=1,
    hash_len=32,
    type=argon2.Type.ID,
)


def hash_password(password: str) -> str:
    """Hash a plaintext password using Argon2id with cryptographically random salt.

    Args:
        password: The plain text password to hash.

    Returns:
        str: PHC-formatted Argon2id hash ($argon2id$v=19$m=65536,t=2,p=1$...).

    Raises:
        ValueError: If password is empty or None.
    """
    if not password or not isinstance(password, str):
        raise ValueError("Password cannot be empty or non-string.")
    return _password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against an Argon2id hash in constant time.

    Args:
        plain_password: The plaintext password provided during authentication.
        hashed_password: The stored Argon2id hash string from database.

    Returns:
        bool: True if password matches the hash, False otherwise.
    """
    if not plain_password or not hashed_password:
        return False
    try:
        return _password_hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(hashed_password: str) -> bool:
    """Determine whether a stored password hash requires rehashing due to parameter updates.

    Args:
        hashed_password: Stored Argon2id hash string.

    Returns:
        bool: True if hash parameters do not match current hasher settings.
    """
    if not hashed_password:
        return True
    try:
        return _password_hasher.check_needs_rehash(hashed_password)
    except Exception:
        return True
