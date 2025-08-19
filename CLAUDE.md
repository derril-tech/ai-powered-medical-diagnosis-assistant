# 🤖 Claude Development Guide for AuraMD

## 🎯 Quick Start for Claude

**You are working with AuraMD** - a production-ready, AI-powered medical diagnosis assistant for healthcare professionals. This is a **healthcare application where code quality and reliability save lives**.

### **🏥 What is AuraMD?**
- **Purpose**: AI-powered medical diagnosis assistant for doctors, nurses, and specialists
- **Core Feature**: Analyze patient symptoms → Generate differential diagnoses → Provide evidence-based recommendations
- **AI Integration**: Dual validation using OpenAI GPT-4 + Anthropic Claude for medical accuracy
- **Compliance**: HIPAA-compliant, healthcare-grade security and data protection

### **📁 Project Structure**
```
auramd/
├── frontend/          # Next.js 14 + TypeScript + Tailwind (Medical UI)
├── backend/           # FastAPI + SQLAlchemy + PostgreSQL (Medical API)
├── REPO_MAP.md        # Complete file structure guide
├── API_SPEC.md        # Full API documentation
├── CLAUDE.md          # This file - your development guide
└── README.md          # Comprehensive project documentation
```

## 🚀 Essential Commands

### **Development Setup**
```bash
# Install all dependencies
npm install

# Start development servers (both frontend + backend)
npm run dev

# Start with Docker (includes PostgreSQL + Redis)
docker-compose up -d

# Database migrations
cd backend && alembic upgrade head
```

### **Key URLs (Development)**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs
- **Health Check**: http://localhost:8000/health

## 🏥 Medical Context & Domain Knowledge

### **Target Users**
- **Primary**: Healthcare professionals (doctors, nurses, specialists)
- **Use Case**: Clinical decision support and diagnostic assistance
- **Environment**: Hospitals, clinics, telemedicine platforms

### **Medical Workflow**
```
Patient Presents → Symptom Collection → AI Analysis → Differential Diagnosis → Evidence Review → Clinical Decision
```

### **Key Medical Concepts**
- **Differential Diagnosis**: Ranked list of potential conditions by likelihood
- **Confidence Scoring**: AI certainty levels (0.0-1.0) for each diagnosis
- **ICD-10 Codes**: International medical condition classification
- **Urgency Levels**: routine → moderate → urgent → emergency
- **Red Flags**: Symptoms requiring immediate medical attention

### **Medical Data Types**
- **Symptoms**: Name, severity, duration, location, associated symptoms
- **Diagnoses**: Condition name, confidence score, ICD-10 code, reasoning
- **Patient Data**: Demographics, medical history, allergies, medications
- **Clinical Notes**: Provider assessments, treatment plans, follow-up

## 🔧 Development Patterns

### **1. Medical Data Validation**
```python
# Always validate medical data
from app.utils.medical_validators import MedicalValidators

# Validate ICD-10 codes
if not MedicalValidators.validate_icd10_code("I21.9"):
    raise ValueError("Invalid ICD-10 code")

# Validate confidence scores
if not MedicalValidators.validate_confidence_score(0.87):
    raise ValueError("Confidence score must be 0.0-1.0")
```

### **2. AI Integration Pattern**
```python
# Always use dual AI validation for medical accuracy
async def analyze_symptoms(symptoms, patient):
    # Get analysis from both AI models
    gpt4_result = await ai_service._get_gpt4_analysis(prompt)
    claude_result = await ai_service._get_claude_analysis(prompt)
    
    # Combine and validate results
    combined = ai_service._combine_ai_analyses(gpt4_result, claude_result)
    
    # Ensure medical safety
    if not combined or len(combined.get('differential_diagnoses', [])) == 0:
        return ai_service._get_fallback_analysis()
    
    return combined
```

### **3. Medical UI Components**
```tsx
// Use medical-specific styling classes
<div className="medical-card p-6">
  <h3 className="text-lg font-semibold text-neutral-900 dark:text-white">
    Diagnosis Results
  </h3>
  
  {/* Confidence indicator */}
  <div className="diagnosis-confidence-high">
    94% Confidence - High
  </div>
  
  {/* Urgency indicator */}
  <span className="urgency-emergency px-2 py-1 rounded">
    EMERGENCY
  </span>
  
  <button className="medical-button">
    Save to Patient Record
  </button>
</div>
```

