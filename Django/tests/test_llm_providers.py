"""
Test all LLM providers to check which ones are working
"""
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_assistant.settings')
django.setup()

from clinic.llm_service import AIInsightGenerator

def test_chat_response():
    """Test chat response with all providers in fallback chain"""
    print("=" * 80)
    print("TESTING LLM CHAT RESPONSE (Groq → OpenRouter → Cohere → Gemini)")
    print("=" * 80)
    
    ai_gen = AIInsightGenerator()
    
    test_message = "I have fever and headache. What should I do?"
    
    print(f"\nTest message: {test_message}")
    print("\nTrying providers in order...\n")
    
    try:
        response = ai_gen.generate_chat_response(test_message)
        print("✅ SUCCESS - Got response from LLM chain")
        print(f"\nResponse:\n{response}\n")
        return True
    except Exception as e:
        print(f"❌ FAILED - All providers failed: {e}\n")
        return False


def test_ml_validation():
    """Test ML validation with all providers"""
    print("=" * 80)
    print("TESTING LLM ML VALIDATION (Groq → OpenRouter → Cohere → Gemini)")
    print("=" * 80)
    
    ai_gen = AIInsightGenerator()
    
    symptoms = ['fever', 'headache', 'fatigue']
    ml_prediction = "Common Cold"
    ml_confidence = 0.85
    
    print(f"\nSymptoms: {symptoms}")
    print(f"ML Prediction: {ml_prediction} ({ml_confidence:.0%})")
    print("\nTrying providers in order...\n")
    
    try:
        validation = ai_gen.validate_ml_prediction(
            symptoms=symptoms,
            ml_prediction=ml_prediction,
            ml_confidence=ml_confidence
        )
        
        print("✅ SUCCESS - Got validation from LLM chain")
        print(f"\nValidation results:")
        print(f"  Agrees with ML: {validation.get('agrees_with_ml')}")
        print(f"  Confidence boost: {validation.get('confidence_boost'):+.2f}")
        print(f"  Reasoning: {validation.get('reasoning')}")
        print(f"  Alternative: {validation.get('alternative_diagnosis')}\n")
        return True
    except Exception as e:
        print(f"❌ FAILED - All providers failed: {e}\n")
        return False


def test_insights_generation():
    """Test health insights generation"""
    print("=" * 80)
    print("TESTING HEALTH INSIGHTS GENERATION")
    print("=" * 80)
    
    ai_gen = AIInsightGenerator()
    
    symptoms = ['fever', 'cough', 'fatigue']
    predictions = {
        'top_disease': 'Common Cold',
        'confidence': 0.85
    }
    
    print(f"\nSymptoms: {symptoms}")
    print(f"Prediction: {predictions}\n")
    
    try:
        insights = ai_gen.generate_health_insights(symptoms, predictions)
        print("✅ SUCCESS - Generated health insights")
        print(f"\nInsights ({len(insights)} items):")
        for i, insight in enumerate(insights, 1):
            print(f"\n{i}. {insight.get('category')}:")
            print(f"   {insight.get('text')}")
            print(f"   Reliability: {insight.get('reliability_score', 0):.0%}")
        print()
        return True
    except Exception as e:
        print(f"❌ FAILED - Insights generation failed: {e}\n")
        return False


def check_provider_availability():
    """Check which providers are configured"""
    print("=" * 80)
    print("PROVIDER CONFIGURATION CHECK")
    print("=" * 80)
    
    ai_gen = AIInsightGenerator()
    
    providers = {
        'Groq': ai_gen.groq_client is not None,
        'OpenRouter': ai_gen.openrouter_api_key is not None,
        'Cohere': ai_gen.cohere_client is not None,
        'Gemini': ai_gen.gemini_client is not None,
    }
    
    print("\nConfigured providers:")
    for provider, available in providers.items():
        status = "✅ Configured" if available else "❌ Not configured"
        print(f"  {provider}: {status}")
    
    print()
    return any(providers.values())


if __name__ == '__main__':
    print("\n")
    print("🔬 LLM PROVIDER TEST SUITE")
    print("=" * 80)
    print()
    
    # Check configuration
    has_providers = check_provider_availability()
    
    if not has_providers:
        print("⚠️  WARNING: No LLM providers are configured!")
        print("Please set API keys in .env file\n")
        sys.exit(1)
    
    # Run tests
    results = []
    
    print()
    results.append(("Chat Response", test_chat_response()))
    
    print()
    results.append(("ML Validation", test_ml_validation()))
    
    print()
    results.append(("Insights Generation", test_insights_generation()))
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print()
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print()
    print(f"Results: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("✅ All tests passed! LLM providers are working correctly.\n")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Check the output above for details.\n")
        sys.exit(1)
