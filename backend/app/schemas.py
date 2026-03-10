from pydantic import BaseModel
from typing import Optional, Dict, Any

class CourseCreate(BaseModel):
    name: str
    code: str
    semester: Optional[str] = None
    blueprint_json: Dict[str, Any] = {}

class CourseRead(CourseCreate):
    id: int
    creator_id: Optional[int]

class DocumentRead(BaseModel):
    id: int
    type: str
    file_path: str
    course_id: int

class QuestionGenerateRequest(BaseModel):
    course_id: int
    topic: str
    bloom_level: str
    difficulty: str

class QuestionRead(BaseModel):
    id: Optional[int]
    text: str
    type: str
    marks: int
    bloom_level: str
    difficulty: str
    answer_key: str
    rubric: str
    accepted: bool
    tags: Dict[str, Any] = {}

class AuditRequest(BaseModel):
    question_id: int
    topic: str

class RefineRequest(BaseModel):
    question_id: int
    critique: str
    topic: str

# Auth Schemas
class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
