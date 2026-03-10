from typing import TYPE_CHECKING, Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON

class CourseBase(SQLModel):
    name: str = Field(index=True)
    code: str = Field(index=True)
    semester: Optional[str] = None
    blueprint_json: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

class Course(CourseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creator_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    creator: Optional["User"] = Relationship(back_populates="courses")
    documents: List["Document"] = Relationship(back_populates="course")
    questions: List["Question"] = Relationship(back_populates="course")


if TYPE_CHECKING:
    from .user import User
    from .document import Document
    from .question import Question
