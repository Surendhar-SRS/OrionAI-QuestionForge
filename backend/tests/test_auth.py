from datetime import timedelta, datetime, timezone
from jose import jwt
import pytest
from app.core.auth import create_access_token, verify_password, get_password_hash
from app.core.config import settings

def test_get_password_hash():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token():
    subject = "test@example.com"
    token = create_access_token(subject)
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == subject
    assert "exp" in decoded

def test_create_access_token_expires_delta():
    subject = "test2@example.com"
    expires_delta = timedelta(minutes=15)
    token = create_access_token(subject, expires_delta=expires_delta)
    decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert decoded["sub"] == subject
    assert "exp" in decoded

    # Verify expiration is approximately correct (within 10 seconds)
    expected_expire = datetime.now(timezone.utc).replace(tzinfo=None) + expires_delta
    token_expire = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc).replace(tzinfo=None)
    assert abs((token_expire - expected_expire).total_seconds()) < 10

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

def test_get_password_hash_format():
    password = "testpassword"
    hashed = get_password_hash(password)
    # bcrypt hashes typically start with $2b$ or $2a$ or $2y$ and are 60 chars long
    assert hashed.startswith("$2")
    assert len(hashed) == 60

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

def test_get_password_hash_format():
    password = "testpassword"
    hashed = get_password_hash(password)
    # bcrypt hashes typically start with $2b$ or $2a$ or $2y$ and are 60 chars long
    assert hashed.startswith("$2")
    assert len(hashed) == 60
