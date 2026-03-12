from datetime import timedelta, datetime, timezone
from jose import jwt
import pytest
from unittest.mock import patch

from app.core.auth import create_access_token, verify_password, get_password_hash


def test_get_password_hash():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True


def test_verify_password_incorrect():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password("wrongpassword", hashed) is False


@patch("app.core.auth.settings")
@patch("app.core.auth.datetime")
def test_create_access_token(mock_datetime, mock_settings):
    # Setup mocks
    mock_settings.SECRET_KEY = "test_secret_key"
    mock_settings.ALGORITHM = "HS256"
    mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    mock_now = datetime.now(timezone.utc)
    mock_datetime.now.return_value = mock_now

    # Run
    subject = "test@example.com"
    token = create_access_token(subject)

    # Verify
    decoded = jwt.decode(
        token, mock_settings.SECRET_KEY, algorithms=[mock_settings.ALGORITHM]
    )
    assert decoded["sub"] == subject

    # Expected expiration is mock_now + 30 minutes
    expected_exp = int((mock_now + timedelta(minutes=30)).timestamp())
    assert decoded["exp"] == expected_exp


@patch("app.core.auth.settings")
@patch("app.core.auth.datetime")
def test_create_access_token_expires_delta(mock_datetime, mock_settings):
    # Setup mocks
    mock_settings.SECRET_KEY = "test_secret_key"
    mock_settings.ALGORITHM = "HS256"

    mock_now = datetime.now(timezone.utc)
    mock_datetime.now.return_value = mock_now

    # Run
    subject = "test2@example.com"
    expires_delta = timedelta(minutes=15)
    token = create_access_token(subject, expires_delta=expires_delta)

    # Verify
    decoded = jwt.decode(
        token, mock_settings.SECRET_KEY, algorithms=[mock_settings.ALGORITHM]
    )
    assert decoded["sub"] == subject

    # Expected expiration is mock_now + 15 minutes
    expected_exp = int((mock_now + timedelta(minutes=15)).timestamp())
    assert decoded["exp"] == expected_exp


def test_verify_password_correct():
    password = "correcthorsebatterystaple"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True


def test_verify_password_invalid_hash():
    password = "testpassword"
    with pytest.raises(ValueError):
        verify_password(password, "")


def test_verify_password_empty_password():
    password = ""
    hashed = get_password_hash("testpassword")
    assert verify_password(password, hashed) is False


def test_verify_password_empty_both():
    with pytest.raises(ValueError):
        verify_password("", "")


def test_get_password_hash_different_salts():
    password = "testpassword"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    assert hash1 != hash2
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


def test_get_password_hash_empty_string():
    password = ""
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True


def test_get_password_hash_long_password():
    # bcrypt has a 72-byte limit
    password = "a" * 72
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True

    # Test that it still works but effectively ignores characters beyond 72
    # passlib/bcrypt might truncate or handle it, but verification should still pass for the 72-char version
    password_73 = "a" * 73
    hashed_73 = get_password_hash(password_73)
    assert verify_password(password_73, hashed_73) is True


def test_get_password_hash_unicode():
    password = "pásswörd_123_🔥"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True


def test_get_password_hash_special_chars():
    password = "!@#$%^&*()_+=-[]{};':\",./<>?`~"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True

def test_verify_password_malformed_hash():
    password = "testpassword"
    with pytest.raises(ValueError):
        verify_password(password, "not_a_valid_hash")

def test_verify_password_none_inputs():
    # Passlib verify returns False or raises TypeError depending on input.
    # verify(None, hash) raises TypeError
    with pytest.raises(TypeError):
        verify_password(None, "$2b$12$jZzaDFhvoDtIVdSHemwb4..TSc6oBJWV9cDZ7BhwpjcAr10hDNw72")

    # verify("pass", None) returns False gracefully
    assert verify_password("testpassword", None) is False

def test_verify_password_long_password_mismatch():
    # bcrypt truncates at 72 bytes. Passwords longer than 72 bytes that share the same first 72 bytes
    # will both verify against the same hash. We need to verify that modifying a character WITHIN
    # the 72 byte limit causes verification to fail.
    password = "a" * 100
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True

    # Modify a character within the 72 byte limit
    different_password = "b" + ("a" * 99)
    assert verify_password(different_password, hashed) is False
