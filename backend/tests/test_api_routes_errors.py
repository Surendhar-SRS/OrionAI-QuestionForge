import pytest
import pytest_asyncio
import httpx
from unittest.mock import patch, AsyncMock, MagicMock

from httpx import AsyncClient

from app.main import app as main_app
from app.api.routes import get_session
from app.api.auth import get_current_user
from app.models import User


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=httpx.ASGITransport(app=main_app, raise_app_exceptions=False),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.mark.asyncio
async def test_ingest_document_rag_service_exception(client):
    test_user = User(
        id=1, email="test@example.com", hashed_password="fake", full_name="Test User"
    )
    main_app.dependency_overrides[get_current_user] = lambda: test_user

    mock_session = AsyncMock()
    mock_course = MagicMock()
    mock_course.id = 1
    mock_course.creator_id = test_user.id
    mock_session.get.return_value = mock_course

    main_app.dependency_overrides[get_session] = lambda: mock_session

    file_content = b"fake pdf content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}
    data = {"course_id": "1"}

    with patch(
        "app.api.routes.rag_service.ingest_document", new_callable=AsyncMock
    ) as mock_ingest:
        mock_ingest.side_effect = Exception("RAG service failed")

        with patch("app.api.routes.os.remove") as mock_remove:
            with patch("app.api.routes.os.path.exists", return_value=True):
                response = await client.post("/api/ingest/", data=data, files=files)
                assert response.status_code == 500

                # Check that os.remove was called because the outer finally block runs
                mock_remove.assert_called_once()
                mock_ingest.assert_called_once()


@pytest.mark.asyncio
async def test_ingest_document_save_file_exception(client):
    test_user = User(
        id=1, email="test@example.com", hashed_password="fake", full_name="Test User"
    )
    main_app.dependency_overrides[get_current_user] = lambda: test_user

    mock_session = AsyncMock()
    mock_course = MagicMock()
    mock_course.id = 1
    mock_course.creator_id = test_user.id
    mock_session.get.return_value = mock_course

    main_app.dependency_overrides[get_session] = lambda: mock_session

    file_content = b"fake pdf content"
    files = {"file": ("test.pdf", file_content, "application/pdf")}
    data = {"course_id": "1"}

    # Mock open inside the thread exception handling
    with patch("builtins.open", side_effect=Exception("Disk full")):
        with patch("app.api.routes.os.remove") as mock_remove:
            with patch("app.api.routes.os.path.exists", return_value=True):
                response = await client.post("/api/ingest/", data=data, files=files)
                assert response.status_code == 500
                # In this case os.remove gets called by the `except Exception as e:` block inside `save_file`
                # Let's verify that mock_remove was called.
                mock_remove.assert_called_once()
