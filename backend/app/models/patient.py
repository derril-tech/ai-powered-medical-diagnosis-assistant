"""
Patient Model for Medical Records
"""

from sqlalchemy import Column, String, Integer, Date, DateTime, Text, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, date
import enum

from app.core.database import Base

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Personal Information
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    
    # Contact Information
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    
    # Medical Identifiers
    medical_record_number = Column(String, unique=True, nullable=True)
    insurance_number = Column(String, nullable=True)
    
    # Emergency Contact
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    emergency_contact_relationship = Column(String, nullable=True)
    
    # Medical Information
    blood_type = Column(String, nullable=True)
    allergies = Column(Text, nullable=True)  # JSON string of allergies
    chronic_conditions = Column(Text, nullable=True)  # JSON string of conditions
    current_medications = Column(Text, nullable=True)  # JSON string of medications
    
    # Privacy & Consent
    consent_for_ai_analysis = Column(Boolean, default=False)
    data_sharing_consent = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medical_history = relationship("MedicalHistory", back_populates="patient")
    diagnosis_sessions = relationship("DiagnosisSession", back_populates="patient")
    
    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
