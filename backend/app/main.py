from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Use Alembic for database migrations
    from app.core.migrations import run_migrations
    import asyncio

    await asyncio.to_thread(run_migrations)
    yield


app = FastAPI(title="Question Bank Generator", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
def read_root():
    return {"message": "Question Bank Generator API is running"}


from app.api.routes import router

app.include_router(router, prefix="/api")
