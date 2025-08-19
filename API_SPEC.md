# 🏥 AuraMD API Specification

## 📋 Overview
Complete API specification for AuraMD, an AI-powered medical diagnosis assistant. This RESTful API provides endpoints for healthcare professionals to manage patients, analyze symptoms, and generate AI-powered differential diagnoses.

**Base URL**: `https://api.auramd.com/api/v1`  
**Development URL**: `http://localhost:8000/api/v1`

## 🔐 Authentication

### Authentication Method
- **Type**: Bearer Token (JWT)
- **Header**: `Authorization: Bearer <access_token>`
- **Token Expiry**: 30 minutes (configurable)
- **Refresh Token**: 7 days (configurable)

### User Roles
- `doctor` - Full access to all medical features
- `nurse` - Patient management and symptom analysis
- `specialist` - Specialized diagnosis and consultation
- `admin` - System administration and user management

## 📚 API Endpoints

### 🔑 Authentication Endpoints

#### POST `/auth/register`
Register a new healthcare professional.

**Request Body:**
```json
{
  "email": "doctor@hospital.com",
  "password": "securePassword123",
  "full_name": "Dr. Jane Smith",
  "role": "doctor",
  "medical_license": "MD123456",
  "specialization": "cardiology",
  "hospital_affiliation": "General Hospital"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "email": "doctor@hospital.com",
  "full_name": "Dr. Jane Smith",
  "role": "doctor",
  "medical_license": "MD123456",
  "specialization": "cardiology",
  "hospital_affiliation": "General Hospital",
  "is_active": true,
  "is_verified": false
}
```

**Status Codes:**
- `201` - User created successfully
- `400` - Invalid request data
- `409` - Email already registered

#### POST `/auth/login`
Authenticate healthcare professional and return JWT tokens.

**Request Body (Form Data):**
```
username: doctor@hospital.com
password: securePassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Status Codes:**
- `200` - Login successful
- `401` - Invalid credentials
- `400` - Inactive user account

#### POST `/auth/refresh`
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET `/auth/me`
Get current authenticated user information.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": "uuid-string",
  "email": "doctor@hospital.com",
  "full_name": "Dr. Jane Smith",
  "role": "doctor",
  "medical_license": "MD123456",
  "specialization": "cardiology",
  "hospital_affiliation": "General Hospital",
  "is_active": true,
  "is_verified": true
}
```

### 👥 Patient Management Endpoints

#### GET `/patients/`
Get list of patients with pagination.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 20)

**Response:**
```json
[
  {
    "id": "uuid-string",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1980-01-15",
    "gender": "male",
    "email": "john.doe@email.com",
    "phone": "+1234567890",
    "medical_record_number": "MR001234",
    "blood_type": "O+",
    "allergies": "Penicillin, Shellfish",
    "chronic_conditions": "Hypertension, Type 2 Diabetes",
    "current_medications": "Metformin 500mg, Lisinopril 10mg",
    "consent_for_ai_analysis": true,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### GET `/patients/{patient_id}`
Get specific patient by ID.

**Headers:** `Authorization: Bearer <token>`

**Path Parameters:**
- `patient_id` (string): Patient UUID

**Response:** Same as single patient object above

**Status Codes:**
- `200` - Patient found
- `404` - Patient not found
- `403` - Access denied

### 🩺 Diagnosis Endpoints

#### POST `/diagnosis/analyze`
Analyze patient symptoms and generate AI-powered differential diagnoses.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "patient_id": "uuid-string",
  "chief_complaint": "Chest pain and shortness of breath for 2 hours",
  "symptoms": [
    {
      "name": "chest pain",
      "description": "Sharp, stabbing pain in center of chest",
      "severity": "severe",
      "duration": "acute",
      "body_location": "chest",
      "associated_symptoms": "shortness of breath, sweating",
      "triggers": "started at rest",
      "relieving_factors": "none identified"
    },
    {
      "name": "shortness of breath",
      "description": "Difficulty breathing, feeling of air hunger",
      "severity": "moderate",
      "duration": "acute",
      "body_location": "chest",
      "associated_symptoms": "chest pain",
      "triggers": "worsens with exertion",
      "relieving_factors": "sitting upright"
    }
  ],
  "medical_history": "Hypertension, smoking history, family history of CAD"
}
```

