from app.database import Base
from sqlalchemy import Column, Integer, String, func, DateTime, Boolean
from pydantic import BaseModel, Field

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, server_default=func.now())


class UserRequest(BaseModel):
    username: str = Field(min_length=3)
    full_name: str = Field(min_length=3)
    password: str = Field(min_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str