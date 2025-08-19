"""
Medical Data Validators
Validation utilities for medical data and clinical information
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime, date

class MedicalValidators:
    """Validators for medical data"""
    
    @staticmethod
    def validate_icd10_code(code: str) -> bool:
        """Validate ICD-10 diagnosis code format"""
        # ICD-10 format: Letter followed by 2-3 digits, optional decimal and 1-4 more digits
        pattern = r'^[A-Z]\d{2,3}(\.\d{1,4})?$'
        return bool(re.match(pattern, code.upper()))
    
    @staticmethod
    def validate_medical_license(license_number: str) -> bool:
        """Validate medical license number format"""
        # Basic format validation - adjust based on your region's requirements
        pattern = r'^[A-Z]{2}\d{4,8}$'
        return bool(re.match(pattern, license_number.upper()))
    
    @staticmethod
    def validate_patient_age(birth_date: date) -> bool:
        """Validate patient age is reasonable (0-150 years)"""
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return 0 <= age <= 150
    
    @staticmethod
    def validate_confidence_score(score: float) -> bool:
        """Validate AI confidence score is between 0.0 and 1.0"""
        return 0.0 <= score <= 1.0
    
    @staticmethod
    def validate_vital_signs(vitals: Dict[str, Any]) -> Dict[str, bool]:
        """Validate vital signs are within reasonable ranges"""
        validations = {}
        
        # Blood pressure (systolic/diastolic)
        if 'systolic_bp' in vitals:
            validations['systolic_bp'] = 60 <= vitals['systolic_bp'] <= 250
        if 'diastolic_bp' in vitals:
            validations['diastolic_bp'] = 30 <= vitals['diastolic_bp'] <= 150
            
        # Heart rate (BPM)
        if 'heart_rate' in vitals:
            validations['heart_rate'] = 30 <= vitals['heart_rate'] <= 220
            
        # Temperature (Celsius)
        if 'temperature' in vitals:
            validations['temperature'] = 30.0 <= vitals['temperature'] <= 45.0
            
        # Respiratory rate
        if 'respiratory_rate' in vitals:
            validations['respiratory_rate'] = 8 <= vitals['respiratory_rate'] <= 40
            
        # Oxygen saturation
        if 'oxygen_saturation' in vitals:
            validations['oxygen_saturation'] = 70 <= vitals['oxygen_saturation'] <= 100
            
        return validations
    
    @staticmethod
    def sanitize_medical_text(text: str) -> str:
        """Sanitize medical text input"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove potentially dangerous characters but keep medical symbols
        # Keep: letters, numbers, spaces, medical punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)\[\]\+\-\%\/\°\']', '', text)
        
        return text
    
    @staticmethod
    def validate_symptom_severity(severity: str) -> bool:
        """Validate symptom severity level"""
        valid_severities = ['mild', 'moderate', 'severe', 'critical']
        return severity.lower() in valid_severities
    
    @staticmethod
    def validate_urgency_level(urgency: str) -> bool:
        """Validate medical urgency level"""
        valid_urgencies = ['routine', 'moderate', 'urgent', 'emergency']
        return urgency.lower() in valid_urgencies
    
    @staticmethod
    def validate_medical_specialization(specialization: str) -> bool:
        """Validate medical specialization"""
        valid_specializations = [
            'internal_medicine', 'cardiology', 'neurology', 'oncology',
            'pediatrics', 'surgery', 'emergency_medicine', 'radiology',
            'pathology', 'anesthesiology', 'psychiatry', 'dermatology',
            'orthopedics', 'ophthalmology', 'otolaryngology', 'urology',
            'gynecology', 'family_medicine', 'general_practice'
        ]
        return specialization.lower() in valid_specializations
    
    @staticmethod
    def validate_drug_name(drug_name: str) -> bool:
        """Basic validation for drug names"""
        # Allow letters, numbers, spaces, hyphens, parentheses
        pattern = r'^[A-Za-z0-9\s\-\(\)]+$'
        return bool(re.match(pattern, drug_name)) and len(drug_name.strip()) > 0

class ClinicalDataValidator:
    """Advanced clinical data validation"""
    
    @staticmethod
    def validate_diagnosis_session(session_data: Dict[str, Any]) -> List[str]:
        """Validate complete diagnosis session data"""
        errors = []
        
        # Required fields
        required_fields = ['patient_id', 'chief_complaint']
        for field in required_fields:
            if not session_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Validate chief complaint length
        if session_data.get('chief_complaint'):
            complaint = session_data['chief_complaint'].strip()
            if len(complaint) < 5:
                errors.append("Chief complaint too short (minimum 5 characters)")
            if len(complaint) > 1000:
                errors.append("Chief complaint too long (maximum 1000 characters)")
        
        # Validate symptoms if present
        if 'symptoms' in session_data:
            symptoms = session_data['symptoms']
            if not isinstance(symptoms, list):
                errors.append("Symptoms must be a list")
            elif len(symptoms) == 0:
                errors.append("At least one symptom is required")
            else:
                for i, symptom in enumerate(symptoms):
                    if not isinstance(symptom, dict):
                        errors.append(f"Symptom {i+1} must be an object")
                        continue
                    
                    # Validate symptom fields
                    if not symptom.get('name'):
                        errors.append(f"Symptom {i+1}: name is required")
                    
                    if not MedicalValidators.validate_symptom_severity(symptom.get('severity', '')):
                        errors.append(f"Symptom {i+1}: invalid severity level")
        
        return errors
    
    @staticmethod
    def validate_ai_diagnosis(diagnosis_data: Dict[str, Any]) -> List[str]:
        """Validate AI-generated diagnosis data"""
        errors = []
        
        # Required fields
        required_fields = ['condition_name', 'confidence_score']
        for field in required_fields:
            if field not in diagnosis_data:
                errors.append(f"Missing required field: {field}")
        
        # Validate confidence score
        if 'confidence_score' in diagnosis_data:
            score = diagnosis_data['confidence_score']
            if not isinstance(score, (int, float)):
                errors.append("Confidence score must be a number")
            elif not MedicalValidators.validate_confidence_score(score):
                errors.append("Confidence score must be between 0.0 and 1.0")
        
        # Validate condition name
        if 'condition_name' in diagnosis_data:
            condition = diagnosis_data['condition_name'].strip()
            if len(condition) < 2:
                errors.append("Condition name too short")
            if len(condition) > 200:
                errors.append("Condition name too long")
        
        # Validate ICD-10 code if present
        if 'icd_10_code' in diagnosis_data and diagnosis_data['icd_10_code']:
            if not MedicalValidators.validate_icd10_code(diagnosis_data['icd_10_code']):
                errors.append("Invalid ICD-10 code format")
        
        return errors

# Utility functions for common medical calculations
class MedicalCalculations:
    """Medical calculation utilities"""
    
    @staticmethod
    def calculate_age(birth_date: date) -> int:
        """Calculate age from birth date"""
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    @staticmethod
    def calculate_bmi(weight_kg: float, height_m: float) -> float:
        """Calculate Body Mass Index"""
        if height_m <= 0:
            raise ValueError("Height must be greater than 0")
        return round(weight_kg / (height_m ** 2), 1)
    
    @staticmethod
    def categorize_bmi(bmi: float) -> str:
        """Categorize BMI value"""
        if bmi < 18.5:
            return "underweight"
        elif bmi < 25:
            return "normal"
        elif bmi < 30:
            return "overweight"
        else:
            return "obese"
    
    @staticmethod
    def calculate_map(systolic: int, diastolic: int) -> float:
        """Calculate Mean Arterial Pressure"""
        return round((2 * diastolic + systolic) / 3, 1)
