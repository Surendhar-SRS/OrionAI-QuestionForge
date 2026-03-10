import os
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/qbank_db")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
