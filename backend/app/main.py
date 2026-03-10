from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.core.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # In production, use Alembic. For hackathon, create tables on startup.
    async with engine.begin() as conn:
        # Import models to ensure they are registered with SQLModel
        from app import models  # noqa: F401
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(title="Question Bank Generator", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Question Bank Generator API is running"}

app.include_router(router, prefix="/api")
