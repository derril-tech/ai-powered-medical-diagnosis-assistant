"""
AI Service for Medical Diagnosis
Integration with OpenAI GPT-4 and Anthropic Claude for medical analysis
"""

import json
from typing import List, Dict, Any, Optional
import openai
import anthropic
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

from app.core.config import settings
from app.models.symptom import Symptom
from app.models.patient import Patient
from app.schemas.diagnosis import DiagnosisRequest, DiagnosisResponse

class MedicalAIService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        # LangChain models
        self.gpt4 = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,  # Low temperature for medical accuracy
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.claude = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            temperature=0.1,
            anthropic_api_key=settings.ANTHROPIC_API_KEY
        )

    async def analyze_symptoms(
        self, 
        symptoms: List[Symptom], 
        patient: Patient,
        medical_history: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze symptoms and generate differential diagnoses"""
        
        # Prepare symptom data
        symptom_data = []
        for symptom in symptoms:
            symptom_data.append({
                "name": symptom.name,
                "description": symptom.description,
                "severity": symptom.severity.value,
                "duration": symptom.duration.value,
                "location": symptom.body_location,
                "associated_symptoms": symptom.associated_symptoms
            })
        
        # Prepare patient context
        patient_context = {
            "age": patient.age,
            "gender": patient.gender.value,
            "medical_history": medical_history or "No significant medical history",
            "allergies": patient.allergies or "No known allergies",
            "current_medications": patient.current_medications or "No current medications"
        }
        
        # Create medical analysis prompt
        system_prompt = """You are an expert medical AI assistant specializing in differential diagnosis. 
        You help healthcare professionals by analyzing patient symptoms and providing evidence-based diagnostic suggestions.
        
        IMPORTANT GUIDELINES:
        1. Always provide differential diagnoses ranked by likelihood
        2. Include confidence scores (0.0-1.0) for each diagnosis
        3. Explain your reasoning with medical evidence
        4. Suggest appropriate diagnostic tests
        5. Indicate urgency level (routine, urgent, emergency)
        6. Never provide definitive diagnoses - only suggestions for healthcare professionals
        7. Always recommend consulting with appropriate specialists when needed
        
        Format your response as a structured JSON with the following fields:
        - differential_diagnoses: Array of diagnoses with confidence scores and reasoning
        - recommended_tests: Array of suggested diagnostic tests
        - urgency_level: String indicating urgency
        - clinical_reasoning: Detailed explanation of analysis
        - red_flags: Any concerning symptoms that require immediate attention
        """
        
        user_prompt = f"""
        Please analyze the following patient case:
        
        PATIENT INFORMATION:
        Age: {patient_context['age']} years
        Gender: {patient_context['gender']}
        Medical History: {patient_context['medical_history']}
        Allergies: {patient_context['allergies']}
        Current Medications: {patient_context['current_medications']}
        
        PRESENTING SYMPTOMS:
        {json.dumps(symptom_data, indent=2)}
        
        Please provide a comprehensive differential diagnosis analysis.
        """
        
        # Get analysis from GPT-4
        gpt4_response = await self._get_gpt4_analysis(system_prompt, user_prompt)
        
        # Get second opinion from Claude for complex cases
        claude_response = await self._get_claude_analysis(system_prompt, user_prompt)
        
        # Combine and validate responses
        analysis_result = self._combine_ai_analyses(gpt4_response, claude_response)
        
        return analysis_result

    async def _get_gpt4_analysis(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Get analysis from GPT-4"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        
        except Exception as e:
            print(f"GPT-4 analysis error: {e}")
            return self._get_fallback_analysis()

    async def _get_claude_analysis(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Get analysis from Claude"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                temperature=0.1,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            content = response.content[0].text
            return json.loads(content)
        
        except Exception as e:
            print(f"Claude analysis error: {e}")
            return self._get_fallback_analysis()

    def _combine_ai_analyses(self, gpt4_result: Dict, claude_result: Dict) -> Dict[str, Any]:
        """Combine analyses from both AI models"""
        
        # Merge differential diagnoses and average confidence scores
        combined_diagnoses = {}
        
        # Process GPT-4 diagnoses
        for diagnosis in gpt4_result.get("differential_diagnoses", []):
            condition = diagnosis.get("condition_name")
            if condition:
                combined_diagnoses[condition] = {
                    "condition_name": condition,
                    "gpt4_confidence": diagnosis.get("confidence_score", 0.5),
                    "claude_confidence": 0.0,
                    "gpt4_reasoning": diagnosis.get("reasoning", ""),
                    "claude_reasoning": ""
                }
        
        # Process Claude diagnoses
        for diagnosis in claude_result.get("differential_diagnoses", []):
            condition = diagnosis.get("condition_name")
            if condition in combined_diagnoses:
                combined_diagnoses[condition]["claude_confidence"] = diagnosis.get("confidence_score", 0.5)
                combined_diagnoses[condition]["claude_reasoning"] = diagnosis.get("reasoning", "")
            else:
                combined_diagnoses[condition] = {
                    "condition_name": condition,
                    "gpt4_confidence": 0.0,
                    "claude_confidence": diagnosis.get("confidence_score", 0.5),
                    "gpt4_reasoning": "",
                    "claude_reasoning": diagnosis.get("reasoning", "")
                }
        
        # Calculate combined confidence scores
        final_diagnoses = []
        for condition, data in combined_diagnoses.items():
            gpt4_conf = data["gpt4_confidence"]
            claude_conf = data["claude_confidence"]
            
            # Average confidence with weight towards agreement
            if gpt4_conf > 0 and claude_conf > 0:
                combined_confidence = (gpt4_conf + claude_conf) / 2
                agreement_bonus = 0.1 if abs(gpt4_conf - claude_conf) < 0.2 else 0
                combined_confidence = min(1.0, combined_confidence + agreement_bonus)
            else:
                combined_confidence = max(gpt4_conf, claude_conf) * 0.8  # Reduce confidence for single model
            
            final_diagnoses.append({
                "condition_name": condition,
                "confidence_score": combined_confidence,
                "ai_reasoning": self._combine_reasoning(data["gpt4_reasoning"], data["claude_reasoning"]),
                "source_models": ["gpt-4"] if gpt4_conf > 0 else [] + ["claude"] if claude_conf > 0 else []
            })
        
        # Sort by confidence score
        final_diagnoses.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        return {
            "differential_diagnoses": final_diagnoses[:settings.MAX_DIFFERENTIAL_DIAGNOSES],
            "recommended_tests": self._merge_recommendations(
                gpt4_result.get("recommended_tests", []),
                claude_result.get("recommended_tests", [])
            ),
            "urgency_level": self._determine_urgency(
                gpt4_result.get("urgency_level", "routine"),
                claude_result.get("urgency_level", "routine")
            ),
            "clinical_reasoning": self._combine_reasoning(
                gpt4_result.get("clinical_reasoning", ""),
                claude_result.get("clinical_reasoning", "")
            ),
            "red_flags": list(set(
                gpt4_result.get("red_flags", []) + claude_result.get("red_flags", [])
            ))
        }

    def _combine_reasoning(self, gpt4_reasoning: str, claude_reasoning: str) -> str:
        """Combine reasoning from both models"""
        if gpt4_reasoning and claude_reasoning:
            return f"GPT-4 Analysis: {gpt4_reasoning}\n\nClaude Analysis: {claude_reasoning}"
        return gpt4_reasoning or claude_reasoning

    def _merge_recommendations(self, gpt4_tests: List, claude_tests: List) -> List:
        """Merge test recommendations"""
        all_tests = gpt4_tests + claude_tests
        unique_tests = []
        seen = set()
        
        for test in all_tests:
            test_name = test.get("test_name", "") if isinstance(test, dict) else str(test)
            if test_name not in seen:
                unique_tests.append(test)
                seen.add(test_name)
        
        return unique_tests

    def _determine_urgency(self, gpt4_urgency: str, claude_urgency: str) -> str:
        """Determine overall urgency level"""
        urgency_levels = {"emergency": 4, "urgent": 3, "moderate": 2, "routine": 1}
        
        gpt4_level = urgency_levels.get(gpt4_urgency.lower(), 1)
        claude_level = urgency_levels.get(claude_urgency.lower(), 1)
        
        max_level = max(gpt4_level, claude_level)
        
        for level, value in urgency_levels.items():
            if value == max_level:
                return level
        
        return "routine"

    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """Fallback analysis when AI services are unavailable"""
        return {
            "differential_diagnoses": [
                {
                    "condition_name": "Unable to analyze - AI service unavailable",
                    "confidence_score": 0.0,
                    "reasoning": "Please consult with a healthcare professional for proper diagnosis."
                }
            ],
            "recommended_tests": ["Comprehensive clinical evaluation recommended"],
            "urgency_level": "urgent",
            "clinical_reasoning": "AI analysis unavailable. Immediate clinical assessment recommended.",
            "red_flags": ["AI service unavailable - manual assessment required"]
        }

    async def generate_medical_summary(self, diagnosis_session) -> str:
        """Generate a comprehensive medical summary"""
        system_prompt = """You are a medical documentation AI. Create a concise, professional medical summary 
        suitable for healthcare records. Include key findings, differential diagnoses, and recommendations."""
        
        user_prompt = f"""
        Create a medical summary for this case:
        Chief Complaint: {diagnosis_session.chief_complaint}
        Symptoms: {len(diagnosis_session.symptoms)} symptoms documented
        AI Analysis: {diagnosis_session.ai_summary}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Medical summary generation failed: {e}"

# Global AI service instance
ai_service = MedicalAIService()
