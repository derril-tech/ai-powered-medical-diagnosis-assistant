"""
AI Prompt Templates for Medical Diagnosis
Structured prompts for OpenAI and Claude medical analysis
"""

from typing import Dict, List, Any
from datetime import datetime

class MedicalAIPrompts:
    """Medical AI prompt templates and utilities"""
    
    @staticmethod
    def get_system_prompt() -> str:
        """Base system prompt for medical AI analysis"""
        return """You are an expert medical AI assistant specializing in differential diagnosis and clinical decision support. 
        You help healthcare professionals by analyzing patient symptoms and providing evidence-based diagnostic suggestions.
        
        CRITICAL GUIDELINES:
        1. Always provide differential diagnoses ranked by likelihood with confidence scores (0.0-1.0)
        2. Include detailed medical reasoning for each diagnosis
        3. Suggest appropriate diagnostic tests and procedures
        4. Indicate urgency level (routine, moderate, urgent, emergency)
        5. Identify any clinical red flags requiring immediate attention
        6. Provide evidence-based recommendations with medical literature references when possible
        7. Never provide definitive diagnoses - only suggestions for healthcare professionals
        8. Always recommend consulting with appropriate specialists when needed
        9. Consider patient demographics, medical history, and risk factors
        10. Maintain medical accuracy and patient safety as top priorities
        
        OUTPUT FORMAT:
        Respond with a structured JSON object containing:
        - differential_diagnoses: Array of potential diagnoses with confidence scores and reasoning
        - recommended_tests: Array of suggested diagnostic tests
        - urgency_level: String indicating urgency (routine/moderate/urgent/emergency)
        - clinical_reasoning: Detailed explanation of your analysis
        - red_flags: Array of concerning symptoms requiring immediate attention
        - specialist_referrals: Suggested specialist consultations if needed
        """
    
    @staticmethod
    def build_symptom_analysis_prompt(
        patient_data: Dict[str, Any],
        symptoms: List[Dict[str, Any]],
        medical_history: str = None
    ) -> str:
        """Build comprehensive symptom analysis prompt"""
        
        # Format patient information
        patient_info = f"""
        PATIENT INFORMATION:
        - Age: {patient_data.get('age', 'Unknown')} years
        - Gender: {patient_data.get('gender', 'Unknown')}
        - Medical History: {medical_history or 'No significant medical history provided'}
        - Known Allergies: {patient_data.get('allergies', 'None reported')}
        - Current Medications: {patient_data.get('current_medications', 'None reported')}
        """
        
        # Format symptoms
        symptom_details = []
        for i, symptom in enumerate(symptoms, 1):
            symptom_text = f"""
        Symptom {i}:
        - Name: {symptom.get('name', 'Not specified')}
        - Severity: {symptom.get('severity', 'Not specified')}
        - Duration: {symptom.get('duration', 'Not specified')}
        - Location: {symptom.get('body_location', 'Not specified')}
        - Description: {symptom.get('description', 'Not provided')}
        - Associated Symptoms: {symptom.get('associated_symptoms', 'None reported')}
        - Triggers: {symptom.get('triggers', 'None identified')}
        - Relieving Factors: {symptom.get('relieving_factors', 'None identified')}
        """
            symptom_details.append(symptom_text)
        
        symptoms_section = "\n".join(symptom_details)
        
        return f"""
        Please analyze the following patient case and provide a comprehensive differential diagnosis:
        
        {patient_info}
        
        PRESENTING SYMPTOMS:
        {symptoms_section}
        
        ANALYSIS REQUEST:
        Provide a thorough medical analysis including:
        1. Top 5 differential diagnoses ranked by likelihood
        2. Confidence scores for each diagnosis (0.0-1.0)
        3. Clinical reasoning for each diagnosis
        4. Recommended diagnostic tests and procedures
        5. Urgency assessment and any red flags
        6. Specialist referral recommendations if needed
        
        Consider the patient's demographics, symptom constellation, and medical history in your analysis.
        """
    
    @staticmethod
    def build_second_opinion_prompt(
        initial_diagnosis: Dict[str, Any],
        patient_data: Dict[str, Any]
    ) -> str:
        """Build prompt for second opinion analysis"""
        return f"""
        Please provide a second opinion on the following medical case analysis:
        
        INITIAL AI ANALYSIS:
        Primary Diagnosis: {initial_diagnosis.get('primary_diagnosis', 'Not specified')}
        Confidence: {initial_diagnosis.get('confidence_score', 'Not specified')}
        Reasoning: {initial_diagnosis.get('reasoning', 'Not provided')}
        
        PATIENT CONTEXT:
        Age: {patient_data.get('age')} years
        Gender: {patient_data.get('gender')}
        Key Symptoms: {', '.join(patient_data.get('key_symptoms', []))}
        
        SECOND OPINION REQUEST:
        1. Do you agree with the primary diagnosis? Why or why not?
        2. What alternative diagnoses should be considered?
        3. Are there any missed red flags or concerning features?
        4. What additional tests or evaluations would you recommend?
        5. How would you modify the urgency assessment?
        
        Provide your analysis in the same structured JSON format.
        """
    
    @staticmethod
    def build_literature_search_prompt(condition: str) -> str:
        """Build prompt for medical literature search"""
        return f"""
        Please provide evidence-based information about {condition} including:
        
        1. Current diagnostic criteria and guidelines
        2. Key clinical features and presentations
        3. Recommended diagnostic workup
        4. Treatment approaches and options
        5. Prognosis and outcomes
        6. Recent research findings or updates
        
        Focus on peer-reviewed sources and established clinical guidelines.
        Include specific references where possible.
        """
    
    @staticmethod
    def build_risk_assessment_prompt(
        patient_data: Dict[str, Any],
        potential_diagnoses: List[str]
    ) -> str:
        """Build risk stratification prompt"""
        return f"""
        Please perform a risk assessment for this patient:
        
        PATIENT PROFILE:
        - Age: {patient_data.get('age')} years
        - Gender: {patient_data.get('gender')}
        - Medical History: {patient_data.get('medical_history', 'None significant')}
        - Risk Factors: {', '.join(patient_data.get('risk_factors', []))}
        
        POTENTIAL DIAGNOSES:
        {', '.join(potential_diagnoses)}
        
        RISK ASSESSMENT REQUEST:
        1. Stratify risk level (low, moderate, high, critical)
        2. Identify modifiable risk factors
        3. Assess immediate vs long-term risks
        4. Recommend risk mitigation strategies
        5. Determine appropriate monitoring intervals
        
        Consider evidence-based risk calculators and guidelines where applicable.
        """
    
    @staticmethod
    def build_treatment_recommendation_prompt(
        diagnosis: str,
        patient_data: Dict[str, Any]
    ) -> str:
        """Build treatment recommendation prompt"""
        return f"""
        Please provide evidence-based treatment recommendations for:
        
        DIAGNOSIS: {diagnosis}
        
        PATIENT CONTEXT:
        - Age: {patient_data.get('age')} years
        - Gender: {patient_data.get('gender')}
        - Allergies: {patient_data.get('allergies', 'None known')}
        - Current Medications: {patient_data.get('current_medications', 'None')}
        - Comorbidities: {patient_data.get('comorbidities', 'None')}
        
        TREATMENT RECOMMENDATIONS NEEDED:
        1. First-line treatment options
        2. Alternative treatments if first-line fails
        3. Contraindications and precautions
        4. Monitoring requirements
        5. Patient education points
        6. Follow-up recommendations
        7. When to escalate care
        
        Base recommendations on current clinical guidelines and best practices.
        """
    
    @staticmethod
    def validate_ai_response(response_data: Dict[str, Any]) -> List[str]:
        """Validate AI response structure and content"""
        errors = []
        
        required_fields = [
            'differential_diagnoses',
            'recommended_tests',
            'urgency_level',
            'clinical_reasoning'
        ]
        
        for field in required_fields:
            if field not in response_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate differential diagnoses structure
        if 'differential_diagnoses' in response_data:
            diagnoses = response_data['differential_diagnoses']
            if not isinstance(diagnoses, list):
                errors.append("differential_diagnoses must be a list")
            else:
                for i, diagnosis in enumerate(diagnoses):
                    if not isinstance(diagnosis, dict):
                        errors.append(f"Diagnosis {i+1} must be an object")
                        continue
                    
                    required_diagnosis_fields = ['condition_name', 'confidence_score', 'ai_reasoning']
                    for field in required_diagnosis_fields:
                        if field not in diagnosis:
                            errors.append(f"Diagnosis {i+1} missing field: {field}")
                    
                    # Validate confidence score
                    if 'confidence_score' in diagnosis:
                        score = diagnosis['confidence_score']
                        if not isinstance(score, (int, float)) or not (0.0 <= score <= 1.0):
                            errors.append(f"Diagnosis {i+1} invalid confidence score")
        
        # Validate urgency level
        if 'urgency_level' in response_data:
            urgency = response_data['urgency_level'].lower()
            valid_urgencies = ['routine', 'moderate', 'urgent', 'emergency']
            if urgency not in valid_urgencies:
                errors.append(f"Invalid urgency level: {urgency}")
        
        return errors

