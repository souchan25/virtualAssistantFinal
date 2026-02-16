# Custom actions for CPSU Virtual Health Assistant
# Integrates with Django ML backend for disease prediction

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import logging

logger = logging.getLogger(__name__)

# Django backend configuration
DJANGO_BASE_URL = "http://localhost:8000"
DJANGO_ML_ENDPOINT = f"{DJANGO_BASE_URL}/api/rasa/predict/"

# Emergency symptoms that require immediate attention
EMERGENCY_SYMPTOMS = [
    'chest_pain', 'severe_chest_pain', 'difficulty_breathing', 'breathlessness',
    'loss_of_consciousness', 'coma', 'severe_headache', 'confusion',
    'altered_sensorium', 'weakness_of_one_body_side', 'slurred_speech',
    'acute_liver_failure', 'stomach_bleeding', 'blood_in_sputum',
    'severe_abdominal_pain', 'continuous_feel_of_urine'
]


class ActionExtractSymptoms(Action):
    """Extract symptoms from user message and store in slot"""
    
    def name(self) -> Text:
        return "action_extract_symptoms"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get current symptoms from slot
        current_symptoms = tracker.get_slot("symptoms") or []
        
        # Extract symptom entities from latest message
        entities = tracker.latest_message.get('entities', [])
        new_symptoms = [entity['value'] for entity in entities if entity['entity'] == 'symptom']
        
        # Combine with existing symptoms (remove duplicates)
        all_symptoms = list(set(current_symptoms + new_symptoms))
        
        logger.info(f"Extracted symptoms: {new_symptoms}")
        logger.info(f"Total symptoms: {all_symptoms}")
        
        if new_symptoms:
            symptom_list = ", ".join(new_symptoms)
            dispatcher.utter_message(text=f"I've noted: {symptom_list}")
        
        return [SlotSet("symptoms", all_symptoms)]


class ActionPredictDisease(Action):
    """Call Django ML API to predict disease from symptoms"""
    
    def name(self) -> Text:
        return "action_predict_disease"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptoms = tracker.get_slot("symptoms") or []
        sender_id = tracker.sender_id
        
        if not symptoms:
            dispatcher.utter_message(text="I haven't recorded any symptoms yet. Please tell me what you're experiencing.")
            return []
        
        try:
            # Normalize symptoms (replace spaces with underscores, lowercase)
            normalized_symptoms = [s.lower().replace(' ', '_') for s in symptoms]
            
            # Call Django ML API
            logger.info(f"Calling Django ML API with symptoms: {normalized_symptoms}")
            
            response = requests.post(
                DJANGO_ML_ENDPOINT,
                json={
                    "symptoms": normalized_symptoms,
                    "sender_id": sender_id,
                    "generate_insights": True  # Enable ML+LLM hybrid validation for reliable output
                },
                timeout=60  # Increased timeout for ML + LLM validation
            )
            
            if response.status_code == 200:
                data = response.json()
                
                predicted_disease = data.get('predicted_disease', 'Unknown')
                confidence = data.get('confidence', 0.0)
                confidence_pct = int(confidence * 100)
                description = data.get('description', '')
                precautions = data.get('precautions', [])
                is_communicable = data.get('is_communicable', False)
                llm_validated = data.get('llm_validated', False)
                
                # Format response message
                message = f"🏥 **Diagnosis Analysis**\n\n"
                message += f"**Condition**: {predicted_disease}\n"
                message += f"**Confidence**: {confidence_pct}%"
                
                if llm_validated:
                    message += " ✅ (AI Validated)\n\n"
                else:
                    message += "\n\n"
                
                if description:
                    message += f"**Description**: {description}\n\n"
                
                if is_communicable:
                    message += "⚠️ **Note**: This condition may be communicable. Please avoid close contact with others.\n\n"
                
                message += "**Recommended Precautions**:\n"
                for i, precaution in enumerate(precautions[:4], 1):
                    message += f"{i}. {precaution}\n"
                
                message += "\n⚕️ **Important**: This is an AI-based assessment. "
                message += "Please visit the CPSU clinic for proper medical diagnosis and treatment."
                
                # Get top 3 alternative predictions
                top_predictions = data.get('top_predictions', [])
                
                # Send diagnosis message with custom data for Django to save
                dispatcher.utter_message(
                    text=message,
                    custom={
                        "diagnosis": {
                            "predicted_disease": predicted_disease,
                            "confidence": confidence,
                            "symptoms": normalized_symptoms,
                            "description": description,
                            "precautions": precautions,
                            "is_communicable": is_communicable,
                            "is_acute": data.get('is_acute', False),
                            "icd10_code": data.get('icd10_code', ''),
                            "top_predictions": top_predictions,
                            "duration_days": 1,  # Default, can be improved with slot tracking
                            "severity": "moderate"  # Default, can be improved with slot tracking
                        }
                    }
                )
                
                if len(top_predictions) > 1:
                    alternatives = "\n\n**Other Possibilities**:\n"
                    for pred in top_predictions[1:3]:  # Skip first (already shown)
                        alt_disease = pred.get('disease', '')
                        alt_conf = int(pred.get('confidence', 0) * 100)
                        alternatives += f"• {alt_disease} ({alt_conf}%)\n"
                    dispatcher.utter_message(text=alternatives)
                
                return [
                    SlotSet("diagnosis", predicted_disease),
                    SlotSet("confidence", confidence)
                ]
            else:
                logger.error(f"Django API error: {response.status_code} - {response.text}")
                dispatcher.utter_message(
                    text="I'm having trouble analyzing your symptoms right now. "
                         "Please visit the CPSU clinic for assistance."
                )
                return []
        
        except requests.exceptions.Timeout:
            logger.error("Django API timeout")
            dispatcher.utter_message(
                text="The analysis is taking longer than expected. "
                     "Please try again or visit the clinic directly."
            )
            return []
        
        except Exception as e:
            logger.error(f"Error calling Django ML API: {str(e)}")
            dispatcher.utter_message(
                text="I encountered an error while analyzing your symptoms. "
                     "Please visit the CPSU clinic for proper diagnosis."
            )
            return []


