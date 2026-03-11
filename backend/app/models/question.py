from typing import TYPE_CHECKING, Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON


class QuestionBase(SQLModel):
    text: str
    type: str  # MCQ, Short, Long
    marks: int
    bloom_level: str
    difficulty: str
    tags: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    answer_key: str
    rubric: str
    course_id: Optional[int] = Field(default=None, foreign_key="course.id")
    accepted: bool = Field(default=False)


class Question(QuestionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course: Optional["Course"] = Relationship(back_populates="questions")
    audit_logs: List["AuditLog"] = Relationship(back_populates="question")


if TYPE_CHECKING:
    from .course import Course
    from .audit_log import AuditLog
