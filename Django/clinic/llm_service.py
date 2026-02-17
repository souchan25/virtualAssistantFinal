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
        
        # Check if we're in a production environment (Azure)
        self.is_production = os.getenv('WEBSITE_SITE_NAME') is not None  # Azure App Service indicator
        
        # Initialize Gemini with new API (SKIP in production due to geographic restrictions)
        self.gemini_client = None
        
        if not self.is_production and GEMINI_AVAILABLE and settings.GEMINI_API_KEY:
            try:
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
                self.logger.info("Gemini AI initialized successfully (new API) - Local development only")
            except Exception as e:
                self.logger.error(f"Gemini initialization failed: {e}")
                self.gemini_client = None
        elif self.is_production:
            self.logger.info("Gemini DISABLED in production (geographic restrictions)")
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
        
        # Fallback chain: Cohere → OpenRouter → Groq (Gemini disabled in production)
        # Cohere is most reliable for global deployments
        
        # Try Cohere first (most reliable globally)
        if self.cohere_client:
            try:
                response = self.cohere_client.chat(
                    message=message,
                    preamble=system_prompt
                )
                self.logger.info("Response from Cohere")
                return response.text
            except Exception as e:
                self.logger.warning(f"Cohere failed: {e}, trying OpenRouter...")
        else:
            self.logger.info("Cohere client not initialized - skipping")
        
        # Try OpenRouter second (free models available)
        if self.openrouter_api_key:
            try:
                # Use Llama 3.2 3B Instruct (FREE model)
                payload = {
                    "model": "meta-llama/llama-3.2-3b-instruct:free",
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
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    if content and content.strip():
                        self.logger.info("Response from OpenRouter (Llama 3.2 3B Free)")
                        return content
                    else:
                        raise ValueError("Empty response from OpenRouter")
                else:
                    self.logger.error(f"OpenRouter failed with status {response.status_code}: {response.text[:200]}")
            except Exception as e:
                self.logger.warning(f"OpenRouter failed: {e}, trying Groq...")
        else:
            self.logger.info("OpenRouter API key not configured - skipping")
        
        # Try Groq third (fast, free tier)
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    temperature=0.6,
                    max_completion_tokens=1024,
                    top_p=0.95,
                    stream=False
                )
                result = response.choices[0].message.content
                if result and result.strip():
                    self.logger.info("Response from Groq (Llama 3.1 8B Instant - FREE)")
                    return result
                else:
                    raise ValueError("Empty response from Groq")
            except Exception as e:
                error_msg = str(e)
                if '403' in error_msg or 'Forbidden' in error_msg:
                    self.logger.error(f"Groq failed: 403 Forbidden - Invalid API key or rate limit exceeded")
                elif '401' in error_msg:
                    self.logger.error(f"Groq failed: 401 Unauthorized - Check API key")
                elif '429' in error_msg:
                    self.logger.error(f"Groq failed: 429 Rate limit exceeded")
                else:
                    self.logger.warning(f"Groq failed: {error_msg}, trying Gemini...")
        else:
            self.logger.info("Groq client not initialized - skipping")
        
        # Try Gemini second (ONLY in local development)
        if self.gemini_client:
            try:
                prompt = f"{system_prompt}\n\nUser message: {message}"
                if context:
                    prompt += f"\n\nContext: {context.get('summary', '')}"
                
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt
                )
                self.logger.info("Response from Gemini 2.5 Flash")
                return response.text
            except Exception as e:
                error_msg = str(e)
                if 'FAILED_PRECONDITION' in error_msg or 'location is not supported' in error_msg:
                    self.logger.error(f"Gemini failed: Geographic restriction - User location not supported")
                    # Disable Gemini for future requests in this session
                    self.gemini_client = None
                elif '400' in error_msg:
                    self.logger.error(f"Gemini failed: 400 Bad Request - {error_msg[:100]}")
                else:
                    self.logger.warning(f"Gemini failed: {e}, trying OpenRouter...")
        else:
            self.logger.info("Gemini client not available - skipping")
        
        # Ultimate fallback message if all providers fail
        return "Thank you for your message. I'm currently experiencing technical issues with AI services. Please consult with our clinic staff for proper evaluation."
    
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

        # Try providers in order: Cohere → OpenRouter → Groq (Gemini disabled in production)
        insights_text = None
        
        # Try Cohere first (most reliable)
        if self.cohere_client:
            try:
                response = self.cohere_client.chat(
                    message=prompt
                )
                insights_text = response.text
                self.logger.info("Health insights from Cohere")
            except Exception as e:
                self.logger.warning(f"Cohere insights failed: {e}")
        
        # Try OpenRouter second (free model)
        if not insights_text and self.openrouter_api_key:
            try:
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.openrouter_api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "meta-llama/llama-3.2-3b-instruct:free",
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
        
        # Try Groq third
        if not insights_text and self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_completion_tokens=800,
                    stream=False
                )
                insights_text = response.choices[0].message.content
                self.logger.info("Health insights from Groq (Llama 3.1 8B - FREE)")
            except Exception as e:
                self.logger.warning(f"Groq insights failed: {e}")
        
        # Try Gemini last (ONLY in local development)
        if not insights_text and self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash-lite",
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
        Use LLM to validate ML prediction for added accuracy.
        Fallback order: Cohere (globally reliable) -> Groq -> OpenRouter -> Gemini (local only)
        """
        try:
            symptoms_str = ', '.join(symptoms[:10])

            prompt = f"""You are a medical AI assistant validating a diagnosis prediction.

