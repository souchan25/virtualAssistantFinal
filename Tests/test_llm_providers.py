"""
Test LLM Providers and Fallback Chain
Tests each provider individually and shows fallback order
"""

import os
import sys
from pathlib import Path

# Add Django project to path
django_path = Path(__file__).parent.parent / 'Django'
sys.path.insert(0, str(django_path))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_assistant.settings')
import django
django.setup()

from clinic.llm_service import AIInsightGenerator
import logging

# Setup logging to see which provider is used
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)


def print_status(provider, status, message=""):
    """Print provider status"""
    status_symbol = "✓" if status else "✗"
    status_text = "WORKING" if status else "FAILED"
    color_code = "\033[92m" if status else "\033[91m"
    reset_code = "\033[0m"
    
    print(f"{color_code}{status_symbol} {provider:20} - {status_text}{reset_code}")
    if message:
        print(f"  └─ {message}")


def test_individual_providers():
    """Test each LLM provider individually"""
    print_header("TESTING INDIVIDUAL LLM PROVIDERS")
    
    ai_gen = AIInsightGenerator()
    test_message = "I have a fever and headache. What should I do?"
    
    results = {}
    
    # Test 1: Groq (Llama 3.3 70B)
    print("\n[1/4] Testing Groq (Llama 3.3 70B Versatile)...")
    if ai_gen.groq_client:
        try:
            response = ai_gen.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a health assistant."},
                    {"role": "user", "content": test_message}
                ],
                temperature=0.6,
                max_tokens=100
            )
            result = response.choices[0].message.content
            if result and result.strip():
                print_status("Groq (Llama 3.3 70B)", True, f"Response: {result[:80]}...")
                results['groq'] = True
            else:
                print_status("Groq (Llama 3.3 70B)", False, "Empty response")
                results['groq'] = False
        except Exception as e:
            print_status("Groq (Llama 3.3 70B)", False, f"Error: {str(e)[:60]}")
            results['groq'] = False
    else:
        print_status("Groq (Llama 3.3 70B)", False, "Client not initialized (check API key)")
        results['groq'] = False
    
    # Test 2: OpenRouter (Qwen 3 Next 80B)
    print("\n[2/4] Testing OpenRouter (Qwen 3 Next 80B Free)...")
    if ai_gen.openrouter_api_key:
        try:
            import requests
            import json
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {ai_gen.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://cpsu-health-assistant.edu.ph",
                    "X-Title": "CPSU Virtual Health Assistant",
                },
                data=json.dumps({
                    "model": "qwen/qwen3-next-80b-a3b-instruct:free",
                    "messages": [{"role": "user", "content": test_message}],
                    "max_tokens": 100
                }),
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                if result and result.strip():
                    print_status("OpenRouter (Qwen 3)", True, f"Response: {result[:80]}...")
                    results['openrouter'] = True
                else:
                    print_status("OpenRouter (Qwen 3)", False, "Empty response")
                    results['openrouter'] = False
            else:
                print_status("OpenRouter (Qwen 3)", False, f"HTTP {response.status_code}: {response.text[:100]}")
                results['openrouter'] = False
        except Exception as e:
            print_status("OpenRouter (Qwen 3)", False, f"Error: {str(e)[:60]}")
            results['openrouter'] = False
    else:
        print_status("OpenRouter (Qwen 3)", False, "API key not configured")
        results['openrouter'] = False
    
    # Test 3: Cohere
    print("\n[3/4] Testing Cohere...")
    if hasattr(ai_gen, 'cohere_client') and ai_gen.cohere_client:
        try:
            response = ai_gen.cohere_client.chat(
                message=test_message,
                preamble="You are a health assistant."
            )
            result = response.text
            if result and result.strip():
                print_status("Cohere", True, f"Response: {result[:80]}...")
                results['cohere'] = True
            else:
                print_status("Cohere", False, "Empty response")
                results['cohere'] = False
        except Exception as e:
            print_status("Cohere", False, f"Error: {str(e)[:60]}")
            results['cohere'] = False
    else:
        print_status("Cohere", False, "Client not initialized (check API key)")
        results['cohere'] = False
    
    # Test 4: Gemini (with multiple model fallbacks)
    print("\n[4/4] Testing Gemini (with fallbacks)...")
    if ai_gen.gemini_client:
        gemini_models = [
            ("gemini-2.5-flash-lite", "Gemini 2.5 Flash Lite")
            # ("gemini-2.0-flash-lite", "Gemini 2.0 Flash Lite")
            # ("gemini-1.5-flash", "Gemini 1.5 Flash")
        ]
        
        gemini_success = False
        for model_name, display_name in gemini_models:
            try:
                response = ai_gen.gemini_client.models.generate_content(
                    model=model_name,
                    contents=f"You are a health assistant. User says: {test_message}"
                )
                result = response.text
                if result and result.strip():
                    print_status(f"Gemini ({display_name})", True, f"Response: {result[:80]}...")
                    results['gemini'] = True
                    gemini_success = True
                    break
            except Exception as e:
                if "404" in str(e) or "not found" in str(e).lower():
                    continue  # Try next model
                elif "403" in str(e) or "PERMISSION_DENIED" in str(e):
                    print_status(f"Gemini ({display_name})", False, f"Permission denied: {str(e)[:60]}")
                    break  # Don't try other models if permission denied
                else:
                    continue  # Try next model
        
        if not gemini_success:
            print_status("Gemini (All models)", False, "All models failed or unavailable")
            results['gemini'] = False
    else:
        print_status("Gemini", False, "Client not initialized (check API key)")
        results['gemini'] = False
    
    return results


