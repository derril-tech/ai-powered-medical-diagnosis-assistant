"""
AuraMD Database Configuration
SQLAlchemy setup with PostgreSQL and pgvector for medical AI features
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import redis
from app.core.config import settings

# SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Redis connection
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# Metadata for database operations
metadata = MetaData()

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    """Redis dependency for FastAPI"""
    return redis_client

async def init_db():
    """Initialize database with required extensions"""
    try:
        # Enable pgvector extension for AI features
        with engine.connect() as conn:
            conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            conn.commit()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
