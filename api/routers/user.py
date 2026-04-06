from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from api.database.database import get_db
from api.models.user import User
from api.schemas.user import UserBase as UserSchema

router = APIRouter(prefix="/users", tags=["Пользователи"])

@router.get("/{user_id}", response_model=List[UserSchema])
async def get_users(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().one()

@router.get("/", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.post("/")
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    db.add(user)
    await db.commit()
    return user

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user.name
    await db.commit()
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted"}