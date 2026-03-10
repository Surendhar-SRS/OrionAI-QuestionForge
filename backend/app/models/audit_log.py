from typing import TYPE_CHECKING, Optional, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON

class AuditLogBase(SQLModel):
    iteration_id: str
    metrics_snapshot: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    ai_critique: str
    actions_taken: str
    question_id: Optional[int] = Field(default=None, foreign_key="question.id")

class AuditLog(AuditLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: Optional["Question"] = Relationship(back_populates="audit_logs")


if TYPE_CHECKING:
    from .question import Question
