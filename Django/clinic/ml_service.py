"""
ML/AI Integration Services
Handles disease prediction and health insights generation
"""

import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from django.conf import settings
from typing import Dict, List, Tuple
import os
import logging

# Import LLM service
from .llm_service import AIInsightGenerator


class MLPredictor:
    """
    Disease prediction service using trained ML model
    Integrates with models from ML/models/ directory
    """
    
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.severity_dict = {}
        self.description_dict = {}
        self.precaution_dict = {}
        self._load_model()
        self._load_metadata()
    
    def _load_model(self):
        """Load trained ML model"""
        model_path = settings.ML_MODEL_PATH
        
        try:
            # Try v2 model first
            if model_path.exists():
                with open(model_path, 'rb') as f:
                    model_data = pickle.load(f)
                self.model = model_data['model']
                self.feature_names = model_data['feature_names']
                print(f"[OK] Loaded ML model from {model_path}")
            else:
                # Fallback to v1 model
                fallback_path = model_path.parent / 'disease_predictor.pkl'
                with open(fallback_path, 'rb') as f:
                    model_data = pickle.load(f)
                self.model = model_data['model']
                self.feature_names = model_data['feature_names']
                print(f"[OK] Loaded ML model from {fallback_path}")
        except Exception as e:
            print(f"[ERROR] Error loading ML model: {e}")
            raise
    
    def _load_metadata(self):
        """Load symptom severity, descriptions, and precautions"""
        datasets_path = settings.ML_DATASETS_PATH
        
        try:
            # Load symptom severity
            severity_path = datasets_path / 'Symptom-severity.csv'
            if severity_path.exists():
                severity_df = pd.read_csv(severity_path)
                self.severity_dict = dict(zip(severity_df['Symptom'], severity_df['weight']))
            
            # Load disease descriptions
            desc_path = datasets_path / 'symptom_Description.csv'
            if desc_path.exists():
                desc_df = pd.read_csv(desc_path)
                self.description_dict = dict(zip(desc_df['Disease'], desc_df['Description']))
            
            # Load precautions
            precaution_path = datasets_path / 'symptom_precaution.csv'
            if precaution_path.exists():
                precaution_df = pd.read_csv(precaution_path)
                for _, row in precaution_df.iterrows():
                    disease = row['Disease']
                    precautions = [
                        row[f'Precaution_{i}'] 
                        for i in range(1, 5) 
                        if pd.notna(row.get(f'Precaution_{i}', ''))
                    ]
                    self.precaution_dict[disease] = precautions
            
            print("[OK] Loaded disease metadata")
        except Exception as e:
            print(f"[WARN] Error loading metadata: {e}")
    
    def predict(self, symptoms: List[str]) -> Dict:
        """
        Predict disease from symptoms
        
        Args:
            symptoms: List of symptom names (e.g., ['fever', 'cough'])
        
        Returns:
            Dictionary with prediction results
        """
        if not self.model or not self.feature_names:
            raise ValueError("ML model not loaded")
        
        # Normalize symptom names (lowercase, replace spaces with underscores)
        normalized_symptoms = [s.lower().replace(' ', '_') for s in symptoms]
        
        # Create input vector
        input_vector = np.zeros(len(self.feature_names))
        matched_symptoms = []
        
        for symptom in normalized_symptoms:
            if symptom in self.feature_names:
                idx = self.feature_names.index(symptom)
                input_vector[idx] = 1
                matched_symptoms.append(symptom)
        
        # Get prediction
        prediction = self.model.predict(input_vector.reshape(1, -1))[0]
        
        # Get confidence scores (initialize empty list first)
        top_predictions = []
        
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(input_vector.reshape(1, -1))[0]
            top_3_idx = np.argsort(proba)[::-1][:3]
            
            for idx in top_3_idx:
                disease = self.model.classes_[idx]
                confidence = float(proba[idx])
                top_predictions.append({
                    'disease': disease,
                    'confidence': confidence
                })
        else:
            # Fallback if model doesn't support probability
            top_predictions.append({
                'disease': prediction,
                'confidence': 0.85  # Default confidence for non-probabilistic models
            })
        
        # Get disease information
        description = self.description_dict.get(prediction, '')
        precautions = self.precaution_dict.get(prediction, [])
        
        # Categorize disease
        is_communicable = self._is_communicable(prediction)
        is_acute = self._is_acute(prediction)
        icd10_code = self._get_icd10_code(prediction)
        
        return {
            'predicted_disease': prediction,
            'confidence_score': float(top_predictions[0]['confidence']) if top_predictions else 0.0,
            'top_predictions': top_predictions,
            'description': description,
            'precautions': precautions,
            'matched_symptoms': matched_symptoms,
            'is_communicable': is_communicable,
            'is_acute': is_acute,
            'icd10_code': icd10_code
        }
    
    def _is_communicable(self, disease: str) -> bool:
        """Determine if disease is communicable"""
        communicable_diseases = [
            'common cold', 'flu', 'tuberculosis', 'pneumonia', 'covid-19',
            'malaria', 'dengue', 'typhoid', 'hepatitis', 'chickenpox',
            'measles', 'mumps', 'influenza'
        ]
        return any(comm in disease.lower() for comm in communicable_diseases)
    
    def _is_acute(self, disease: str) -> bool:
        """Determine if disease is acute (vs chronic)"""
        chronic_diseases = [
            'diabetes', 'hypertension', 'asthma', 'arthritis', 'chronic',
            'migraine', 'allergy', 'gerd', 'osteoporosis'
        ]
        return not any(chronic in disease.lower() for chronic in chronic_diseases)
    
    def _get_icd10_code(self, disease: str) -> str:
        """Get ICD-10 code for disease (simplified mapping)"""
        icd10_mapping = {
            'common cold': 'J00',
            'influenza': 'J11',
            'pneumonia': 'J18',
            'diabetes': 'E11',
            'hypertension': 'I10',
            'asthma': 'J45',
            'migraine': 'G43',
            'dengue': 'A90',
            'typhoid': 'A01',
            'malaria': 'B54',
        }
        
        disease_lower = disease.lower()
        for key, code in icd10_mapping.items():
            if key in disease_lower:
                return code
        
        return ''
    
    def get_available_symptoms(self) -> List[str]:
        """Get list of all available symptoms the model can recognize"""
        return self.feature_names if self.feature_names else []


# Singleton instances
_ml_predictor = None
_ai_generator = None


def get_ml_predictor() -> MLPredictor:
    """Get ML predictor singleton instance"""
    global _ml_predictor
    if _ml_predictor is None:
        _ml_predictor = MLPredictor()
    return _ml_predictor


def get_ai_generator() -> AIInsightGenerator:
    """
    Get AI insight generator singleton instance
    Uses the real LLM-powered AIInsightGenerator from llm_service.py
    """
    global _ai_generator
    if _ai_generator is None:
        _ai_generator = AIInsightGenerator()
    return _ai_generator
