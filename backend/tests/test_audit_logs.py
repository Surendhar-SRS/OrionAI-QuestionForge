import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.routes import get_session
from app.api.auth import get_current_user
from app.models import User, Course, Question, AuditLog

# Database setup for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with async_session_maker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture
async def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[get_session] = _get_session_override
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_user(session):
    user = User(email="test@example.com", hashed_password="fake", full_name="Test User")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@pytest_asyncio.fixture
async def other_user(session):
    user = User(email="other@example.com", hashed_password="fake", full_name="Other User")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@pytest.mark.asyncio
async def test_get_audit_logs_success(client, session, test_user):
    # Setup: Mock current user
    app.dependency_overrides[get_current_user] = lambda: test_user

    # Create course
    course = Course(name="Test Course", code="TC101", creator_id=test_user.id)
    session.add(course)
    await session.commit()
    await session.refresh(course)

    # Create question
    question = Question(
        text="What is 2+2?",
        type="MCQ",
        marks=5,
        bloom_level="Understand",
        difficulty="Easy",
        answer_key="4",
        rubric="Correct answer gets 5 marks",
        course_id=course.id
    )
    session.add(question)
    await session.commit()
    await session.refresh(question)

    # Create audit log
    audit_log = AuditLog(
        iteration_id="test_1",
        ai_critique="Good",
        actions_taken="None",
        question_id=question.id,
        metrics_snapshot={"score": 100}
    )
    session.add(audit_log)
    await session.commit()

    response = await client.get(f"/api/audit-logs/{course.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["iteration_id"] == "test_1"
    assert data[0]["question_id"] == question.id

@pytest.mark.asyncio
async def test_get_audit_logs_unauthorized(client, session, test_user, other_user):
    # Setup: Current user is test_user, but course belongs to other_user
    app.dependency_overrides[get_current_user] = lambda: test_user

    course = Course(name="Other Course", code="OC101", creator_id=other_user.id)
    session.add(course)
    await session.commit()
    await session.refresh(course)

    response = await client.get(f"/api/audit-logs/{course.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to access this course"

@pytest.mark.asyncio
async def test_get_audit_logs_not_found(client, session, test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user

    # Use a non-existent course ID
    response = await client.get("/api/audit-logs/999")
    assert response.status_code == 403 # Current implementation returns 403 if course not found or not owner
    assert response.json()["detail"] == "Not authorized to access this course"

@pytest.mark.asyncio
async def test_get_audit_logs_empty(client, session, test_user):
    app.dependency_overrides[get_current_user] = lambda: test_user

    course = Course(name="Empty Course", code="EC101", creator_id=test_user.id)
    session.add(course)
    await session.commit()
    await session.refresh(course)

    response = await client.get(f"/api/audit-logs/{course.id}")
    assert response.status_code == 200
    assert response.json() == []
