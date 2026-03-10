from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    courses: List["Course"] = Relationship(back_populates="creator")



if TYPE_CHECKING:
    from .course import Course
