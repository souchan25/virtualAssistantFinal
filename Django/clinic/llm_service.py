"""
LLM Integration Services for AI-powered health insights
Supports multiple LLM providers: Gemini, OpenRouter (Qwen 3), Groq, and Cohere
"""

import logging
import re
from typing import Dict, List
from django.conf import settings
import os
import requests
import json

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import cohere
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False


class AIInsightGenerator:
    """
    Generates AI-powered health insights using multiple LLM providers.
    Supports Gemini, Groq, and Cohere.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.logger = logging.getLogger(__name__)
        self._initialized = True
        
        # Initialize Gemini with new API
        self.gemini_client = None
        
        if GEMINI_AVAILABLE and settings.GEMINI_API_KEY:
            try:
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
                self.logger.info("Gemini AI initialized successfully (new API)")
            except Exception as e:
                self.logger.error(f"Gemini initialization failed: {e}")
                self.gemini_client = None
        else:
            self.logger.warning("Gemini not available - check API key or install google-genai")
        
        # Initialize OpenRouter (Qwen 3 free model)
        self.openrouter_api_key = None
        if hasattr(settings, 'OPENROUTER_API_KEY') and settings.OPENROUTER_API_KEY:
            self.openrouter_api_key = settings.OPENROUTER_API_KEY
            self.logger.info("OpenRouter API key configured (Qwen 3 free model)")
        else:
            self.logger.warning("OpenRouter not available - check OPENROUTER_API_KEY")
            
        # Initialize Groq (direct API, not OpenRouter)
        self.groq_client = None
        if OPENAI_AVAILABLE and hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY:
            try:
                self.groq_client = OpenAI(
                    api_key=settings.GROQ_API_KEY,
                    base_url="https://api.groq.com/openai/v1",
                )
                self.logger.info("Groq API initialized successfully")
            except Exception as e:
                self.logger.error(f"Groq initialization failed: {e}")
                self.groq_client = None
        else:
            self.logger.warning("Groq not available - check GROQ_API_KEY")
            
        # Initialize Cohere
        if COHERE_AVAILABLE and settings.COHERE_API_KEY:
            try:
                self.cohere_client = cohere.Client(settings.COHERE_API_KEY)
                self.logger.info("Cohere AI initialized successfully")
            except Exception as e:
                self.logger.error(f"Cohere initialization failed: {e}")
                self.cohere_client = None
        else:
            self.cohere_client = None
        
        self.logger.info("AI Insight Generator initialized with real LLM APIs")
    
    def _fix_json_response(self, text: str) -> str:
        """
        Fix common JSON errors in LLM responses.
        LLMs sometimes return malformed JSON that needs cleanup.
        """
        if not text:
            return text
        
        # Fix "true/false" literal (LLM copies from prompt example)
        text = re.sub(r':\s*true/false', ': true', text)
        
        # Fix trailing commas before closing braces
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        
        # Fix single quotes to double quotes
        # Be careful not to change apostrophes in text
        text = re.sub(r"'(\w+)':", r'"\1":', text)  # 'key': -> "key":
        text = re.sub(r":\s*'([^']*)'", r': "\1"', text)  # : 'value' -> : "value"
        
        # Fix unquoted null
        text = re.sub(r':\s*null\b', ': null', text, flags=re.IGNORECASE)
        text = re.sub(r':\s*None\b', ': null', text)
        
        # Fix Python-style booleans
        text = re.sub(r':\s*True\b', ': true', text)
        text = re.sub(r':\s*False\b', ': false', text)
        
        return text
    
    def generate_chat_response(self, message: str, context: dict = None) -> str:
        """
        Generate AI response for health chat using available LLM.
        Tries Groq first, then Qwen (OpenRouter), then Cohere, then Gemini.
        
        Args:
            message: User's message
            context: Optional context (previous messages, user profile, etc.)
        
        Returns:
            AI-generated response
        """
        # Build system prompt
        system_prompt = """You are a compassionate health assistant for CPSU (Central Philippines State University) students.
        
