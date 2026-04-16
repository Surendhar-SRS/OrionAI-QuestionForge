import pytest
from importlib import reload

from app.core import config


def test_settings_defaults(monkeypatch):
    # Ensure no environment variables interfere
    monkeypatch.delenv("TOKEN_URL", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    monkeypatch.delenv("BACKEND_CORS_ORIGINS", raising=False)

    # Reload config to evaluate defaults
    reload(config)

    # When reloading config, the settings instance is created at module level.
    # We can check config.settings directly or create a new instance.
    settings = config.Settings()

    assert settings.PROJECT_NAME == "Question Bank Generator"
    assert settings.TOKEN_URL == "api/auth/login"
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert settings.DATABASE_URL == "sqlite+aiosqlite:///:memory:"
    # SECRET_KEY should be auto-generated
    assert settings.SECRET_KEY is not None
    assert len(settings.SECRET_KEY) > 0


def test_settings_missing_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    # The config module instantiation will fail at the module level
    # due to config.settings = Settings() being called on load
    with pytest.raises(
        ValueError, match="DATABASE_URL environment variable must be set"
    ):
        reload(config)


def test_settings_custom_values(monkeypatch):
    monkeypatch.setenv("TOKEN_URL", "custom/token/url")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/db")
    monkeypatch.setenv("SECRET_KEY", "supersecretkey")

    reload(config)
    settings = config.Settings()

    assert settings.TOKEN_URL == "custom/token/url"
    assert settings.DATABASE_URL == "postgresql://user:pass@localhost/db"
    assert settings.SECRET_KEY == "supersecretkey"
