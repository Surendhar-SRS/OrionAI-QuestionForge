from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.core.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # In production, use Alembic. For hackathon, create tables on startup.
    async with engine.begin() as conn:
        # Import models to ensure they are registered with SQLModel
        from app import models
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(title="Question Bank Generator", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Question Bank Generator API is running"}

from app.api.routes import router
app.include_router(router, prefix="/api")
