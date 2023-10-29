from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import config

engine = create_async_engine(
    f"postgresql+asyncpg://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_URL']}/{config['DB_NAME']}",
    future=True,
    echo=True,
)

AsyncSessionFactory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)

async def get_session() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
