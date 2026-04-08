from fastapi import FastAPI, APIRouter, Response, status, HTTPException, Depends, File, UploadFile, Form
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.database.database import engine, Base
from api.routers import user



app = FastAPI(
    title="REST API для ...",
    description="Описание",
    version="1.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prefix="/api", router=user.router)

@app.on_event("startup")
async def create_tables():
    """Автоматическое создание таблиц при запуске приложения."""
    import asyncio
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Таблицы базы данных созданы/проверены")
            break
        except Exception as e:
            print(f"❌ Попытка {attempt}/{max_attempts} не удалась: {e}")
            if attempt == max_attempts:
                print("⚠️  Не удалось создать таблицы. Продолжаем работу, возможно таблицы уже существуют.")
                import traceback
                traceback.print_exc()
            else:
                await asyncio.sleep(2 ** attempt)  # экспоненциальная задержка


@app.get("/health")
async def health_check():
    return {"status": "healthy"}    