**Response:**
```json
{
  "session_id": "uuid-string",
  "differential_diagnoses": [
    {
      "condition_name": "Acute Myocardial Infarction",
      "confidence_score": 0.87,
      "ai_reasoning": "Classic presentation of chest pain with associated symptoms, risk factors present including hypertension and smoking history. ECG and cardiac enzymes needed for confirmation.",
      "icd_10_code": "I21.9",
      "differential_rank": 1
    },
    {
      "condition_name": "Unstable Angina",
      "confidence_score": 0.73,
      "ai_reasoning": "Chest pain pattern consistent with acute coronary syndrome, but biomarkers needed to differentiate from MI.",
      "icd_10_code": "I20.0",
      "differential_rank": 2
    },
    {
      "condition_name": "Pulmonary Embolism",
      "confidence_score": 0.65,
      "ai_reasoning": "Shortness of breath and chest pain could indicate PE. D-dimer and CT-PA recommended for evaluation.",
      "icd_10_code": "I26.9",
      "differential_rank": 3
    }
  ],
  "recommended_tests": [
    "ECG (12-lead)",
    "Cardiac enzymes (Troponin I/T, CK-MB)",
    "Complete Blood Count",
    "Basic Metabolic Panel",
    "D-dimer",
    "Chest X-ray",
    "CT Pulmonary Angiogram (if PE suspected)"
  ],
  "urgency_level": "emergency",
  "clinical_reasoning": "Patient presents with acute chest pain and dyspnea with cardiovascular risk factors. Given the symptom constellation, severity, and risk profile, immediate cardiac evaluation is warranted to rule out acute coronary syndrome. The combination of chest pain, shortness of breath, and risk factors (hypertension, smoking) creates a high-risk scenario requiring emergency assessment.",
  "red_flags": [
    "Severe acute chest pain",
    "Shortness of breath at rest",
    "Multiple cardiovascular risk factors",
    "Potential acute coronary syndrome"
  ],
  "ai_summary": "High-risk presentation requiring immediate evaluation for acute coronary syndrome. Multiple differential diagnoses possible, with MI being most concerning given presentation and risk factors."
}
```

**Status Codes:**
- `200` - Analysis completed successfully
- `400` - Invalid request data
- `404` - Patient not found
- `500` - AI analysis failed

#### GET `/diagnosis/sessions`
Get diagnosis sessions for current user.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 20)

