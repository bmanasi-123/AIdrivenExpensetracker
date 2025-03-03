from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData

DATABASE_URL = "postgresql+asyncpg://postgres:12345678@localhost:5432/expenseTracker"

# Create an async engine
# engine = create_async_engine(DATABASE_URL, echo=True)
engine = create_async_engine(
    DATABASE_URL, echo=True, pool_size=20, max_overflow=10
)

SessionLocal = sessionmaker( bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
