from datetime import timedelta, datetime, timezone
from jose import jwt
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
