"""
Symptom Management Endpoints
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.symptom import Symptom

router = APIRouter()

@router.get("/")
async def get_symptoms(
    session_id: str = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get symptoms"""
    query = db.query(Symptom)
    
    if session_id:
        query = query.filter(Symptom.diagnosis_session_id == session_id)
    
    symptoms = query.offset(skip).limit(limit).all()
    return symptoms
