from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime



class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @field_validator('username')
    def username_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Username cannot be empty')
        if len(v.strip()) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v.strip()
    
    @field_validator('email')
    def email_must_be_valid(cls, v):
        if not v.strip():
            raise ValueError('Email cannot be empty')
        if '@' not in v or v.startswith('@'):
            raise ValueError('Please enter a valid email address')
        return v.strip()
    
    @field_validator('password')
    def password_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Password cannot be empty')
        if len(v.strip()) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v.strip()

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True




