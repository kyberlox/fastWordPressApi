import asyncio
import sys
import os
from database.database import engine, Base
from api.models import user



async def create_tables():
    async with engine.begin() as conn:
        # Удаляем существующие таблицы (для разработки)
        # В продакшене используйте миграции Alembic
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы успешно")


if __name__ == "__main__":
    asyncio.run(create_tables())