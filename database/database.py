from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from database.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL) 
async_session_maker = async_sessionmaker(engine, expire_on_commit=False) 

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_db(session: AsyncSession = Depends(get_async_session)):
    return session

# async def get_film_db(session: AsyncSession = Depends(get_async_session)):
#     return session



