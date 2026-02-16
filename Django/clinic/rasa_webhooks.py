"""
API endpoint for Rasa to call Django ML prediction service
This allows Rasa to get ML predictions during conversations
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .ml_service import get_ml_predictor
from .llm_service import AIInsightGenerator
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])  # Rasa webhook - secure with API key in production
def rasa_webhook_predict(request):
    """
    Webhook for Rasa to get ML disease predictions
    
    POST /api/rasa/predict/
    
    Request:
    {
        "symptoms": ["fever", "headache", "fatigue"],
        "sender_id": "user-session-id",
        "generate_insights": true  # optional, default false
    }
    
    Response:
    {
        "predicted_disease": "Common Cold",
        "confidence": 0.85,
        "top_predictions": [...],
        "description": "...",
        "precautions": [...],
        "insights": [...]  # if generate_insights=true
    }
    """
    try:
        # Validate request
        symptoms = request.data.get('symptoms', [])
        sender_id = request.data.get('sender_id')
        generate_insights = request.data.get('generate_insights', False)
        
        if not symptoms:
            return Response({
                'error': 'symptoms list is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get ML prediction
        predictor = get_ml_predictor()
        prediction = predictor.predict(symptoms)
        
        # HYBRID: Use LLM to validate ML prediction (FREE tier)
        llm_validation = None
        validation_confidence_boost = 0.0
        
        if generate_insights:
            try:
                llm_validator = AIInsightGenerator()
                llm_validation = llm_validator.validate_ml_prediction(
                    symptoms=symptoms,
                    ml_prediction=prediction.get('predicted_disease'),
                    ml_confidence=prediction.get('confidence_score')
                )
                
                # Boost confidence if LLM agrees
                if llm_validation and llm_validation.get('agrees_with_ml'):
                    validation_confidence_boost = llm_validation.get('confidence_boost', 0.05)
                    logger.info(f"LLM validated ML prediction: {llm_validation.get('reasoning')}")
                
            except Exception as e:
                logger.warning(f"LLM validation failed (continuing with ML only): {e}")
        
        # Calculate final confidence (ML + LLM validation boost)
        final_confidence = min(
            prediction.get('confidence_score', 0.0) + validation_confidence_boost,
            1.0  # Cap at 100%
        )
        
        # Prepare response
        response_data = {
            'predicted_disease': prediction.get('predicted_disease'),
            'confidence': final_confidence,
            'ml_confidence': prediction.get('confidence_score'),  # Original ML score
            'llm_validated': llm_validation is not None,
            'top_predictions': prediction.get('top_predictions', [])[:3],
            'description': prediction.get('description'),
            'precautions': prediction.get('precautions', []),
            'is_communicable': prediction.get('is_communicable', False),
            'is_acute': prediction.get('is_acute', False),
            'icd10_code': prediction.get('icd10_code', ''),
            'matched_symptoms': prediction.get('matched_symptoms', [])
        }
        
        # Add LLM validation results to response
        if llm_validation:
            response_data['llm_validation'] = {
                'agrees': llm_validation.get('agrees_with_ml'),
                'reasoning': llm_validation.get('reasoning'),
                'confidence_boost': validation_confidence_boost,
                'alternative_diagnosis': llm_validation.get('alternative_diagnosis')
            }
        
        # Generate AI insights if requested (optional, uses LLM)
        if generate_insights:
            try:
                ai_generator = AIInsightGenerator()
                insights = ai_generator.generate_health_insights(
                    symptoms=symptoms,
                    predictions=prediction
                )
                response_data['insights'] = insights
            except Exception as e:
                logger.error(f"Failed to generate insights: {e}")
                response_data['insights'] = []
        
        logger.info(f"Rasa webhook prediction for {sender_id}: {prediction.get('predicted_disease')} (confidence: {final_confidence:.2f}, validated: {llm_validation is not None})")
        
        return Response(response_data)
        
    except Exception as e:
        logger.error(f"Rasa webhook error: {e}")
        return Response({
            'error': 'Failed to generate prediction',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def rasa_webhook_symptoms(request):
    """
    Get list of available symptoms for Rasa entity extraction
    
    GET /api/rasa/symptoms/
    
    Response:
    {
        "symptoms": ["fever", "headache", ...]
    }
    """
    try:
        predictor = get_ml_predictor()
        symptoms = predictor.get_available_symptoms()
        
        return Response({
            'symptoms': symptoms,
            'count': len(symptoms)
        })
        
    except Exception as e:
        logger.error(f"Failed to get symptoms: {e}")
        return Response({
            'error': 'Failed to retrieve symptoms'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
