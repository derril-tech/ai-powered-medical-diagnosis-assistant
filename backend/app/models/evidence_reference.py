"""
Evidence Reference Model for Medical Literature and Guidelines
"""

from sqlalchemy import Column, String, DateTime, Text, Float, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from app.core.database import Base

class EvidenceType(str, enum.Enum):
    CLINICAL_STUDY = "clinical_study"
    SYSTEMATIC_REVIEW = "systematic_review"
    META_ANALYSIS = "meta_analysis"
    CLINICAL_GUIDELINE = "clinical_guideline"
    CASE_STUDY = "case_study"
    TEXTBOOK = "textbook"
    MEDICAL_DATABASE = "medical_database"

class EvidenceQuality(str, enum.Enum):
    HIGH = "high"  # Grade A evidence
    MODERATE = "moderate"  # Grade B evidence
    LOW = "low"  # Grade C evidence
    VERY_LOW = "very_low"  # Grade D evidence

class EvidenceReference(Base):
    __tablename__ = "evidence_references"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Reference Information
    title = Column(String, nullable=False)
    authors = Column(Text, nullable=True)  # JSON string of authors
    journal = Column(String, nullable=True)
    publication_date = Column(DateTime, nullable=True)
    doi = Column(String, nullable=True)
    pubmed_id = Column(String, nullable=True)
    
    # Evidence Classification
    evidence_type = Column(Enum(EvidenceType), nullable=False)
    evidence_quality = Column(Enum(EvidenceQuality), nullable=False)
    
    # Content
    abstract = Column(Text, nullable=True)
    key_findings = Column(Text, nullable=True)  # JSON string of key findings
    methodology = Column(Text, nullable=True)
    sample_size = Column(String, nullable=True)
    
    # Relevance Scoring
    relevance_score = Column(Float, nullable=True)  # 0.0 - 1.0
    ai_summary = Column(Text, nullable=True)  # AI-generated summary
    
    # URLs and Access
    url = Column(String, nullable=True)
    pdf_url = Column(String, nullable=True)
    is_open_access = Column(Boolean, default=False)
    
    # Medical Context
    medical_specialties = Column(Text, nullable=True)  # JSON string
    conditions_covered = Column(Text, nullable=True)  # JSON string
    icd_10_codes = Column(Text, nullable=True)  # JSON string
    
    # Relationships
    diagnosis_id = Column(UUID(as_uuid=True), ForeignKey("diagnoses.id"))
    diagnosis = relationship("Diagnosis", back_populates="evidence_references")
    
    # Quality Metrics
    citation_count = Column(String, nullable=True)
    impact_factor = Column(Float, nullable=True)
    peer_reviewed = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<EvidenceReference {self.title[:50]}...>"
