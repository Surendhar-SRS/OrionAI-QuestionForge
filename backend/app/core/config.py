import os
import secrets
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    import logging
    logging.warning("python-dotenv not installed, environment variables from .env will not be loaded.")

class Settings:
    PROJECT_NAME: str = "Question Bank Generator"
    BACKEND_CORS_ORIGINS: list[str] = [origin.strip() for origin in os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:5173,http://localhost:5176,http://localhost:8000").split(",") if origin.strip()]
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/qgen")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        # In production, this should be set in environment variables.
        # Generating a random one for development safety.
        SECRET_KEY = secrets.token_urlsafe(32)

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

settings = Settings()
