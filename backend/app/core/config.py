import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    import logging

    logging.warning(
        "python-dotenv not installed, environment variables from .env will not be loaded."
    )


class Settings:
    PROJECT_NAME: str = "Question Bank Generator"
    TOKEN_URL: str = os.getenv("TOKEN_URL", "api/auth/login")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable must be set")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set")

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes

    BACKEND_CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "BACKEND_CORS_ORIGINS",
            "http://localhost:5173,http://localhost:5176,http://localhost:8000,http://localhost",
        ).split(",")
        if origin.strip()
    ]

    # LLM Configuration
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")


settings = Settings()
