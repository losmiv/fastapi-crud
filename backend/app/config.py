import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

DB_CONFIG = os.getenv("DB_URL")


class AsyncDatabaseSession:

    def __init__(self):
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self):
        self.engine = create_async_engine(
            DB_CONFIG,
            future=True,
            echo=True,
            pool_size=10,
            max_overflow=20
        )
        self.session = sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


db = AsyncDatabaseSession()


async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