Guidelines:
- Provide supportive, empathetic health guidance
- Support English, Filipino, and local Philippine dialects
- Always recommend seeing clinic staff for serious concerns
- Keep responses concise and actionable
- Be culturally sensitive to Filipino students
- Never diagnose - only provide general health information"""
        
        # Fallback chain: Groq → Qwen (OpenRouter) → Cohere → Gemini
        
        # Try Groq first (fast, free tier)
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    temperature=0.6,
                    max_tokens=1024,
                    top_p=0.95
                )
                result = response.choices[0].message.content
                if result and result.strip():
                    self.logger.info("Response from Groq (Llama 3.3 70B)")
                    return result
                else:
                    raise ValueError("Empty response from Groq")
            except Exception as e:
                self.logger.warning(f"Groq failed: {e}, trying OpenRouter...")
        
        # Try OpenRouter with Mistral free model
        if self.openrouter_api_key:
            try:
                # Prepare payload - json parameter will properly escape all special characters
                payload = {
                    "model": "mistralai/devstral-2512:free",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    "temperature": 0.6,
                    "max_tokens": 500
                }
                
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openrouter_api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://cpsu-health-assistant.edu.ph",
                        "X-Title": "CPSU Virtual Health Assistant",
                    },
                    json=payload,  # Use json parameter instead of data=json.dumps()
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    if content and content.strip():
                        self.logger.info("Response from OpenRouter (Mistral Devstral)")
                        return content
                    else:
                        raise ValueError("Empty response from OpenRouter")
                else:
                    self.logger.warning(f"OpenRouter failed with status {response.status_code}, trying Cohere...")
            except Exception as e:
                self.logger.warning(f"OpenRouter failed: {e}, trying Cohere...")
        
        # Try Cohere
        if self.cohere_client:
            try:
                response = self.cohere_client.chat(
                    message=message,
                    preamble=system_prompt
                )
                self.logger.info("Response from Cohere")
                return response.text
            except Exception as e:
                self.logger.warning(f"Cohere failed: {e}, trying Gemini...")
        
        # Try Gemini as last fallback (rate limited)
        if self.gemini_client:
            try:
                prompt = f"{system_prompt}\n\nUser message: {message}"
                if context:
                    prompt += f"\n\nContext: {context.get('summary', '')}"
                
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                self.logger.info("Response from Gemini 2.5 Flash (last fallback)")
                return response.text
            except Exception as e:
                self.logger.error(f"Gemini (last fallback) failed: {e}")
        
        # Ultimate fallback
        return "Thank you for your message. Based on your symptoms, I recommend consulting with our clinic staff for proper evaluation."
    
    def generate_health_insights(self, symptoms: list, predictions: dict, chat_summary: str = None) -> list:
        """
        Generate health insights using LLM based on symptoms and predictions.
        
        Args:
            symptoms: List of reported symptoms
            predictions: ML prediction results
            chat_summary: Optional summary of chat session
        
        Returns:
            List of insights (max 3)
        """
        disease = predictions.get('predicted_disease') or predictions.get('top_disease', 'Unknown')
        confidence = predictions.get('confidence_score') or predictions.get('confidence', 0)
        
        # Build prompt for insight generation with structured JSON output
        prompt = f"""You are a health assistant for CPSU (Central Philippine State University) students in the Philippines.

Generate 3 health insights for a student with these symptoms: {', '.join(symptoms)}
Predicted condition: {disease} (confidence: {confidence:.0%})

Respond ONLY with a JSON array in this exact format:
[
  {{"category": "Prevention", "text": "Brief prevention tip culturally appropriate for Filipino students"}},
  {{"category": "Monitoring", "text": "What symptoms to monitor and when to be concerned"}},
  {{"category": "Medical Advice", "text": "When to visit the CPSU campus clinic"}}
]

