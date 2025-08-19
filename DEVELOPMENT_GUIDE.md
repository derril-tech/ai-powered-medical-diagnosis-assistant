# 🏥 AuraMD Development Guide

## 📋 Quick Reference for Claude Code

### **Project Structure Overview**
```
auramd/
├── frontend/           # Next.js 14 + TypeScript + Tailwind
├── backend/           # FastAPI + SQLAlchemy + PostgreSQL
├── CLAUDE_INSTRUCTIONS.md    # ⭐ READ THIS FIRST
├── DEVELOPMENT_GUIDE.md     # This file
└── README.md          # Comprehensive documentation
```

### **🎯 Key Development Patterns**

#### **Medical Data Flow**
```
Patient → Symptoms → AI Analysis → Diagnoses → Evidence → Clinical Decision
```

#### **AI Integration Pattern**
```python
# Always use dual AI validation
gpt4_result = await ai_service._get_gpt4_analysis(prompt)
claude_result = await ai_service._get_claude_analysis(prompt)
combined = ai_service._combine_ai_analyses(gpt4_result, claude_result)
```

#### **Frontend Component Pattern**
```tsx
// Medical components use specific styling classes
<div className="medical-card">
  <div className="diagnosis-confidence-high">94% Confidence</div>
  <button className="medical-button">Analyze Symptoms</button>
</div>
```

### **🔧 Common Development Tasks**

#### **1. Adding New Medical Endpoints**
```python
# backend/app/api/v1/endpoints/new_endpoint.py
from app.core.security import get_current_active_user
from app.models.patient import Patient

@router.post("/new-feature")
async def new_medical_feature(
    data: NewFeatureSchema,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Always validate medical data
    validation_errors = MedicalValidators.validate_feature_data(data)
    if validation_errors:
        raise HTTPException(400, detail=validation_errors)
    
    # Process with AI if needed
    ai_result = await ai_service.analyze_feature(data)
    
    return {"result": ai_result}
```

#### **2. Creating Medical UI Components**
```tsx
// frontend/src/components/medical/NewComponent.tsx
import { motion } from 'framer-motion'
import { useAuth } from '@/hooks/useAuth'

export function MedicalComponent({ patientId }: { patientId: string }) {
  const { user } = useAuth()
  
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="medical-card p-6"
    >
      <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
        Medical Feature
      </h3>
      {/* Medical content */}
    </motion.div>
  )
}
```

#### **3. Adding AI Analysis Features**
```python
# backend/app/services/ai_service.py
async def new_ai_analysis(self, medical_data):
    system_prompt = MedicalAIPrompts.get_system_prompt()
    user_prompt = MedicalAIPrompts.build_analysis_prompt(medical_data)
    
    # Get dual AI analysis
    gpt4_response = await self._get_gpt4_analysis(system_prompt, user_prompt)
    claude_response = await self._get_claude_analysis(system_prompt, user_prompt)
    
    # Combine and validate
    result = self._combine_ai_analyses(gpt4_response, claude_response)
    validation_errors = MedicalAIPrompts.validate_ai_response(result)
    
    if validation_errors:
        return self._get_fallback_analysis()
    
    return result
```

### **🏥 Medical Domain Guidelines**

#### **Required Medical Validations**
- Patient age: 0-150 years
- Confidence scores: 0.0-1.0
- ICD-10 codes: Valid format (A00-Z99)
- Vital signs: Within reasonable ranges
- Medical license: Valid format for region

#### **Urgency Levels**
- `routine`: Standard follow-up
- `moderate`: Within 24-48 hours
- `urgent`: Within hours
- `emergency`: Immediate attention

#### **Confidence Levels**
- `very_high`: 0.9-1.0 (Classic presentation)
- `high`: 0.8-0.9 (Typical features)
- `moderate`: 0.6-0.8 (Some uncertainty)
- `low`: 0.0-0.6 (Differential consideration)

### **🎨 UI/UX Patterns**

#### **Medical Color Coding**
```css
/* Confidence levels */
.diagnosis-confidence-high    /* Green - High confidence */
.diagnosis-confidence-moderate /* Yellow - Moderate confidence */
.diagnosis-confidence-low     /* Red - Low confidence */

/* Urgency levels */
.urgency-emergency   /* Red - Immediate */
.urgency-urgent      /* Orange - Hours */
.urgency-moderate    /* Yellow - 24-48h */
.urgency-routine     /* Green - Standard */
```

