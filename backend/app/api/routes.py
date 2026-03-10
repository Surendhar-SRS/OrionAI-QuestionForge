from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import func
from sqlmodel import select
from typing import List
from app.core.database import engine
from app.models import Course, Document, Question, AuditLog, User
from app.schemas import CourseCreate, CourseRead, QuestionGenerateRequest, QuestionRead, AuditRequest, RefineRequest
from app.services.rag_service import rag_service
from app.services.generator_agent import generator_agent
from app.services.auditor_agent import auditor_agent
import shutil
import os

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
    current_user: User = Depends(auth.get_current_user)
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
    current_user: User = Depends(auth.get_current_user)
):
    result = await session.exec(select(Course).where(Course.creator_id == current_user.id))
    return result.all()

@router.post("/ingest/")
async def ingest_document(
    course_id: int = Form(...), 
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user)
):
    # Verify course ownership
    course = await session.get(Course, course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")
    # Save file temporarily
    filename = file.filename or "unnamed_file"
    safe_filename = os.path.basename(filename.replace("\\", "/"))
    if not safe_filename or safe_filename == "." or safe_filename == "..":
        safe_filename = "unnamed_file"
    file_location = f"temp_{safe_filename}"

    def save_file():
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    await asyncio.to_thread(save_file)
    
    # Ingest
    try:
        await rag_service.ingest_document(file_location, course_id)
        
        # Save record to DB
        async with AsyncSession(engine) as session:
            doc = Document(
                type="Uploaded", 
                content_hash=safe_filename, # Placeholder hash
                file_path=file_location, 
                course_id=course_id
            )
            session.add(doc)
            await session.commit()
            
        return {"status": "Ingested", "filename": safe_filename}
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)

@router.post("/generate/", response_model=QuestionRead)
async def generate_question_endpoint(
    request: QuestionGenerateRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user)
):
    # Verify course ownership
    course = await session.get(Course, request.course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")
    data = await generator_agent.generate_question(
        request.course_id, 
        request.bloom_level, 
        request.difficulty, 
        request.topic
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
        tags={} # Agent tags
    )
    
    async with AsyncSession(engine) as session:
        session.add(question)
        await session.commit()
        await session.refresh(question)
        return question

@router.post("/audit/")
async def audit_question_endpoint(
    request: AuditRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user)
):
    async with AsyncSession(engine) as session:
        question = await session.get(Question, request.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Verify ownership via course
        course = await session.get(Course, question.course_id)
        if not course or course.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to access this question")
            
        audit_result = await auditor_agent.audit_question(question.dict(), request.topic)
        
        # Save Log
        log = AuditLog(
            iteration_id="manual_1",
            ai_critique=audit_result.get("feedback", ""),
            actions_taken=str(audit_result.get("actions", [])),
            question_id=request.question_id,
            metrics_snapshot={"score": audit_result.get("score")}
        )
        session.add(log)
        await session.commit()
        
        return audit_result

@router.post("/refine/", response_model=QuestionRead)
async def refine_question_endpoint(
    request: RefineRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user)
):
    async with AsyncSession(engine) as session:
        # 1. Get original question
        db_question = await session.get(Question, request.question_id)
        if not db_question:
            raise HTTPException(status_code=404, detail="Question not found")
            
        # 2. Verify ownership
        course = await session.get(Course, db_question.course_id)
        if not course or course.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
            
        # 3. Get context (optional, but helps to re-ground)
        # For efficiency we might skip RAG here or just pass topic. 
        # Let's do a lightweight context retrieval or just rely on the question itself.
        # We'll re-fetch context to be safe.
        context = rag_service.retrieve_context(f"{request.topic}", db_question.course_id)
        context_str = "\n".join(context)
        
        # 4. Call Generator Agent to Refine
        refined_data = await generator_agent.refine_question(
            db_question.dict(), 
            request.critique, 
            context_str, 
            request.topic
        )
        
        if not refined_data:
            raise HTTPException(status_code=500, detail="Refinement failed")
            
        # 5. Update Question in DB (Or create a new version? For now, update in place)
        # Updating in place is simpler for the UI right now.
        db_question.text = refined_data.get("text", db_question.text)
        db_question.answer_key = refined_data.get("answer_key", db_question.answer_key)
        db_question.rubric = refined_data.get("rubric", db_question.rubric)
        db_question.type = refined_data.get("type", db_question.type)
        # Note: we generally keep bloom/difficulty unless changed, which the agent handles.
        
        session.add(db_question)
        await session.commit()
        await session.refresh(db_question)
        
        # 6. Log the refinement action
        log = AuditLog(
            iteration_id=f"refine_{request.question_id}",
            ai_critique="Refinement Step",
            actions_taken=f"Refined based on: {request.critique[:50]}...",
            question_id=request.question_id,
            metrics_snapshot={"score": 100} # Assume improvement
        )
        session.add(log)
        await session.commit()
        
        return db_question

@router.get("/audit-logs/{course_id}")
async def get_audit_logs(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user)
):
    # Verify course ownership
    course = await session.get(Course, course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")
    
    # Get logs for all questions in this course
    statement = select(AuditLog).join(Question).where(Question.course_id == course_id)
    result = await session.exec(statement)
    return result.all()

@router.get("/stats/{course_id}")
async def get_course_stats(
    course_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(auth.get_current_user)
):
    course = await session.get(Course, course_id)
    if not course or course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this course")
    
    # Simplified stats for now
    total_statement = select(func.count()).select_from(Question).where(Question.course_id == course_id)
    total_result = await session.exec(total_statement)
    total = total_result.one()

    bloom_statement = select(Question.bloom_level, func.count()).where(Question.course_id == course_id).group_by(Question.bloom_level)
    bloom_result = await session.exec(bloom_statement)
    bloom_counts = dict(bloom_result.all())
    bloom_dist = {b: bloom_counts.get(b, 0) for b in ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]}

    diff_statement = select(Question.difficulty, func.count()).where(Question.course_id == course_id).group_by(Question.difficulty)
    diff_result = await session.exec(diff_statement)
    diff_counts = dict(diff_result.all())
    diff_dist = {d: diff_counts.get(d, 0) for d in ["Easy", "Medium", "Hard"]}
    
    return {
        "total_questions": total,
        "bloom_distribution": bloom_dist,
        "difficulty_distribution": diff_dist
    }