Keep each insight under 100 words. Be culturally sensitive to Filipino students."""

        # Try providers in order: Groq → OpenRouter → Cohere → Gemini
        insights_text = None
        
        # Try Groq first
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=800
                )
                insights_text = response.choices[0].message.content
                self.logger.info("Health insights from Groq")
            except Exception as e:
                self.logger.warning(f"Groq insights failed: {e}")
        
        # Try OpenRouter
        if not insights_text and self.openrouter_api_key:
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openrouter_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "mistralai/devstral-2512:free",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.5,
                        "max_tokens": 800
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    insights_text = response.json()['choices'][0]['message']['content']
                    self.logger.info("Health insights from OpenRouter")
            except Exception as e:
                self.logger.warning(f"OpenRouter insights failed: {e}")
        
        # Try Gemini
        if not insights_text and self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                insights_text = response.text
                self.logger.info("Health insights from Gemini")
            except Exception as e:
                self.logger.warning(f"Gemini insights failed: {e}")
        
        # Parse LLM response into structured insights
        if insights_text:
            try:
                return self._parse_insights_response(insights_text, disease, confidence)
            except Exception as e:
                self.logger.error(f"Failed to parse insights: {e}")
        
        # Fallback to basic insights
        return self._generate_fallback_insights(symptoms, predictions)
    
    def _parse_insights_response(self, insights_text: str, disease: str, confidence: float) -> list:
        """Parse LLM response into structured insights"""
        # Clean up response - extract JSON if wrapped in markdown
        text = insights_text.strip()
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()
        
        # Try to find JSON array
        if not text.startswith('['):
            json_match = re.search(r'\[[\s\S]*\]', text)
            if json_match:
                text = json_match.group(0)
        
        # Parse JSON
        parsed = json.loads(text)
        
        # Add reliability scores based on category
        reliability_map = {'Prevention': 0.85, 'Monitoring': 0.90, 'Medical Advice': confidence or 0.75}
        
        insights = []
        for item in parsed[:3]:
            category = item.get('category', 'General')
            insights.append({
                'category': category,
                'text': item.get('text', ''),
                'reliability_score': reliability_map.get(category, 0.80)
            })
        
        return insights
    
    def _generate_fallback_insights(self, symptoms: list, predictions: dict) -> list:
        """Generate basic insights without LLM"""
        insights = [
            {
                'category': 'Prevention',
                'text': f"Based on your symptoms ({', '.join(symptoms[:3])}), maintain good hygiene and adequate rest.",
                'reliability_score': 0.85
            },
            {
                'category': 'Monitoring',
                'text': "Monitor your condition. If symptoms persist beyond 3 days, visit the campus clinic.",
                'reliability_score': 0.90
            }
        ]
        
        if predictions and predictions.get('top_disease'):
            disease = predictions['top_disease']
            insights.append({
                'category': 'Medical Advice',
                'text': f"Predicted condition: {disease}. Please consult CPSU clinic staff for proper diagnosis.",
                'reliability_score': predictions.get('confidence', 0.7)
            })
        
        return insights[:3]
    
    def validate_ml_prediction(self, symptoms: List[str], ml_prediction: str, ml_confidence: float) -> Dict:
        """
        Use LLM (Gemini, OpenRouter, or Groq) to validate ML prediction for added accuracy
        
        This creates a HYBRID system: ML for fast prediction + LLM for validation
        Cost: FREE (uses Gemini, OpenRouter Qwen 3, or Groq free tier)
        
        Returns:
        {
            'agrees_with_ml': bool,
            'confidence_boost': float,  # 0.0-0.15 boost if agrees
            'reasoning': str,
            'alternative_diagnosis': str or None
        }
        """
        try:
            # Create validation prompt
            symptoms_str = ', '.join(symptoms[:10])  # Limit to avoid token overflow
            
            prompt = f"""You are a medical AI assistant validating a diagnosis prediction.

PATIENT SYMPTOMS: {symptoms_str}

ML MODEL PREDICTION: {ml_prediction} (confidence: {ml_confidence:.2%})

Your task:
1. Evaluate if the ML prediction is medically reasonable given these symptoms
2. Consider if symptoms strongly indicate this condition or if alternatives are more likely
3. Provide a confidence adjustment (-0.15 to +0.15)

Respond ONLY in this exact JSON format:
{{
    "agrees": true/false,
    "confidence_adjustment": 0.0,
    "reasoning": "Brief medical reasoning (2-3 sentences)",
    "alternative_diagnosis": "Alternative condition name or null"
}}