class PromptOptimizer:
    """Optimize prompts for better AI responses"""
    
    @staticmethod
    def add_context_enhancement(prompt: str, context: Dict[str, Any]) -> str:
        """Enhance prompt with additional context"""
        enhancements = []
        
        if context.get('time_of_day'):
            enhancements.append(f"Time of presentation: {context['time_of_day']}")
        
        if context.get('season'):
            enhancements.append(f"Season: {context['season']}")
        
        if context.get('geographic_location'):
            enhancements.append(f"Geographic location: {context['geographic_location']}")
        
        if context.get('recent_travel'):
            enhancements.append(f"Recent travel: {context['recent_travel']}")
        
        if enhancements:
            enhancement_text = "\n\nADDITIONAL CONTEXT:\n" + "\n".join(f"- {e}" for e in enhancements)
            prompt += enhancement_text
        
        return prompt
    
    @staticmethod
    def add_confidence_calibration(prompt: str) -> str:
        """Add confidence calibration instructions"""
        calibration_text = """
        
        CONFIDENCE CALIBRATION:
        - 0.9-1.0: Virtually certain, classic presentation
        - 0.8-0.9: High confidence, typical features present
        - 0.7-0.8: Good confidence, most features align
        - 0.6-0.7: Moderate confidence, some uncertainty
        - 0.5-0.6: Low confidence, differential consideration
        - 0.0-0.5: Very low confidence, unlikely but possible
        """
        return prompt + calibration_text