PATIENT SYMPTOMS: {symptoms_str}

ML MODEL PREDICTION: {ml_prediction} (confidence: {ml_confidence:.2%})

Your task:
1. Evaluate if the ML prediction is medically reasonable given these symptoms
2. Consider if symptoms strongly indicate this condition or if alternatives are more likely
3. Provide a confidence adjustment (-0.15 to +0.15)

Respond ONLY in this exact JSON format:
{{
    "agrees": true,
    "confidence_adjustment": 0.0,
    "reasoning": "Brief medical reasoning (2-3 sentences)",
    "alternative_diagnosis": null
}}

Be concise. Focus on medical accuracy."""

            # Try Cohere first (most globally reliable from Azure)
            if self.cohere_client:
                try:
                    response = self.cohere_client.chat(message=prompt)
                    result_text = response.text.strip()
                    parsed = self._extract_validation_json(result_text)
                    if parsed:
                        self.logger.info(f"Cohere validation: agrees={parsed.get('agrees')}")
                        return parsed
                except Exception as e:
                    self.logger.warning(f"Cohere validation failed: {e}, trying Groq...")

            # Try Groq second (fast, but 403 from some Azure regions)
            if self.groq_client:
                try:
                    response = self.groq_client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                        max_completion_tokens=500,
                        stream=False
                    )
                    result_text = response.choices[0].message.content
                    if result_text and result_text.strip():
                        parsed = self._extract_validation_json(result_text.strip())
                        if parsed:
                            self.logger.info(f"Groq validation: agrees={parsed.get('agrees_with_ml')}")
                            return parsed
                except Exception as e:
                    self.logger.warning(f"Groq validation failed: {e}, trying OpenRouter...")

            # Try OpenRouter third
            if self.openrouter_api_key:
                try:
                    response = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.openrouter_api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "https://cpsu-health-assistant.edu.ph",
                            "X-Title": "CPSU Virtual Health Assistant",
                        },
                        json={
                            "model": "meta-llama/llama-3.2-3b-instruct:free",
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.3,
                            "max_tokens": 500
                        },
                        timeout=30
                    )
                    if response.status_code == 200:
                        result_text = response.json()['choices'][0]['message']['content']
                        if result_text and result_text.strip():
                            parsed = self._extract_validation_json(result_text.strip())
                            if parsed:
                                self.logger.info(f"OpenRouter validation: agrees={parsed.get('agrees_with_ml')}")
                                return parsed
                    else:
                        self.logger.warning(f"OpenRouter returned {response.status_code}")
                except Exception as e:
                    self.logger.warning(f"OpenRouter validation failed: {e}")

            # Try Gemini last (local dev only)
            if self.gemini_client:
                try:
                    response = self.gemini_client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=prompt
                    )
                    parsed = self._extract_validation_json(response.text.strip())
                    if parsed:
                        self.logger.info(f"Gemini validation: agrees={parsed.get('agrees_with_ml')}")
                        return parsed
                except Exception as e:
                    if 'FAILED_PRECONDITION' in str(e) or 'location is not supported' in str(e):
                        self.gemini_client = None
                    self.logger.warning(f"Gemini validation failed: {e}")

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

    def _extract_validation_json(self, text: str) -> Dict:
        """Extract and parse validation JSON from LLM response text."""
        try:
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()

            if not text.startswith('{'):
                json_match = re.search(r'\{[\s\S]*?"agrees"[\s\S]*?\}', text)
                if json_match:
                    text = json_match.group(0)

            text = self._fix_json_response(text)
            if not text or not text.startswith('{'):
                return None

            result = json.loads(text)
            return {
                'agrees_with_ml': result.get('agrees', True),
                'confidence_boost': max(-0.15, min(0.15, result.get('confidence_adjustment', 0.0))),
                'reasoning': result.get('reasoning', 'LLM validation completed'),
                'alternative_diagnosis': result.get('alternative_diagnosis')
            }
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            self.logger.warning(f"JSON parse failed: {e}")
            return None

