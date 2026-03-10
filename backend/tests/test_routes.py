import pytest_asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch, MagicMock
import sys

# Mock services BEFORE app imports
mock_rag = MagicMock()
mock_generator = MagicMock()
mock_auditor = MagicMock()

sys.modules['app.services.rag_service'] = MagicMock(rag_service=mock_rag)
sys.modules['app.services.generator_agent'] = MagicMock(generator_agent=mock_generator)
sys.modules['app.services.auditor_agent'] = MagicMock(auditor_agent=mock_auditor)

from sqlmodel.ext.asyncio.session import AsyncSession
from app.main import app
from app.api.routes import get_session
from app.api.auth import get_current_user
from app.models import User, Course

@pytest_asyncio.fixture
def mock_user():
    return User(id=1, email="test@example.com", full_name="Test User", hashed_password="hashed")

@pytest_asyncio.fixture
def mock_session():
    session = AsyncMock(spec=AsyncSession)
    return session

@pytest_asyncio.fixture
async def client(mock_session, mock_user):
    async def override_get_session():
        yield mock_session

    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_course(client: AsyncClient, mock_session: AsyncMock, mock_user: User):
    # Setup mock behavior for session.refresh
    async def mock_refresh(obj):
        obj.id = 1
        obj.creator_id = mock_user.id
        return None

    mock_session.refresh.side_effect = mock_refresh

    # Test payload
    payload = {
        "name": "Test Course",
        "code": "TEST101",
        "semester": "Fall 2024",
        "blueprint_json": {"topics": ["intro"]}
    }

    response = await client.post("/api/courses/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["code"] == payload["code"]
    assert data["semester"] == payload["semester"]
    assert data["blueprint_json"] == payload["blueprint_json"]
    assert data["id"] == 1
    assert data["creator_id"] == mock_user.id

    # Verify mock calls
    mock_session.add.assert_called_once()
    added_course = mock_session.add.call_args[0][0]
    assert isinstance(added_course, Course)
    assert added_course.name == payload["name"]
    assert added_course.code == payload["code"]
    assert added_course.creator_id == mock_user.id

    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(added_course)

@pytest.mark.asyncio
async def test_read_courses(client: AsyncClient, mock_session: AsyncMock, mock_user: User):
    # Setup mock behavior for session.exec().all()
    mock_result = MagicMock()
    mock_courses = [
        Course(id=1, name="Test Course 1", code="TEST101", creator_id=mock_user.id),
        Course(id=2, name="Test Course 2", code="TEST102", creator_id=mock_user.id),
    ]
    mock_result.all.return_value = mock_courses
    mock_session.exec.return_value = mock_result

    response = await client.get("/api/courses/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

    assert data[0]["id"] == 1
    assert data[0]["name"] == "Test Course 1"
    assert data[0]["code"] == "TEST101"
    assert data[0]["creator_id"] == mock_user.id

    assert data[1]["id"] == 2
    assert data[1]["name"] == "Test Course 2"
    assert data[1]["code"] == "TEST102"
    assert data[1]["creator_id"] == mock_user.id

    # Verify mock calls
    mock_session.exec.assert_called_once()