### **4. Authentication & Security**
```python
# Always check authentication for medical data
@router.get("/patients/{patient_id}")
async def get_patient(
    patient_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify user has access to patient data
    if not current_user.is_medical_professional:
        raise HTTPException(403, "Access denied")
    
    # Log access for audit trail
    logger.info("patient_accessed", 
                user_id=current_user.id, 
                patient_id=patient_id)
```

## 📊 Key Files & Components

### **Backend Core Files**
- `backend/app/main.py` - FastAPI app with medical endpoints
- `backend/app/services/ai_service.py` - Dual AI integration (OpenAI + Claude)
- `backend/app/models/diagnosis.py` - Medical diagnosis data models
- `backend/app/utils/medical_validators.py` - Medical data validation
- `backend/app/utils/ai_prompts.py` - Medical AI prompt templates

### **Frontend Core Components**
- `frontend/src/app/page.tsx` - Landing page with medical hero
- `frontend/src/app/dashboard/page.tsx` - Healthcare professional dashboard
- `frontend/src/components/diagnosis/SymptomAnalyzer.tsx` - Main diagnosis feature
- `frontend/src/types/medical.ts` - Complete medical type definitions
- `frontend/src/app/globals.css` - Medical-themed styling

### **Configuration Files**
- `env.example` - All environment variables (AI keys, database, etc.)
- `docker-compose.yml` - Complete development environment
- `frontend/vercel.json` - Production deployment config
- `backend/render.yaml` - Backend deployment config

## 🎨 Medical UI/UX Guidelines

### **Color Coding System**
```css
/* Confidence Levels */
.diagnosis-confidence-high     /* Green - 80-100% confidence */
.diagnosis-confidence-moderate /* Yellow - 60-80% confidence */
.diagnosis-confidence-low      /* Red - 0-60% confidence */

/* Urgency Levels */
.urgency-emergency    /* Red - Immediate attention */
.urgency-urgent       /* Orange - Within hours */
.urgency-moderate     /* Yellow - Within 24-48h */
.urgency-routine      /* Green - Standard follow-up */
```

### **Medical Component Patterns**
- **Cards**: Use `.medical-card` for all content containers
- **Buttons**: Use `.medical-button` for primary actions
- **Inputs**: Use `.medical-input` for form fields
- **Loading**: Show progress for AI analysis (can take 1-2 seconds)
- **Accessibility**: Ensure WCAG 2.1 AA compliance for healthcare environments

### **Data Display Patterns**
- **Confidence Scores**: Show as percentage with visual progress bar
- **Urgency**: Use color-coded badges with clear text
- **Diagnoses**: Rank by likelihood with supporting evidence
- **Patient Data**: Protect with role-based access controls

## 🔒 Security & Compliance

### **HIPAA Compliance Requirements**
- **Data Encryption**: All medical data encrypted at rest and in transit
- **Access Controls**: Role-based permissions (doctor, nurse, specialist, admin)
- **Audit Logging**: Log all access to patient data
- **Data Minimization**: Only collect necessary medical information
- **User Consent**: Verify patient consent for AI analysis

### **Authentication Pattern**
```typescript
// Frontend: Always check auth state
const { user, loading } = useAuth()

if (loading) return <LoadingSpinner />
if (!user) return <LoginRequired />
if (!user.is_medical_professional) return <AccessDenied />

// Proceed with medical feature
```

### **Medical Data Handling**
```python
# Backend: Always sanitize and validate medical input
medical_data = MedicalValidators.sanitize_medical_text(user_input)
validation_errors = ClinicalDataValidator.validate_diagnosis_session(data)

if validation_errors:
    raise HTTPException(400, detail=validation_errors)
```

## 🧪 Testing Medical Features

### **Critical Test Areas**
```python
def test_ai_diagnosis_accuracy():
    """Test AI diagnosis with known medical cases"""
    symptoms = [{"name": "chest pain", "severity": "severe"}]
    result = ai_service.analyze_symptoms(symptoms, patient)
    
    # Verify medical accuracy
    assert result["urgency_level"] in ["routine", "moderate", "urgent", "emergency"]
    assert all(0.0 <= d["confidence_score"] <= 1.0 for d in result["diagnoses"])
    assert len(result["differential_diagnoses"]) > 0

def test_medical_data_validation():
    """Test medical data validation"""
    assert MedicalValidators.validate_icd10_code("I21.9")  # Valid MI code
    assert not MedicalValidators.validate_icd10_code("INVALID")
    assert MedicalValidators.validate_confidence_score(0.87)
    assert not MedicalValidators.validate_confidence_score(1.5)
```

