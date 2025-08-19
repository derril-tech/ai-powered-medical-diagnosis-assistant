"""
AuraMD Configuration Settings
Centralized configuration management using Pydantic Settings
"""

from typing import List, Optional
from pydantic import BaseSettings, validator
import secrets

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "AuraMD"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql://auramd_user:auramd_password@localhost:5432/auramd"
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI APIs
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Cloud Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: str = "auramd-medical-files"
    AWS_REGION: str = "us-east-1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://auramd.vercel.app"
    ]
    
    # Security
    ALLOWED_HOSTS: List[str] = ["*"]
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: List[str] = [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/dicom",
        "text/plain"
    ]
    
    # Medical Settings
    DIAGNOSIS_CONFIDENCE_THRESHOLD: float = 0.7
    MAX_DIFFERENTIAL_DIAGNOSES: int = 10
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()
