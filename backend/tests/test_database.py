from unittest.mock import patch, MagicMock
import importlib


def test_database_engine_creation():
    with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_create_engine:
        import app.core.database

        # Reset the mock before reloading because it was already imported during test discovery
        mock_create_engine.reset_mock()
        importlib.reload(app.core.database)

        from app.core.config import settings

        mock_create_engine.assert_called_once_with(
            settings.DATABASE_URL, echo=True, future=True
        )


def test_database_engine_properties():
    with patch("sqlalchemy.ext.asyncio.create_async_engine") as mock_create_engine:
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        import app.core.database

        importlib.reload(app.core.database)

        from app.core.database import engine

        assert engine == mock_engine