#### **Accessibility Requirements**
- WCAG 2.1 AA compliance
- Keyboard navigation support
- Screen reader compatibility
- High contrast ratios
- Focus indicators

### **🔒 Security Patterns**

#### **Authentication Check**
```python
current_user: User = Depends(get_current_active_user)
```

#### **Role-based Access**
```python
@router.get("/admin-only")
async def admin_endpoint(
    current_user: User = Depends(check_permissions("admin"))
):
    pass
```

#### **Data Validation**
```python
# Always validate medical data
validation_errors = ClinicalDataValidator.validate_diagnosis_session(data)
if validation_errors:
    raise HTTPException(400, detail=validation_errors)
```

### **📊 Database Patterns**

#### **Medical Record Creation**
```python
# Always include audit fields
medical_record = MedicalHistory(
    patient_id=patient_id,
    record_type=RecordType.DIAGNOSIS,
    title=diagnosis_name,
    recorded_date=datetime.utcnow().date(),
    provider_name=current_user.full_name
)
db.add(medical_record)
db.commit()
```

#### **AI Analysis Storage**
```python
# Store AI results with metadata
diagnosis = Diagnosis(
    diagnosis_session_id=session.id,
    condition_name=ai_result["condition_name"],
    confidence_score=ai_result["confidence_score"],
    ai_reasoning=ai_result["reasoning"],
    differential_rank=rank
)
```

### **🧪 Testing Patterns**

#### **Medical Data Testing**
```python
def test_diagnosis_analysis():
    # Test with valid medical data
    symptoms = [
        {"name": "chest pain", "severity": "severe", "duration": "acute"}
    ]
    result = ai_service.analyze_symptoms(symptoms, patient)
    
    assert result["urgency_level"] in ["routine", "moderate", "urgent", "emergency"]
    assert all(0.0 <= d["confidence_score"] <= 1.0 for d in result["diagnoses"])
```

#### **API Testing**
```python
def test_diagnosis_endpoint(client, auth_headers):
    response = client.post(
        "/api/v1/diagnosis/analyze",
        json=valid_diagnosis_request,
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "differential_diagnoses" in response.json()
```

### **🚀 Deployment Checklist**

#### **Environment Variables**
- ✅ `OPENAI_API_KEY` - GPT-4 integration
- ✅ `ANTHROPIC_API_KEY` - Claude integration  
- ✅ `DATABASE_URL` - PostgreSQL connection
- ✅ `REDIS_URL` - Cache connection
- ✅ `JWT_SECRET_KEY` - Authentication

#### **Health Checks**
- ✅ `/health` endpoint responding
- ✅ Database connectivity
- ✅ Redis connectivity  
- ✅ AI service availability
- ✅ WebSocket functionality

### **🔍 Debugging Tips**

#### **Common Issues**
1. **AI Service Timeout**: Check API keys and network
2. **Database Connection**: Verify DATABASE_URL format
3. **Authentication Errors**: Check JWT_SECRET_KEY
4. **WebSocket Issues**: Verify CORS settings

#### **Logging Patterns**
```python
import structlog
logger = structlog.get_logger()

# Medical action logging
logger.info(
    "diagnosis_analysis_completed",
    user_id=current_user.id,
    patient_id=patient_id,
    session_id=session.id,
    confidence_score=max_confidence
)
```

### **📚 Key Files Reference**

#### **Backend Core**
- `backend/app/main.py` - FastAPI app entry
- `backend/app/services/ai_service.py` - AI integration
- `backend/app/utils/medical_validators.py` - Data validation
- `backend/app/utils/ai_prompts.py` - AI prompt templates

#### **Frontend Core**
- `frontend/src/app/page.tsx` - Landing page
- `frontend/src/app/dashboard/page.tsx` - Main dashboard
- `frontend/src/components/diagnosis/SymptomAnalyzer.tsx` - Core feature
- `frontend/src/types/medical.ts` - Medical type definitions

#### **Configuration**
- `env.example` - All environment variables
- `docker-compose.yml` - Development environment
- `vercel.json` - Frontend deployment
- `backend/render.yaml` - Backend deployment

---

## 💡 Remember

1. **Medical Safety First**: Always validate medical data and provide disclaimers
2. **Dual AI Validation**: Use both OpenAI and Claude for critical medical decisions
3. **Security**: Protect patient data with encryption and access controls
4. **Accessibility**: Ensure healthcare professionals can use the app effectively
5. **Documentation**: Update docs when adding medical features

**This is a healthcare application - code quality and reliability save lives! 🏥**
