"""
User Model for Healthcare Professionals
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from app.core.database import Base

class UserRole(str, enum.Enum):
    DOCTOR = "doctor"
    NURSE = "nurse"
    ADMIN = "admin"
    SPECIALIST = "specialist"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.DOCTOR)
    
    # Professional Information
    medical_license = Column(String, unique=True, nullable=True)
    specialization = Column(String, nullable=True)
    hospital_affiliation = Column(String, nullable=True)
    
    # Account Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    diagnosis_sessions = relationship("DiagnosisSession", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    @property
    def is_medical_professional(self):
        return self.role in [UserRole.DOCTOR, UserRole.NURSE, UserRole.SPECIALIST]