def test_fallback_chain():
    """Test the fallback chain in action"""
    print_header("TESTING FALLBACK CHAIN")
    
    ai_gen = AIInsightGenerator()
    test_message = "I have fever, cough, and fatigue. Should I be worried?"
    
    print("\nTest Message:", test_message)
    print("\nFallback Order:")
    print("  1. Groq (Llama 3.3 70B Versatile) - Fast, free tier")
    print("  2. OpenRouter (StepFun Step 3.5 Flash) - Free alternative")
    print("  3. Cohere - Another fallback")
    print("  4. Gemini (multiple models) - Last resort (rate limited)")
    print("\nExecuting fallback chain...")
    
    try:
        response = ai_gen.generate_chat_response(test_message)
        print("\n✓ Fallback chain succeeded!")
        print(f"\nResponse (first 200 chars):\n{response[:200]}...")
        return True
    except Exception as e:
        print(f"\n✗ Fallback chain failed: {e}")
        return False


def test_ml_validation():
    """Test ML validation with LLM"""
    print_header("TESTING ML VALIDATION (HYBRID SYSTEM)")
    
    ai_gen = AIInsightGenerator()
    
    print("\nTest Case: ML predicted 'Common Cold' with 85% confidence")
    print("Symptoms: fever, cough, fatigue")
    print("\nValidation Fallback Order:")
    print("  1. Groq (Llama 3.3 70B)")
    print("  2. OpenRouter (StepFun Step 3.5 Flash)")
    print("  3. Cohere")
    print("\nExecuting validation...")
    
    try:
        result = ai_gen.validate_ml_prediction(
            symptoms=['fever', 'cough', 'fatigue'],
            ml_prediction='Common Cold',
            ml_confidence=0.85
        )
        
        print("\n✓ ML Validation succeeded!")
        print(f"\nValidation Results:")
        print(f"  Agrees with ML: {result['agrees_with_ml']}")
        print(f"  Confidence Boost: {result['confidence_boost']:+.2%}")
        print(f"  Reasoning: {result['reasoning'][:150]}...")
        if result.get('alternative_diagnosis'):
            print(f"  Alternative: {result['alternative_diagnosis']}")
        
        return True
    except Exception as e:
        print(f"\n✗ ML Validation failed: {e}")
        return False


def test_health_insights():
    """Test health insights generation"""
    print_header("TESTING HEALTH INSIGHTS GENERATION")
    
    ai_gen = AIInsightGenerator()
    
    print("\nTest Case: Generate insights for Common Cold")
    print("Insights Fallback Order:")
    print("  1. Groq (Llama 3.3 70B)")
    print("  2. OpenRouter (StepFun Step 3.5 Flash)")
    print("  3. Gemini (multiple models)")
    print("\nExecuting insights generation...")
    
    try:
        predictions = {
            'predicted_disease': 'Common Cold',
            'confidence_score': 0.87
        }
        
        insights = ai_gen.generate_health_insights(
            symptoms=['fever', 'cough', 'runny nose'],
            predictions=predictions
        )
        
        print("\n✓ Health Insights succeeded!")
        print(f"\nGenerated {len(insights)} insights:")
        for i, insight in enumerate(insights, 1):
            print(f"\n  [{i}] {insight['category']}")
            print(f"      {insight['text'][:100]}...")
            print(f"      Reliability: {insight['reliability_score']:.0%}")
        
        return True
    except Exception as e:
        print(f"\n✗ Health Insights failed: {e}")
        return False


def print_summary(results):
    """Print summary of all tests"""
    print_header("TEST SUMMARY")
    
    working_providers = sum(1 for v in results.values() if v)
    total_providers = len(results)
    
    print(f"\nProviders Working: {working_providers}/{total_providers}")
    print("\nStatus by Provider:")
    
    for provider, status in results.items():
        status_symbol = "✓" if status else "✗"
        color_code = "\033[92m" if status else "\033[91m"
        reset_code = "\033[0m"
        print(f"  {color_code}{status_symbol} {provider.capitalize()}{reset_code}")
    
    print("\n" + "="*70)
    
    if working_providers == 0:
        print("⚠️  WARNING: No LLM providers are working!")
        print("   System will use fallback responses only.")
        print("   Check your API keys in Django/.env")
    elif working_providers < total_providers:
        print("⚠️  Some providers are not working, but fallback chain is active.")
    else:
        print("✓ All LLM providers are working!")
    
    print("="*70)


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  CPSU VIRTUAL HEALTH ASSISTANT - LLM PROVIDER TEST")
    print("="*70)
    
    # Test individual providers
    provider_results = test_individual_providers()
    
    # Test fallback chain
    print("\n")
    fallback_works = test_fallback_chain()
    
    # Test ML validation
    print("\n")
    validation_works = test_ml_validation()
    
    # Test health insights
    print("\n")
    insights_works = test_health_insights()
    
    # Print summary
    print("\n")
    print_summary(provider_results)
    
    # Final status
    print("\nIntegration Tests:")
    print(f"  {'✓' if fallback_works else '✗'} Chat Fallback Chain")
    print(f"  {'✓' if validation_works else '✗'} ML Validation (Hybrid System)")
    print(f"  {'✓' if insights_works else '✗'} Health Insights Generation")
    
    print("\n" + "="*70)
    print("  TEST COMPLETE")
    print("="*70 + "\n")