### **Frontend Testing**
```tsx
// Test medical components
test('SymptomAnalyzer displays confidence scores correctly', () => {
  render(<SymptomAnalyzer patientId="test-id" />)
  
  // Test confidence display
  expect(screen.getByText('87% Confidence')).toBeInTheDocument()
  expect(screen.getByText('High Confidence')).toHaveClass('diagnosis-confidence-high')
})
```

## 🚀 Common Development Tasks

### **Adding New Medical Endpoints**
1. **Create Model**: Add to `backend/app/models/`
2. **Add Schema**: Create Pydantic schemas in `backend/app/schemas/`
3. **Implement Endpoint**: Add to `backend/app/api/v1/endpoints/`
4. **Add Validation**: Use medical validators
5. **Update Frontend**: Create UI components with medical styling

### **Integrating New AI Features**
1. **Update Prompts**: Add templates in `backend/app/utils/ai_prompts.py`
2. **Extend AI Service**: Add methods to `backend/app/services/ai_service.py`
3. **Test AI Responses**: Validate medical accuracy
4. **Add Frontend**: Create components for AI results

### **Adding Medical UI Components**
1. **Use Medical Patterns**: Follow existing component structure
2. **Apply Medical Styling**: Use `.medical-*` CSS classes
3. **Add Accessibility**: Ensure WCAG compliance
4. **Test Responsiveness**: Verify mobile/tablet functionality

## ⚠️ Critical Considerations

### **Medical Safety**
- **Never bypass validation** - Medical data must always be validated
- **Always provide disclaimers** - AI suggestions need medical professional review
- **Implement fallbacks** - Handle AI service failures gracefully
- **Log everything** - Comprehensive audit trails for regulatory compliance

### **AI Integration Safety**
- **Dual validation required** - Always use both OpenAI and Claude
- **Confidence thresholds** - Don't show low-confidence diagnoses prominently
- **Evidence required** - Provide medical literature support
- **Human oversight** - AI is assistive, not diagnostic

### **Data Protection**
- **Encrypt sensitive data** - Patient information must be protected
- **Role-based access** - Restrict data based on user roles
- **Audit trails** - Log all data access and modifications
- **Consent verification** - Ensure patient consent for AI analysis

## 🆘 Troubleshooting

### **Common Issues**
1. **AI Service Timeout**: Check API keys in environment variables
2. **Database Connection**: Verify `DATABASE_URL` format
3. **Authentication Errors**: Check `JWT_SECRET_KEY` configuration
4. **WebSocket Issues**: Verify CORS settings and connection URLs

### **Debug Commands**
```bash
# Check backend health
curl http://localhost:8000/health

# Test AI service
python -c "from app.services.ai_service import ai_service; print('AI service loaded')"

# Check database connection
python -c "from app.core.database import engine; engine.connect()"
```

## 📚 Additional Resources

### **Medical Resources**
- **ICD-10 Codes**: https://www.who.int/classifications/icd/en/
- **SNOMED CT**: https://www.snomed.org/
- **Medical Terminology**: Use standardized medical terms
- **Clinical Guidelines**: Reference evidence-based practices

### **Development Resources**
- **API Documentation**: `/api/v1/docs` (when running locally)
- **Repository Map**: `REPO_MAP.md` - Complete file structure
- **API Specification**: `API_SPEC.md` - Full endpoint documentation
- **Development Guide**: `DEVELOPMENT_GUIDE.md` - Quick reference

---

## 💡 Remember

**This is a medical application - your code directly impacts patient care and clinical decisions. Always prioritize:**

1. **Medical Accuracy** - Validate all medical data and AI responses
2. **Patient Safety** - Implement comprehensive error handling
3. **Data Security** - Protect patient information with encryption
4. **Regulatory Compliance** - Follow HIPAA and healthcare standards
5. **Professional Standards** - Create interfaces suitable for clinical environments

**Every line of code you write has the potential to improve human health and save lives. Code responsibly!** 🏥✨
