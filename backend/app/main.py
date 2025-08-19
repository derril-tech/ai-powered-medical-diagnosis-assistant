"""
AuraMD: AI-Powered Medical Diagnosis Assistant
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import structlog

from app.core.config import settings
from app.core.database import engine, Base
from app.core.security import get_current_user
from app.api.v1.api import api_router
from app.websocket.connection_manager import ConnectionManager

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="AuraMD API",
    description="AI-Powered Medical Diagnosis Assistant for Healthcare Professionals",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Security
security = HTTPBearer()

# WebSocket Connection Manager
connection_manager = ConnectionManager()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# WebSocket endpoint for real-time medical consultations
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket, user_id: str):
    """WebSocket endpoint for real-time medical consultations"""
    await connection_manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(
                f"Message from {user_id}: {data}", user_id
            )
    except Exception as e:
        logger.error("WebSocket error", error=str(e), user_id=user_id)
    finally:
        connection_manager.disconnect(user_id)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AuraMD API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AuraMD - AI-Powered Medical Diagnosis Assistant",
        "version": "1.0.0",
        "docs": "/api/v1/docs",
        "health": "/health"
    }

@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("Starting AuraMD API", version="1.0.0", environment=settings.ENVIRONMENT)
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down AuraMD API")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
