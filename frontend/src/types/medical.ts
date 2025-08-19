// Medical domain types for AuraMD application

export interface Patient {
  id: string
  firstName: string
  lastName: string
  dateOfBirth: string
  gender: 'male' | 'female' | 'other' | 'prefer_not_to_say'
  email?: string
  phone?: string
  address?: string
  medicalRecordNumber?: string
  insuranceNumber?: string
  bloodType?: string
  allergies?: string
  chronicConditions?: string
  currentMedications?: string
  emergencyContact?: {
    name: string
    phone: string
    relationship: string
  }
  consentForAIAnalysis: boolean
  dataSharingConsent: boolean
  isActive: boolean
  createdAt: string
  updatedAt: string
}

export interface Symptom {
  id: string
  name: string
  description?: string
  category?: string
  severity: 'mild' | 'moderate' | 'severe' | 'critical'
  duration: 'acute' | 'subacute' | 'chronic'
  onset?: string
  severityScore?: number
  frequency?: string
  triggers?: string
  relievingFactors?: string
  associatedSymptoms?: string
  bodyLocation?: string
  laterality?: 'left' | 'right' | 'bilateral'
  icd10Codes?: string[]
  snomedCodes?: string[]
  aiConfidence?: number
  createdAt: string
  updatedAt: string
}

export interface Diagnosis {
  id: string
  conditionName: string
  icd10Code?: string
  snomedCode?: string
  description?: string
  confidenceScore: number
  confidenceLevel: 'low' | 'moderate' | 'high' | 'very_high'
  aiReasoning: string
  differentialRank: number
  probabilityPercentage?: number
  supportingSymptoms?: string[]
  contradictingFactors?: string[]
  requiredTests?: string[]
  treatmentUrgency?: 'immediate' | 'urgent' | 'routine'
  treatmentOptions?: string[]
  prognosis?: string
  physicianApproved: boolean
  physicianNotes?: string
  createdAt: string
  updatedAt: string
}

export interface DiagnosisSession {
  id: string
  patientId: string
  userId: string
  sessionName?: string
  chiefComplaint: string
  status: 'pending' | 'in_progress' | 'completed' | 'reviewed' | 'cancelled'
  symptoms: Symptom[]
  diagnoses: Diagnosis[]
  aiSummary?: string
  riskFactors?: string[]
  recommendedTests?: string[]
  urgencyLevel?: 'low' | 'moderate' | 'high' | 'emergency'
  clinicalNotes?: string
  physicianAssessment?: string
  treatmentPlan?: string
  createdAt: string
  updatedAt: string
  completedAt?: string
}

export interface MedicalHistory {
  id: string
  patientId: string
  recordType: 'diagnosis' | 'procedure' | 'medication' | 'allergy' | 'immunization' | 'lab_result' | 'imaging' | 'vital_signs'
  title: string
  description?: string
  status: 'active' | 'inactive' | 'resolved' | 'chronic'
  icd10Code?: string
  snomedCode?: string
  cptCode?: string
  onsetDate?: string
  resolutionDate?: string
  recordedDate: string
  severity?: 'mild' | 'moderate' | 'severe'
  providerName?: string
  facilityName?: string
  dosage?: string
  frequency?: string
  route?: string
  resultValue?: string
  resultUnit?: string
  referenceRange?: string
  abnormalFlag?: boolean
  notes?: string
  externalId?: string
  sourceSystem?: string
  createdAt: string
  updatedAt: string
}

export interface EvidenceReference {
  id: string
  title: string
  authors?: string[]
  journal?: string
  publicationDate?: string
  doi?: string
  pubmedId?: string
  evidenceType: 'clinical_study' | 'systematic_review' | 'meta_analysis' | 'clinical_guideline' | 'case_study' | 'textbook' | 'medical_database'
  evidenceQuality: 'high' | 'moderate' | 'low' | 'very_low'
  abstract?: string
  keyFindings?: string[]
  methodology?: string
  sampleSize?: string
  relevanceScore?: number
  aiSummary?: string
  url?: string
  pdfUrl?: string
  isOpenAccess: boolean
  medicalSpecialties?: string[]
  conditionsCovered?: string[]
  icd10Codes?: string[]
  citationCount?: string
  impactFactor?: number
  peerReviewed: boolean
  createdAt: string
  updatedAt: string
}

export interface VitalSigns {
  systolicBP?: number
  diastolicBP?: number
  heartRate?: number
  temperature?: number
  respiratoryRate?: number
  oxygenSaturation?: number
  weight?: number
  height?: number
  bmi?: number
  recordedAt: string
}

export interface AIAnalysisRequest {
  patientId: string
  chiefComplaint: string
  symptoms: Omit<Symptom, 'id' | 'createdAt' | 'updatedAt'>[]
  medicalHistory?: string
  vitalSigns?: VitalSigns
  additionalContext?: {
    timeOfDay?: string
    season?: string
    geographicLocation?: string
    recentTravel?: string
    exposures?: string[]
  }
}

export interface AIAnalysisResponse {
  sessionId: string
  differentialDiagnoses: {
    conditionName: string
    confidenceScore: number
    aiReasoning: string
    icd10Code?: string
    differentialRank: number
    supportingEvidence?: string[]
    contradictingFactors?: string[]
  }[]
  recommendedTests: string[]
  urgencyLevel: 'routine' | 'moderate' | 'urgent' | 'emergency'
  clinicalReasoning: string
  redFlags: string[]
  specialistReferrals?: string[]
  aiSummary: string
  confidenceMetrics: {
    overallConfidence: number
    consensusScore: number
    uncertaintyFactors: string[]
  }
  processingTime: number
  modelsUsed: string[]
}

export interface MedicalSpecialty {
  code: string
  name: string
  description: string
}

export interface ClinicalGuideline {
  id: string
  title: string
  organization: string
  version: string
  lastUpdated: string
  conditions: string[]
  recommendations: {
    level: 'A' | 'B' | 'C' | 'D'
    text: string
    evidence: string
  }[]
  url?: string
}

// Form types for components
export interface SymptomFormData {
  name: string
  description?: string
  severity: 'mild' | 'moderate' | 'severe' | 'critical'
  duration: 'acute' | 'subacute' | 'chronic'
  bodyLocation?: string
  associatedSymptoms?: string
  triggers?: string
  relievingFactors?: string
}

export interface DiagnosisFormData {
  patientId: string
  chiefComplaint: string
  symptoms: SymptomFormData[]
  medicalHistory?: string
}

// API response types
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

export interface DiagnosisSessionSummary {
  id: string
  patientName: string
  chiefComplaint: string
  status: string
  urgencyLevel?: string
  primaryDiagnosis?: string
  confidenceScore?: number
  createdAt: string
  updatedAt: string
}

// WebSocket message types
export interface WebSocketMessage {
  type: 'diagnosis_update' | 'ai_analysis_progress' | 'consultation_invite' | 'connection_established'
  data?: any
  sessionId?: string
  userId?: string
  timestamp: number
}

export interface AIAnalysisProgress {
  stage: 'initializing' | 'analyzing_symptoms' | 'generating_diagnoses' | 'retrieving_evidence' | 'finalizing'
  progress: number // 0-100
  message: string
  estimatedTimeRemaining?: number
}
