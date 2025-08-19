# 🤖 Instructions for Claude Code

## 📋 Project Overview
This is **AuraMD**, a production-ready AI-powered medical diagnosis assistant for healthcare professionals. The application combines Next.js 14 frontend with FastAPI backend and dual AI integration (OpenAI + Anthropic Claude) for intelligent medical diagnosis support.

## 🎯 Key Context for Claude Code

### **Application Purpose**
- **Target Users**: Healthcare professionals (doctors, nurses, specialists)
- **Core Function**: AI-assisted medical diagnosis and clinical decision support
- **Compliance**: HIPAA-compliant with healthcare-grade security
- **Scale**: Designed for 10,000+ concurrent users in production

### **Architecture Overview**
```
Frontend (Next.js 14) ↔ Backend (FastAPI) ↔ AI Services (OpenAI + Claude)
                                ↕
                        PostgreSQL + pgvector + Redis
```

## 🔧 Development Guidelines

### **When Adding Features:**
1. **Medical Context**: Always consider healthcare compliance and patient safety
2. **Security First**: All medical data must be encrypted and access-controlled
3. **AI Integration**: Use both OpenAI and Claude for cross-validation of medical insights
4. **Real-time Updates**: Leverage WebSocket connections for live collaboration
5. **Error Handling**: Implement comprehensive error handling - lives depend on reliability

### **Code Patterns to Follow:**

#### **Frontend (Next.js 14)**
- Use App Router with TypeScript
- Follow medical UI patterns (see `globals.css` for medical-specific classes)
- Implement proper loading states for AI analysis
- Use React Query for data fetching with error boundaries
- Maintain accessibility standards (WCAG 2.1 AA)

#### **Backend (FastAPI)**
- Use SQLAlchemy 2.0 async patterns
- Implement proper JWT authentication checks
- Use dependency injection for database sessions
- Follow medical data validation patterns
- Implement comprehensive logging for audit trails

#### **AI Integration**
- Always combine OpenAI and Claude responses for accuracy
- Implement confidence scoring for all AI suggestions
- Provide medical evidence references for all diagnoses
- Use structured prompts with medical context
- Implement fallback responses when AI services are unavailable

## 📁 Key Files to Understand

### **Backend Core Files:**
- `backend/app/main.py` - FastAPI application entry point
- `backend/app/core/config.py` - All configuration settings
- `backend/app/services/ai_service.py` - Main AI integration logic
- `backend/app/models/` - Database models for medical data
- `backend/app/api/v1/endpoints/diagnosis.py` - Core diagnosis API

### **Frontend Core Files:**
- `frontend/src/app/page.tsx` - Landing page with medical hero section
- `frontend/src/contexts/AuthContext.tsx` - Authentication state management
- `frontend/src/lib/api/client.tsx` - API client with token management
- `frontend/src/app/globals.css` - Medical-themed styling system

### **Configuration Files:**
- `env.example` - All environment variables with descriptions
- `docker-compose.yml` - Complete development environment
- `vercel.json` - Frontend deployment configuration
- `backend/render.yaml` - Backend deployment configuration

## 🚀 Common Development Tasks

### **Adding New Medical Features:**
1. Create database model in `backend/app/models/`
2. Add Pydantic schemas in `backend/app/schemas/`
3. Implement API endpoints in `backend/app/api/v1/endpoints/`
4. Create frontend components with medical styling
5. Add AI integration if needed in `ai_service.py`
6. Update WebSocket handlers for real-time features

### **AI Enhancement Patterns:**
```python
# Always use both AI models for medical accuracy
gpt4_response = await self._get_gpt4_analysis(prompt)
claude_response = await self._get_claude_analysis(prompt)
combined_result = self._combine_ai_analyses(gpt4_response, claude_response)
```

### **Medical UI Components:**
```tsx
// Use medical-specific CSS classes
<div className="medical-card">
  <div className="diagnosis-confidence-high">High Confidence</div>
  <button className="medical-button">Analyze Symptoms</button>
</div>
```

## 🔍 Testing & Quality Assurance

### **Critical Testing Areas:**
- AI diagnosis accuracy and consistency
- Medical data security and encryption
- Real-time collaboration features
- API authentication and authorization
- Database performance with medical records
- WebSocket connection stability

### **Performance Requirements:**
- AI analysis: < 2 seconds response time
- API endpoints: < 500ms response time
- Frontend loading: < 1 second initial load
- Database queries: Optimized with proper indexing

## 🏥 Medical Domain Knowledge

### **Key Medical Concepts:**
- **Differential Diagnosis**: List of potential conditions ranked by likelihood
- **ICD-10 Codes**: International medical condition classification
- **SNOMED CT**: Medical terminology standard
- **Confidence Scoring**: AI certainty levels (0.0-1.0)
- **Clinical Decision Support**: AI recommendations for healthcare professionals

### **Medical Data Hierarchy:**
```
Patient → Medical History → Diagnosis Session → Symptoms → AI Analysis → Diagnoses → Evidence References
```

## 🛠️ Development Environment Setup

### **Quick Start Commands:**
```bash
# Install all dependencies
npm install

# Start development environment
npm run dev

# Run with Docker
docker-compose up -d

# Run tests
npm run test
```

### **Environment Variables Required:**
- `OPENAI_API_KEY` - For GPT-4 integration
- `ANTHROPIC_API_KEY` - For Claude integration
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis cache connection
- `JWT_SECRET_KEY` - Authentication security

## 🚨 Important Considerations

### **Medical Compliance:**
- Never store plain-text medical data
- Always validate user permissions before data access
- Implement comprehensive audit logging
- Follow HIPAA guidelines for data handling

### **AI Safety:**
- Always provide disclaimers that AI suggestions need medical validation
- Implement confidence thresholds for diagnosis suggestions
- Provide medical evidence sources for all AI recommendations
- Include fallback responses when AI services fail

### **Security Requirements:**
- JWT tokens with refresh mechanism
- Role-based access control (Doctor, Nurse, Specialist, Admin)
- API rate limiting and request validation
- Encrypted data transmission (HTTPS/WSS)

## 📚 Additional Resources

### **Medical AI Resources:**
- Medical terminology databases (ICD-10, SNOMED CT)
- Clinical guidelines and research papers
- Medical literature APIs for evidence retrieval

### **Technical Documentation:**
- FastAPI docs: `/api/v1/docs` (when running locally)
- Database schema: See models in `backend/app/models/`
- API client: `frontend/src/lib/api/`

---

## 💡 Tips for Claude Code

1. **Context Matters**: This is a medical application - prioritize accuracy and safety
2. **Follow Patterns**: Use existing code patterns for consistency
3. **Test Thoroughly**: Medical applications require extensive testing
4. **Document Changes**: Update relevant documentation when adding features
5. **Security First**: Always consider security implications of changes

**Remember: This application supports healthcare professionals making life-critical decisions. Code quality and reliability are paramount.**