class ActionProvidePrecautions(Action):
    """Provide precautions for the diagnosed condition"""
    
    def name(self) -> Text:
        return "action_provide_precautions"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        diagnosis = tracker.get_slot("diagnosis")
        
        if not diagnosis:
            dispatcher.utter_message(
                text="I need to analyze your symptoms first. Please tell me what you're experiencing."
            )
            return []
        
        # Precautions are already provided in action_predict_disease
        # This action can provide additional specific guidance
        
        dispatcher.utter_message(
            text=f"For {diagnosis}, make sure to:\n"
                 "• Follow the recommended precautions\n"
                 "• Get adequate rest\n"
                 "• Stay hydrated\n"
                 "• Visit CPSU clinic if symptoms worsen\n"
                 "• Avoid self-medication"
        )
        
        return []


class ActionCheckEmergency(Action):
    """Check if symptoms indicate an emergency situation"""
    
    def name(self) -> Text:
        return "action_check_emergency"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        symptoms = tracker.get_slot("symptoms") or []
        
        # Normalize symptoms
        normalized_symptoms = [s.lower().replace(' ', '_') for s in symptoms]
        
        # Check for emergency symptoms
        is_emergency = any(symptom in EMERGENCY_SYMPTOMS for symptom in normalized_symptoms)
        
        if is_emergency or tracker.latest_message.get('intent', {}).get('name') == 'emergency':
            dispatcher.utter_message(
                text="🚨 **EMERGENCY ALERT** 🚨\n\n"
                     "Your symptoms may require immediate medical attention!\n\n"
                     "**PLEASE DO ONE OF THE FOLLOWING IMMEDIATELY**:\n"
                     "1. Visit the CPSU Health Clinic NOW\n"
                     "2. Go to the nearest hospital emergency room\n"
                     "3. Call emergency services (911 or local emergency number)\n\n"
                     "Do NOT wait or delay seeking medical care."
            )
        
        return []


class ActionDefaultFallback(Action):
    """Fallback action when intent is not recognized"""
    
    def name(self) -> Text:
        return "action_default_fallback"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(
            text="I'm sorry, I didn't quite understand that. I can help you with:\n"
                 "• Reporting symptoms (e.g., 'I have fever and cough')\n"
                 "• Getting health information\n"
                 "• Emergency assistance\n\n"
                 "What would you like to do?"
        )
        
        return []

