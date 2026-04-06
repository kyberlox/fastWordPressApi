from pydantic import BaseModel, Field
from typing import Optional, List

from datetime import datetime

class User(BaseModel):
    id: int
    email: str
    phone: str
    password: str
    full_name: str
    created_at: datetime

class UserBase(BaseModel):
    email: str = Field(..., example="user@example.com")
    phone: str = Field(..., example="+79991234567")
    password: str = Field(..., example="password")
    full_name: str = Field(..., example="John Doe")