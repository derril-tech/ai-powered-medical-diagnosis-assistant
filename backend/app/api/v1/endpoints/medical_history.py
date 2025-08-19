"""
Medical History Endpoints
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.medical_history import MedicalHistory

router = APIRouter()

@router.get("/")
async def get_medical_history(
    patient_id: str = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get medical history records"""
    query = db.query(MedicalHistory)
    
    if patient_id:
        query = query.filter(MedicalHistory.patient_id == patient_id)
    
    records = query.offset(skip).limit(limit).all()
    return records
