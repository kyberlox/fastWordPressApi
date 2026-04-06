from api.database.database import Base

from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship

from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    phone = Column(String(120), unique=True)
    password = Column(String(120))
    full_name = Column(String(120))
    created_at = Column(DateTime, default=datetime.utcnow)