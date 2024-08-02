from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import database_exists, create_database
from src.core.config import settings
from src.core.logger import logger


if not database_exists(settings.DB_URL_STR_SYNC):
    create_database(settings.DB_URL_STR_SYNC)


async_engine = create_async_engine(
    settings.DB_URL_STR_ASYNC,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_POOL_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE,
    future=True
)


async_session_factory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=settings.DB_AUTO_FLUSH,
    expire_on_commit=settings.DB_EXPIRE_COMMIT,
)


async_scoped_session_factory = scoped_session(async_session_factory)


async def db_session() -> AsyncGenerator:
    async with async_scoped_session_factory() as session:
        try:
            yield session
        except exc.SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def init_tables():
    async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_all_session():
    if async_session_factory is not None:
        async_session_factory.close_all()