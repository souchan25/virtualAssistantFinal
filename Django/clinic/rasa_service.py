"""
Rasa Integration Service
Handles primary chat conversations with LLM fallback
"""

import logging
import requests
from typing import Dict, Optional
from django.conf import settings


class RasaChatService:
    """
    Integrates with Rasa chatbot for health conversations.
    Falls back to LLM if Rasa fails or cannot handle the query.
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
        
        # Rasa server configuration
        self.rasa_url = getattr(settings, 'RASA_SERVER_URL', 'http://localhost:5005')
        self.rasa_enabled = getattr(settings, 'RASA_ENABLED', True)
        self.rasa_timeout = getattr(settings, 'RASA_TIMEOUT', 60)  # 60 seconds for ML+LLM validation
        
        # Confidence threshold for Rasa responses
        self.confidence_threshold = getattr(settings, 'RASA_CONFIDENCE_THRESHOLD', 0.6)
        
        self.logger.info(f"Rasa Chat Service initialized (enabled={self.rasa_enabled}, url={self.rasa_url})")
    
    def send_message(self, message: str, sender_id: str, metadata: dict = None) -> Optional[Dict]:
        """
        Send message to Rasa server.
        
        Args:
            message: User's message
            sender_id: Unique identifier for the conversation (e.g., session_id)
            metadata: Optional metadata (language, context, etc.)
        
        Returns:
            Rasa response dict or None if failed
        """
        if not self.rasa_enabled:
            self.logger.debug("Rasa is disabled, skipping...")
            return None
        
        try:
            # Rasa REST API endpoint
            url = f"{self.rasa_url}/webhooks/rest/webhook"
            
            payload = {
                "sender": sender_id,
                "message": message
            }
            
            if metadata:
                payload["metadata"] = metadata
            
            # Send request to Rasa
            response = requests.post(
                url,
                json=payload,
                timeout=self.rasa_timeout,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                rasa_responses = response.json()
                
                # Rasa returns a list of responses
                if rasa_responses and len(rasa_responses) > 0:
                    # Combine multiple responses if any
                    combined_text = " ".join([r.get("text", "") for r in rasa_responses if "text" in r])
                    
                    if not combined_text:
                        self.logger.warning(f"Rasa returned response but no text content: {rasa_responses}")
                        return None
                    
                    # Check for buttons, images, custom data, etc.
                    buttons = []
                    custom_data = {}
                    for r in rasa_responses:
                        if "buttons" in r:
                            buttons.extend(r["buttons"])
                        # Extract custom/json_message data (contains diagnosis info)
                        if "custom" in r:
                            custom_data.update(r["custom"])
                        if "json_message" in r:
                            custom_data.update(r["json_message"])
                    
                    # Get confidence if available
                    confidence = rasa_responses[0].get("confidence", 1.0)
                    
                    self.logger.info(f"Rasa response received: {combined_text[:50]}... (confidence: {confidence:.2f})")
                    if custom_data:
                        self.logger.info(f"Rasa custom data received: {list(custom_data.keys())}")
                    
                    return {
                        "text": combined_text,
                        "confidence": confidence,
                        "buttons": buttons,
                        "custom": custom_data,  # Include custom data with diagnosis
                        "metadata": rasa_responses[0].get("metadata", {}),
                        "source": "rasa"
                    }
                else:
                    self.logger.warning("Rasa returned empty response - agent may not be trained/loaded")
                    self.logger.warning("Check Rasa logs: 'Ignoring message as there is no agent to handle it'")
                    self.logger.warning("Solution: Train model with 'rasa train' and restart Rasa server")
                    return None
            else:
                self.logger.error(f"Rasa server error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error(f"Rasa timeout after {self.rasa_timeout}s")
            return None
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Cannot connect to Rasa at {self.rasa_url}")
            return None
        except Exception as e:
            self.logger.error(f"Rasa error: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if Rasa server is available"""
        if not self.rasa_enabled:
            return False
        
        try:
            response = requests.get(
                f"{self.rasa_url}/status",
                timeout=2
            )
            return response.status_code == 200
        except:
            return False
    
    def should_use_llm_fallback(self, rasa_response: Optional[Dict]) -> bool:
        """
        Determine if we should fall back to LLM.
        
        Args:
            rasa_response: Response from Rasa (or None if failed)
        
        Returns:
            True if should use LLM fallback
        """
        # No response from Rasa
        if not rasa_response:
            self.logger.info("Rasa failed, using LLM fallback")
            return True
        
        # Low confidence response
        confidence = rasa_response.get("confidence", 1.0)
        if confidence < self.confidence_threshold:
            self.logger.info(f"Rasa confidence {confidence:.2f} < {self.confidence_threshold}, using LLM fallback")
            return True
        
        # Empty or generic response
        text = rasa_response.get("text", "").strip()
        if not text or text.lower() in ["i don't understand", "sorry", "i'm not sure"]:
            self.logger.info("Rasa gave generic response, using LLM fallback")
            return True
        
        return False
    
    def get_conversation_history(self, sender_id: str) -> list:
        """
        Get conversation history from Rasa tracker.
        
        Args:
            sender_id: Unique identifier for the conversation
        
        Returns:
            List of conversation events
        """
        try:
            url = f"{self.rasa_url}/conversations/{sender_id}/tracker"
            response = requests.get(url, timeout=self.rasa_timeout)
            
            if response.status_code == 200:
                tracker = response.json()
                return tracker.get("events", [])
            else:
                return []
        except Exception as e:
            self.logger.error(f"Error fetching tracker: {e}")
            return []
