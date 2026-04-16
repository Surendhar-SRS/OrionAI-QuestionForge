import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Use Alembic for database migrations
    from app.core.migrations import run_migrations

    await asyncio.to_thread(run_migrations)
    yield


app = FastAPI(title="Question Bank Generator", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
def health_check():
    return {"message": "Question Bank Generator API is running"}


app.include_router(router, prefix="/api")
