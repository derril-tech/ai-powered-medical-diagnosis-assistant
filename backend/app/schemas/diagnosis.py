"""
Diagnosis Schemas
Pydantic models for diagnosis endpoints
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class SymptomSeverity(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

class SymptomDuration(str, Enum):
    ACUTE = "acute"
    SUBACUTE = "subacute"
    CHRONIC = "chronic"

class SymptomCreate(BaseModel):
    name: str = Field(..., description="Symptom name")
    description: Optional[str] = None
    severity: SymptomSeverity
    duration: SymptomDuration
    body_location: Optional[str] = None
    associated_symptoms: Optional[str] = None
    triggers: Optional[str] = None
    relieving_factors: Optional[str] = None

class DiagnosisRequest(BaseModel):
    patient_id: str
    chief_complaint: str
    symptoms: List[SymptomCreate]
    medical_history: Optional[str] = None

class DiagnosisResult(BaseModel):
    condition_name: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    ai_reasoning: str
    icd_10_code: Optional[str] = None
    differential_rank: int

class DiagnosisResponse(BaseModel):
    session_id: str
    differential_diagnoses: List[DiagnosisResult]
    recommended_tests: List[str]
    urgency_level: str
    clinical_reasoning: str
    red_flags: List[str]
    ai_summary: str

class DiagnosisSessionResponse(BaseModel):
    id: str
    patient_id: str
    user_id: str
    chief_complaint: str
    status: str
    urgency_level: Optional[str] = None
    ai_summary: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
