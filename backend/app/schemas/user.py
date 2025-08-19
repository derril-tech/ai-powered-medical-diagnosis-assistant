"""
User Schemas
Pydantic models for user management
"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.DOCTOR
    medical_license: Optional[str] = None
    specialization: Optional[str] = None
    hospital_affiliation: Optional[str] = None
