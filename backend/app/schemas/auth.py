"""
Authentication Schemas
Pydantic models for authentication endpoints
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from app.models.user import UserRole

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.DOCTOR
    medical_license: Optional[str] = None
    specialization: Optional[str] = None
    hospital_affiliation: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: UserRole
    medical_license: Optional[str] = None
    specialization: Optional[str] = None
    hospital_affiliation: Optional[str] = None
    is_active: bool
    is_verified: bool
    
    class Config:
        from_attributes = True
