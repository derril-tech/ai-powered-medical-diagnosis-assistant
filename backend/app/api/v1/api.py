"""
AuraMD API v1 Router
Main API router that includes all endpoint modules
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, patients, symptoms, diagnosis, medical_history, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(symptoms.router, prefix="/symptoms", tags=["symptoms"])
api_router.include_router(diagnosis.router, prefix="/diagnosis", tags=["diagnosis"])
api_router.include_router(medical_history.router, prefix="/medical-history", tags=["medical-history"])
