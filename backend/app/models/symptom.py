"""
Symptom Model for Medical Diagnosis
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Float, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from app.core.database import Base

class SymptomSeverity(str, enum.Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

class SymptomDuration(str, enum.Enum):
    ACUTE = "acute"  # < 24 hours
    SUBACUTE = "subacute"  # 1-7 days
    CHRONIC = "chronic"  # > 7 days

class Symptom(Base):
    __tablename__ = "symptoms"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Symptom Information
    name = Column(String, nullable=False)  # e.g., "chest pain", "fever"
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # e.g., "cardiovascular", "respiratory"
    
    # Clinical Details
    severity = Column(Enum(SymptomSeverity), nullable=False)
    duration = Column(Enum(SymptomDuration), nullable=False)
    onset = Column(String, nullable=True)  # e.g., "sudden", "gradual"
    
    # Quantitative Measures
    severity_score = Column(Float, nullable=True)  # 1-10 scale
    frequency = Column(String, nullable=True)  # e.g., "constant", "intermittent"
    
    # Context
    triggers = Column(Text, nullable=True)  # JSON string of triggers
    relieving_factors = Column(Text, nullable=True)  # JSON string
    associated_symptoms = Column(Text, nullable=True)  # JSON string
    
    # Location (for physical symptoms)
    body_location = Column(String, nullable=True)
    laterality = Column(String, nullable=True)  # "left", "right", "bilateral"
    
    # AI Analysis
    icd_10_codes = Column(Text, nullable=True)  # JSON string of potential ICD-10 codes
    snomed_codes = Column(Text, nullable=True)  # JSON string of SNOMED CT codes
    ai_confidence = Column(Float, nullable=True)  # AI confidence in symptom classification
    
    # Relationships
    diagnosis_session_id = Column(UUID(as_uuid=True), ForeignKey("diagnosis_sessions.id"))
    diagnosis_session = relationship("DiagnosisSession", back_populates="symptoms")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Symptom {self.name} - {self.severity}>"
