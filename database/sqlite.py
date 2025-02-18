from sqlalchemy.ext.asyncio import create_async_engine
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from config import settings

URL = settings.DB_URL

engine = create_async_engine(URL, echo=False, query_cache_size=100)

session_local = sessionmaker(autoflush=True, expire_on_commit=False, bind=engine, class_=AsyncSession)

@asynccontextmanager
async def get_db():
    async with session_local() as db:
        try:
            yield db
            await db.commit()
        except Exception as ex:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Internal server db error: {ex}")
        finally:
            await db.close()