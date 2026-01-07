import os
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/qbank_db")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