Be concise. Focus on medical accuracy."""

            # Try Groq first (fast, free tier)
            if self.groq_client:
                try:
                    response = self.groq_client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                        max_tokens=500,
                        top_p=0.95
                    )
                    
                    result_text = response.choices[0].message.content
                    
                    # Check for empty response
                    if not result_text or not result_text.strip():
                        raise ValueError("Empty response from Groq API")
                    
                    result_text = result_text.strip()
                    self.logger.info(f"Groq (Llama 3.3 70B) validation response: {result_text[:100]}")
                    
                    # Extract JSON from markdown code blocks if present
                    if '```json' in result_text:
                        result_text = result_text.split('```json')[1].split('```')[0].strip()
                    elif '```' in result_text:
                        result_text = result_text.split('```')[1].split('```')[0].strip()
                    
                    # Try to find JSON object in response
                    if not result_text.startswith('{'):
                        # Look for JSON object pattern (allow nested content)
                        json_match = re.search(r'\{[\s\S]*?"agrees"[\s\S]*?\}', result_text)
                        if json_match:
                            result_text = json_match.group(0)
                    
                    # Fix common LLM JSON errors
                    result_text = self._fix_json_response(result_text)
                    
                    # Validate JSON before parsing
                    if not result_text or not result_text.startswith('{'):
                        raise ValueError(f"No valid JSON found in response: {result_text[:50]}")
                    
                    result_json = json.loads(result_text)
                    
                    return {
                        'agrees_with_ml': result_json.get('agrees', True),
                        'confidence_boost': max(-0.15, min(0.15, result_json.get('confidence_adjustment', 0.0))),
                        'reasoning': result_json.get('reasoning', 'LLM validation completed'),
                        'alternative_diagnosis': result_json.get('alternative_diagnosis')
                    }
                    
                except Exception as groq_error:
                    self.logger.warning(f"Groq validation failed, trying OpenRouter: {groq_error}")
            
            # Try OpenRouter with Mistral free model
            if self.openrouter_api_key:
                try:
                    # Prepare payload - json.dumps will properly escape all special characters
                    payload = {
                        "model": "mistralai/devstral-2512:free",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3,
                        "max_tokens": 500
                    }
                    
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openrouter_api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "https://cpsu-health-assistant.edu.ph",
                            "X-Title": "CPSU Virtual Health Assistant",
                        },
                        json=payload,  # Use json parameter instead of data=json.dumps()
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        response_json = response.json()
                        result_text = response_json['choices'][0]['message']['content']
                        
                        # Check for empty response
                        if not result_text or not result_text.strip():
                            raise ValueError("Empty response from OpenRouter API")
                        
                        result_text = result_text.strip()
                        
                        # Extract JSON from markdown code blocks if present
                        if '```json' in result_text:
                            result_text = result_text.split('```json')[1].split('```')[0].strip()
                        elif '```' in result_text:
                            result_text = result_text.split('```')[1].split('```')[0].strip()
                        
                        # Try to find JSON object in response
                        if not result_text.startswith('{'):
                            json_match = re.search(r'\{[\s\S]*?"agrees"[\s\S]*?\}', result_text)
                            if json_match:
                                result_text = json_match.group(0)
                        
                        # Fix common LLM JSON errors
                        result_text = self._fix_json_response(result_text)
                        
                        # Validate JSON before parsing
                        if not result_text or not result_text.startswith('{'):
                            raise ValueError(f"No valid JSON found in response: {result_text[:50]}")
                        
                        result_json = json.loads(result_text)
                        self.logger.info(f"OpenRouter (Mistral) validation: agrees={result_json.get('agrees')}")
                        
                        return {
                            'agrees_with_ml': result_json.get('agrees', True),
                            'confidence_boost': max(-0.15, min(0.15, result_json.get('confidence_adjustment', 0.0))),
                            'reasoning': result_json.get('reasoning', 'LLM validation completed'),
                            'alternative_diagnosis': result_json.get('alternative_diagnosis')
                        }
                    else:
                        self.logger.warning(f"OpenRouter failed with status {response.status_code}, trying Cohere...")
                        
                except Exception as openrouter_error:
                    self.logger.warning(f"OpenRouter validation failed, trying Cohere: {openrouter_error}")
            
            # Try Cohere
            if self.cohere_client:
                try:
                    # Cohere doesn't support structured JSON, so use simple text parsing
                    simplified_prompt = f"""Given symptoms: {symptoms_str}
ML predicted: {ml_prediction} ({ml_confidence:.0%})

Do you agree with this prediction? Answer: yes/no and brief reason."""
                    
                    response = self.cohere_client.chat(
                        message=simplified_prompt
                    )
                    
                    result_text = response.text.lower()
                    agrees = 'yes' in result_text or 'agree' in result_text or 'correct' in result_text
                    
                    self.logger.info(f"Cohere validation: agrees={agrees}")
                    
                    return {
                        'agrees_with_ml': agrees,
                        'confidence_boost': 0.05 if agrees else -0.05,
                        'reasoning': response.text[:200],
                        'alternative_diagnosis': None
                    }
                    
                except Exception as cohere_error:
                    self.logger.warning(f"Cohere validation failed, trying Gemini: {cohere_error}")
            
            # Try Gemini as last resort (rate limited)
            # if self.gemini_client:
            #     try:
            #         response = self.gemini_client.models.generate_content(
            #             model="gemini-2.5-flash",
            #             contents=prompt
            #         )
            #         result_text = response.text.strip()
                    
            #         # Extract JSON from markdown code blocks if present
            #         if '```json' in result_text:
            #             result_text = result_text.split('```json')[1].split('```')[0].strip()
            #         elif '```' in result_text:
            #             result_text = result_text.split('```')[1].split('```')[0].strip()
                    
            #         result_json = json.loads(result_text)
            #         self.logger.info(f"Gemini validation (last resort): agrees={result_json.get('agrees')}")
                    
            #         return {
            #             'agrees_with_ml': result_json.get('agrees', True),
            #             'confidence_boost': max(-0.15, min(0.15, result_json.get('confidence_adjustment', 0.0))),
            #             'reasoning': result_json.get('reasoning', 'LLM validation completed'),
            #             'alternative_diagnosis': result_json.get('alternative_diagnosis')
            #         }
                    
            #     except Exception as gemini_error:
            #         self.logger.warning(f"Gemini validation (last resort) failed: {gemini_error}")
            
            # If all LLMs fail, return neutral validation
            return {
                'agrees_with_ml': True,
                'confidence_boost': 0.0,
                'reasoning': 'LLM validation unavailable, using ML prediction only',
                'alternative_diagnosis': None
            }
            
        except Exception as e:
            self.logger.error(f"LLM validation error: {e}")
            return {
                'agrees_with_ml': True,
                'confidence_boost': 0.0,
                'reasoning': f'Validation error: {str(e)}',
                'alternative_diagnosis': None
            }

