from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("user")
password = os.getenv("pswd")
database = os.getenv("DB_NAME_API", os.getenv("dbname", "pdb"))
host = "postgres"
port = "5432"
DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL запросов (можно отключить в продакшене)
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для моделей
Base = declarative_base()


# Dependency для получения сессии в эндпоинтах
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()