"""
Diagnosis Endpoints
AI-powered medical diagnosis and analysis
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.patient import Patient
from app.models.diagnosis import DiagnosisSession, Diagnosis
from app.models.symptom import Symptom
from app.schemas.diagnosis import (
    DiagnosisRequest,
    DiagnosisResponse,
    DiagnosisSessionResponse
)
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/analyze", response_model=DiagnosisResponse)
async def analyze_symptoms(
    diagnosis_request: DiagnosisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Analyze patient symptoms and generate AI-powered diagnosis"""
    
    # Verify patient exists and user has access
    patient = db.query(Patient).filter(Patient.id == diagnosis_request.patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )
    
    # Create diagnosis session
    diagnosis_session = DiagnosisSession(
        patient_id=diagnosis_request.patient_id,
        user_id=current_user.id,
        chief_complaint=diagnosis_request.chief_complaint,
        status="in_progress"
    )
    
    db.add(diagnosis_session)
    db.commit()
    db.refresh(diagnosis_session)
    
    # Create symptoms
    symptoms = []
    for symptom_data in diagnosis_request.symptoms:
        symptom = Symptom(
            diagnosis_session_id=diagnosis_session.id,
            name=symptom_data.name,
            description=symptom_data.description,
            severity=symptom_data.severity,
            duration=symptom_data.duration,
            body_location=symptom_data.body_location,
            associated_symptoms=symptom_data.associated_symptoms,
            triggers=symptom_data.triggers,
            relieving_factors=symptom_data.relieving_factors
        )
        db.add(symptom)
        symptoms.append(symptom)
    
    db.commit()
    
    try:
        # Get AI analysis
        ai_analysis = await ai_service.analyze_symptoms(
            symptoms=symptoms,
            patient=patient,
            medical_history=diagnosis_request.medical_history
        )
        
        # Create diagnosis records
        diagnoses = []
        for i, diagnosis_data in enumerate(ai_analysis["differential_diagnoses"]):
            diagnosis = Diagnosis(
                diagnosis_session_id=diagnosis_session.id,
                condition_name=diagnosis_data["condition_name"],
                confidence_score=diagnosis_data["confidence_score"],
                ai_reasoning=diagnosis_data["ai_reasoning"],
                differential_rank=i + 1,
                probability_percentage=diagnosis_data["confidence_score"] * 100
            )
            db.add(diagnosis)
            diagnoses.append(diagnosis)
        
        # Update session with AI results
        diagnosis_session.status = "completed"
        diagnosis_session.ai_summary = ai_analysis["clinical_reasoning"]
        diagnosis_session.urgency_level = ai_analysis["urgency_level"]
        
        db.commit()
        
        # Generate medical summary in background
        background_tasks.add_task(
            generate_medical_summary_task,
            diagnosis_session.id,
            db
        )
        
        return DiagnosisResponse(
            session_id=str(diagnosis_session.id),
            differential_diagnoses=[
                {
                    "condition_name": d["condition_name"],
                    "confidence_score": d["confidence_score"],
                    "ai_reasoning": d["ai_reasoning"],
                    "differential_rank": i + 1
                }
                for i, d in enumerate(ai_analysis["differential_diagnoses"])
            ],
            recommended_tests=ai_analysis["recommended_tests"],
            urgency_level=ai_analysis["urgency_level"],
            clinical_reasoning=ai_analysis["clinical_reasoning"],
            red_flags=ai_analysis["red_flags"],
            ai_summary=ai_analysis["clinical_reasoning"]
        )
        
    except Exception as e:
        # Update session status on error
        diagnosis_session.status = "cancelled"
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI analysis failed: {str(e)}"
        )

@router.get("/sessions", response_model=List[DiagnosisSessionResponse])
async def get_diagnosis_sessions(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get diagnosis sessions for current user"""
    
    sessions = db.query(DiagnosisSession)\
        .filter(DiagnosisSession.user_id == current_user.id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return sessions

@router.get("/sessions/{session_id}", response_model=DiagnosisSessionResponse)
async def get_diagnosis_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get specific diagnosis session"""
    
    session = db.query(DiagnosisSession)\
        .filter(
            DiagnosisSession.id == session_id,
            DiagnosisSession.user_id == current_user.id
        )\
        .first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnosis session not found"
        )
    
    return session

async def generate_medical_summary_task(session_id: str, db: Session):
    """Background task to generate medical summary"""
    try:
        session = db.query(DiagnosisSession).filter(DiagnosisSession.id == session_id).first()
        if session:
            summary = await ai_service.generate_medical_summary(session)
            session.ai_summary = summary
            db.commit()
    except Exception as e:
        print(f"Failed to generate medical summary: {e}")
