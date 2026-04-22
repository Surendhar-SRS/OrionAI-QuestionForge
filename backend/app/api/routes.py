from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from typing import List
from app.core.database import engine
from app.models import Course, Document, Question, AuditLog, User
from app.schemas import (
    CourseCreate,
    CourseRead,
    QuestionGenerateRequest,
    QuestionRead,
    AuditRequest,
    RefineRequest,
)
from app.services.rag_service import rag_service
from app.services.generator_agent import generator_agent
from app.services.auditor_agent import auditor_agent

from werkzeug.utils import secure_filename
import os
import tempfile
import hashlib

import asyncio
from app.api import auth

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


@router.post("/courses/", response_model=CourseRead)
async def create_course(
    course: CourseCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    db_course = Course.from_orm(course)
    db_course.creator_id = current_user.id
    session.add(db_course)
    await session.commit()
    await session.refresh(db_course)
    return db_course


@router.get("/courses/", response_model=List[CourseRead])
async def read_courses(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    result = await session.exec(
        select(Course).where(Course.creator_id == current_user.id)
    )
    return result.all()


@router.post("/ingest/")
async def ingest_document(
    course_id: int = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    # Verify course ownership
    course = await session.get(Course, course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this course"
        )
    # Save file temporarily
    filename = file.filename or "unnamed_file"
    safe_filename = secure_filename(filename)
    if not safe_filename:
        safe_filename = "unnamed_file"

    _, extension = os.path.splitext(safe_filename)

    import aiofiles
    import aiofiles.os

    def get_temp_file():
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
            return temp_file.name

    file_location = await asyncio.to_thread(get_temp_file)
    hasher = hashlib.sha256()

    try:
        async with aiofiles.open(file_location, "wb") as buffer:
            while chunk := await file.read(65536):
                hasher.update(chunk)
                await buffer.write(chunk)
        file_hash = hasher.hexdigest()
    except Exception as e:
        if await aiofiles.os.path.exists(file_location):
            await aiofiles.os.remove(file_location)
        raise e

    # Ingest
    try:
        await rag_service.ingest_document(file_location, course_id)

        # Save record to DB
        doc = Document(
            type="Uploaded",
            content_hash=file_hash,
            file_path=file_location,
            course_id=course_id,
        )
        session.add(doc)
        await session.commit()

        return {"status": "Ingested", "filename": safe_filename}
    finally:
        if await aiofiles.os.path.exists(file_location):
            await aiofiles.os.remove(file_location)


@router.post("/generate/", response_model=QuestionRead)
async def generate_question_endpoint(
    request: QuestionGenerateRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    # Verify course ownership
    course = await session.get(Course, request.course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this course"
        )
    data = await generator_agent.generate_question(
        request.course_id, request.bloom_level, request.difficulty, request.topic
    )
    if not data:
        raise HTTPException(status_code=500, detail="Generation failed")

    # Format for DB (Schema mismatch adaptation might be needed if agent output varies)
    # Assuming Agent output matches QuestionBase keys roughly
    question = Question(
        text=data.get("text"),
        type=data.get("type"),
        marks=data.get("marks"),
        bloom_level=request.bloom_level,
        difficulty=request.difficulty,
        answer_key=data.get("answer_key"),
        rubric=data.get("rubric"),
        course_id=request.course_id,
        tags={},  # Agent tags
    )

    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


@router.post("/audit/")
async def audit_question_endpoint(
    request: AuditRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    question = await session.get(Question, request.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Verify ownership via course
    course = await session.get(Course, question.course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this question"
        )

    audit_result = await auditor_agent.audit_question(question.dict(), request.topic)

    # Save Log
    log = AuditLog(
        iteration_id="manual_1",
        ai_critique=audit_result.get("feedback", ""),
        actions_taken=str(audit_result.get("actions", [])),
        question_id=request.question_id,
        metrics_snapshot={"score": audit_result.get("score")},
    )
    session.add(log)
    await session.commit()

    return audit_result


async def _verify_question_ownership(
    session: AsyncSession, question_id: int, user_id: int
):
    """Fetch question and verify course ownership."""
    db_question = await session.get(Question, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    course = await session.get(Course, db_question.course_id)
    if not course or course.creator_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return db_question


async def _retrieve_refinement_context(topic: str, course_id: int) -> str:
    """Retrieve context string from RAG service."""
    context = await asyncio.to_thread(
        rag_service.retrieve_context, f"{topic}", course_id
    )
    return "\n".join(context)


async def _log_refinement_action(session: AsyncSession, request_id: int, critique: str):
    """Log the refinement action to the database."""
    log = AuditLog(
        iteration_id=f"refine_{request_id}",
        ai_critique="Refinement Step",
        actions_taken=f"Refined based on: {critique[:50]}...",
        question_id=request_id,
        metrics_snapshot={"score": 100},  # Assume improvement
    )
    session.add(log)
    await session.commit()


@router.post("/refine/", response_model=QuestionRead)
async def refine_question_endpoint(
    request: RefineRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    # 1. Get original question & verify ownership
    db_question = await _verify_question_ownership(
        session, request.question_id, current_user.id
    )

    # 2. Get context
    context_str = await _retrieve_refinement_context(
        request.topic, db_question.course_id
    )

    # 3. Call Generator Agent to Refine
    refined_data = await generator_agent.refine_question(
        db_question.dict(), request.critique, context_str, request.topic
    )
    if not refined_data:
        raise HTTPException(status_code=500, detail="Refinement failed")

    # 4. Update Question in DB
    db_question.text = refined_data.get("text", db_question.text)
    db_question.answer_key = refined_data.get("answer_key", db_question.answer_key)
    db_question.rubric = refined_data.get("rubric", db_question.rubric)
    db_question.type = refined_data.get("type", db_question.type)

    session.add(db_question)
    await session.commit()
    await session.refresh(db_question)

    # 5. Log the refinement action
    await _log_refinement_action(session, request.question_id, request.critique)

    return db_question


@router.get("/audit-logs/{course_id}")
async def get_audit_logs(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    # Verify course ownership
    course = await session.get(Course, course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this course"
        )

    # Get logs for all questions in this course
    statement = select(AuditLog).join(Question).where(Question.course_id == course_id)
    result = await session.exec(statement)
    return result.all()


@router.get("/stats/{course_id}")
async def get_course_stats(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    course = await session.get(Course, course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this course"
        )

    # ⚡ Bolt: Single query for aggregated stats
    statement = (
        select(
            func.count(Question.id).label("total"),
            Question.bloom_level,
            Question.difficulty,
        )
        .where(Question.course_id == course_id)
        .group_by(Question.bloom_level, Question.difficulty)
    )
    result = await session.exec(statement)
    rows = result.all()

    total = 0
    bloom_dist = {
        b: 0
        for b in ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    }
    diff_dist = {d: 0 for d in ["Easy", "Medium", "Hard"]}

    for count, bloom, diff in rows:
        total += count
        if bloom in bloom_dist:
            bloom_dist[bloom] += count
        if diff in diff_dist:
            diff_dist[diff] += count

    return {
        "total_questions": total,
        "bloom_distribution": bloom_dist,
        "difficulty_distribution": diff_dist,
    }
