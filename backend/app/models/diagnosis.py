"""
Diagnosis Models for Medical AI Analysis
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, Float, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from app.core.database import Base

class DiagnosisStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    REVIEWED = "reviewed"
    CANCELLED = "cancelled"

class DiagnosisConfidence(str, enum.Enum):
    LOW = "low"  # < 0.5
    MODERATE = "moderate"  # 0.5 - 0.7
    HIGH = "high"  # 0.7 - 0.9
    VERY_HIGH = "very_high"  # > 0.9

class DiagnosisSession(Base):
    __tablename__ = "diagnosis_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Session Information
    session_name = Column(String, nullable=True)
    chief_complaint = Column(Text, nullable=False)  # Primary reason for consultation
    status = Column(Enum(DiagnosisStatus), default=DiagnosisStatus.PENDING)
    
    # Relationships
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    patient = relationship("Patient", back_populates="diagnosis_sessions")
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="diagnosis_sessions")
    
    symptoms = relationship("Symptom", back_populates="diagnosis_session")
    diagnoses = relationship("Diagnosis", back_populates="diagnosis_session")
    
    # AI Analysis Results
    ai_summary = Column(Text, nullable=True)  # AI-generated summary
    risk_factors = Column(Text, nullable=True)  # JSON string of risk factors
    recommended_tests = Column(Text, nullable=True)  # JSON string of recommended tests
    urgency_level = Column(String, nullable=True)  # "low", "moderate", "high", "emergency"
    
    # Clinical Notes
    clinical_notes = Column(Text, nullable=True)
    physician_assessment = Column(Text, nullable=True)
    treatment_plan = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<DiagnosisSession {self.id} - {self.status}>"

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Diagnosis Information
    condition_name = Column(String, nullable=False)
    icd_10_code = Column(String, nullable=True)
    snomed_code = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    # AI Analysis
    confidence_score = Column(Float, nullable=False)  # 0.0 - 1.0
    confidence_level = Column(Enum(DiagnosisConfidence), nullable=False)
    ai_reasoning = Column(Text, nullable=True)  # AI explanation for diagnosis
    
    # Clinical Information
    differential_rank = Column(Integer, nullable=False)  # 1 = most likely
    probability_percentage = Column(Float, nullable=True)  # Percentage likelihood
    
    # Supporting Evidence
    supporting_symptoms = Column(Text, nullable=True)  # JSON string
    contradicting_factors = Column(Text, nullable=True)  # JSON string
    required_tests = Column(Text, nullable=True)  # JSON string of tests needed
    
    # Treatment Information
    treatment_urgency = Column(String, nullable=True)  # "immediate", "urgent", "routine"
    treatment_options = Column(Text, nullable=True)  # JSON string of treatments
    prognosis = Column(Text, nullable=True)
    
    # Relationships
    diagnosis_session_id = Column(UUID(as_uuid=True), ForeignKey("diagnosis_sessions.id"))
    diagnosis_session = relationship("DiagnosisSession", back_populates="diagnoses")
    
    evidence_references = relationship("EvidenceReference", back_populates="diagnosis")
    
    # Review Status
    physician_approved = Column(Boolean, default=False)
    physician_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Diagnosis {self.condition_name} - {self.confidence_level}>"
