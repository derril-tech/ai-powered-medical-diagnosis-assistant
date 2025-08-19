"""
Medical History Model for Patient Records
"""

from sqlalchemy import Column, String, DateTime, Text, Boolean, ForeignKey, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from app.core.database import Base

class RecordType(str, enum.Enum):
    DIAGNOSIS = "diagnosis"
    PROCEDURE = "procedure"
    MEDICATION = "medication"
    ALLERGY = "allergy"
    IMMUNIZATION = "immunization"
    LAB_RESULT = "lab_result"
    IMAGING = "imaging"
    VITAL_SIGNS = "vital_signs"

class RecordStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    RESOLVED = "resolved"
    CHRONIC = "chronic"

class MedicalHistory(Base):
    __tablename__ = "medical_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Record Information
    record_type = Column(Enum(RecordType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(RecordStatus), default=RecordStatus.ACTIVE)
    
    # Medical Codes
    icd_10_code = Column(String, nullable=True)
    snomed_code = Column(String, nullable=True)
    cpt_code = Column(String, nullable=True)  # For procedures
    
    # Dates
    onset_date = Column(Date, nullable=True)
    resolution_date = Column(Date, nullable=True)
    recorded_date = Column(Date, nullable=False, default=datetime.utcnow().date())
    
    # Clinical Details
    severity = Column(String, nullable=True)  # "mild", "moderate", "severe"
    provider_name = Column(String, nullable=True)
    facility_name = Column(String, nullable=True)
    
    # Medication-specific fields
    dosage = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    route = Column(String, nullable=True)  # "oral", "IV", "topical", etc.
    
    # Lab/Imaging specific fields
    result_value = Column(String, nullable=True)
    result_unit = Column(String, nullable=True)
    reference_range = Column(String, nullable=True)
    abnormal_flag = Column(Boolean, nullable=True)
    
    # Additional Data
    notes = Column(Text, nullable=True)
    external_id = Column(String, nullable=True)  # For EHR integration
    source_system = Column(String, nullable=True)  # e.g., "Epic", "Cerner"
    
    # Relationships
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="medical_history")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MedicalHistory {self.record_type} - {self.title}>"