**Response:**
```json
[
  {
    "id": "uuid-string",
    "patient_id": "uuid-string",
    "user_id": "uuid-string",
    "chief_complaint": "Chest pain and shortness of breath",
    "status": "completed",
    "urgency_level": "emergency",
    "ai_summary": "High-risk cardiac presentation requiring immediate evaluation",
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

#### GET `/diagnosis/sessions/{session_id}`
Get specific diagnosis session details.

**Headers:** `Authorization: Bearer <token>`

**Path Parameters:**
- `session_id` (string): Session UUID

**Response:** Same as diagnosis session object with full details including symptoms and diagnoses

### 🔬 Symptom Management Endpoints

#### GET `/symptoms/`
Get symptoms for a specific diagnosis session.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `session_id` (string, optional): Filter by diagnosis session
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 20)

**Response:**
```json
[
  {
    "id": "uuid-string",
    "name": "chest pain",
    "description": "Sharp, stabbing pain in center of chest",
    "severity": "severe",
    "duration": "acute",
    "body_location": "chest",
    "associated_symptoms": "shortness of breath, sweating",
    "triggers": "started at rest",
    "relieving_factors": "none identified",
    "ai_confidence": 0.92,
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

### 📋 Medical History Endpoints

#### GET `/medical-history/`
Get medical history records for a patient.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `patient_id` (string, optional): Filter by patient ID
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 20)

**Response:**
```json
[
  {
    "id": "uuid-string",
    "patient_id": "uuid-string",
    "record_type": "diagnosis",
    "title": "Hypertension",
    "description": "Essential hypertension, well-controlled",
    "status": "active",
    "icd_10_code": "I10",
    "onset_date": "2020-01-01",
    "recorded_date": "2024-01-01",
    "severity": "moderate",
    "provider_name": "Dr. Smith",
    "notes": "Patient responding well to ACE inhibitor therapy",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

### 👨‍⚕️ User Management Endpoints

#### GET `/users/me`
Get current user profile (same as `/auth/me`).

**Headers:** `Authorization: Bearer <token>`

**Response:** Same as auth/me response

## 🌐 WebSocket Endpoints

### WebSocket Connection: `/ws/{user_id}`
Real-time communication for medical consultations and AI analysis progress.

**Connection URL:** `ws://localhost:8000/ws/{user_id}`  
**Authentication:** Include JWT token in connection headers

**Message Types:**

#### Connection Established
```json
{
  "type": "connection_established",
  "message": "Connected to AuraMD real-time services",
  "user_id": "uuid-string",
  "timestamp": 1640995200
}
```

#### AI Analysis Progress
```json
{
  "type": "ai_analysis_progress",
  "progress": {
    "stage": "analyzing_symptoms",
    "progress": 45,
    "message": "Analyzing symptom patterns with medical AI...",
    "estimated_time_remaining": 30
  },
  "timestamp": 1640995200
}
```

#### Diagnosis Update
```json
{
  "type": "diagnosis_update",
  "data": {
    "session_id": "uuid-string",
    "status": "completed",
    "primary_diagnosis": "Acute Myocardial Infarction",
    "confidence_score": 0.87
  },
  "session_id": "uuid-string",
  "timestamp": 1640995200
}
```

#### Consultation Invite
```json
{
  "type": "consultation_invite",
  "from_user_id": "uuid-string",
  "session_id": "uuid-string",
  "message": "Dr. Smith is requesting consultation on urgent case",
  "timestamp": 1640995200
}
```

## 🔧 Health and System Endpoints

#### GET `/health`
Application health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "AuraMD API",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2024-01-01T10:00:00Z"
}
```

#### GET `/`
API root endpoint with basic information.

**Response:**
```json
{
  "message": "Welcome to AuraMD - AI-Powered Medical Diagnosis Assistant",
  "version": "1.0.0",
  "docs": "/api/v1/docs",
  "health": "/health"
}
```

## 📊 Data Models

### User Model
```typescript
interface User {
  id: string
  email: string
  full_name: string
  role: 'doctor' | 'nurse' | 'admin' | 'specialist'
  medical_license?: string
  specialization?: string
  hospital_affiliation?: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at: string
  last_login?: string
}
```

### Patient Model
```typescript
interface Patient {
  id: string
  first_name: string
  last_name: string
  date_of_birth: string
  gender: 'male' | 'female' | 'other' | 'prefer_not_to_say'
  email?: string
  phone?: string
  address?: string
  medical_record_number?: string
  insurance_number?: string
  blood_type?: string
  allergies?: string
  chronic_conditions?: string
  current_medications?: string
  emergency_contact?: {
    name: string
    phone: string
    relationship: string
  }
  consent_for_ai_analysis: boolean
  data_sharing_consent: boolean
  is_active: boolean
  created_at: string
  updated_at: string
}
```

### Symptom Model
```typescript
interface Symptom {
  id: string
  name: string
  description?: string
  severity: 'mild' | 'moderate' | 'severe' | 'critical'
  duration: 'acute' | 'subacute' | 'chronic'
  body_location?: string
  associated_symptoms?: string
  triggers?: string
  relieving_factors?: string
  ai_confidence?: number
  created_at: string
  updated_at: string
}
```

### Diagnosis Model
```typescript
interface Diagnosis {
  id: string
  condition_name: string
  icd_10_code?: string
  description?: string
  confidence_score: number
  confidence_level: 'low' | 'moderate' | 'high' | 'very_high'
  ai_reasoning: string
  differential_rank: number
  probability_percentage?: number
  supporting_symptoms?: string[]
  required_tests?: string[]
  treatment_urgency?: 'immediate' | 'urgent' | 'routine'
  physician_approved: boolean
  physician_notes?: string
  created_at: string
  updated_at: string
}
```

## ⚠️ Error Handling

### Standard Error Response
```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### Common Error Codes
- `INVALID_CREDENTIALS` - Authentication failed
- `ACCESS_DENIED` - Insufficient permissions
- `PATIENT_NOT_FOUND` - Patient ID not found
- `INVALID_MEDICAL_DATA` - Medical data validation failed
- `AI_SERVICE_UNAVAILABLE` - AI analysis service down
- `RATE_LIMIT_EXCEEDED` - Too many requests

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Internal Server Error
- `503` - Service Unavailable

## 🔒 Security Considerations

### Authentication
- JWT tokens with 30-minute expiry
- Refresh tokens with 7-day expiry
- Secure token storage and transmission
- Role-based access control

### Data Protection
- HIPAA-compliant data handling
- Encryption at rest and in transit
- Patient consent validation
- Audit logging for all medical data access

### Rate Limiting
- 100 requests per minute per user (configurable)
- Separate limits for AI analysis endpoints
- WebSocket connection limits

### Input Validation
- Medical data validation using clinical standards
- ICD-10 code validation
- Confidence score validation (0.0-1.0)
- Required field validation

## 📈 Performance

### Response Times
- Authentication: < 200ms
- Patient queries: < 300ms
- AI analysis: < 2 seconds
- WebSocket messages: < 50ms

### Scalability
- Supports 10,000+ concurrent users
- Auto-scaling backend infrastructure
- Database connection pooling
- Redis caching for performance

## 🧪 Testing

### API Testing
Use the interactive API documentation at `/api/v1/docs` when running the development server.

### Example cURL Commands

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=doctor@hospital.com&password=securePassword123"
```

**Get Current User:**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Analyze Symptoms:**
```bash
curl -X POST "http://localhost:8000/api/v1/diagnosis/analyze" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "uuid-string",
    "chief_complaint": "Chest pain and shortness of breath",
    "symptoms": [
      {
        "name": "chest pain",
        "severity": "severe",
        "duration": "acute",
        "description": "Sharp pain in center of chest"
      }
    ]
  }'
```

This API specification provides comprehensive documentation for all endpoints in the AuraMD medical diagnosis assistant, enabling healthcare professionals to integrate AI-powered diagnostic support into their clinical workflows.
