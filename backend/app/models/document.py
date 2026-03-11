from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship


class DocumentBase(SQLModel):
    type: str  # Syllabus, Notes, PastPaper
    content_hash: str = Field(index=True)
    file_path: str
    course_id: Optional[int] = Field(default=None, foreign_key="course.id")


class Document(DocumentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    course: Optional["Course"] = Relationship(back_populates="documents")


if TYPE_CHECKING:
    from .course import Course
