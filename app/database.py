from .config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    expire_on_commit=False, autoflush=False, bind=async_engine
)


async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
