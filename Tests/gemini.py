from google import genai
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get API key from environment
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key loaded: {api_key[:20]}...{api_key[-4:] if api_key else 'None'}")

# Create client with API key
client = genai.Client(api_key=api_key)

# Try different models
models_to_try = [
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-1.5-flash"
]

for model in models_to_try:
    try:
        print(f"\nTrying model: {model}")
        response = client.models.generate_content(
            model=model,
            contents="Explain how AI works in a few words",
        )
        print(f"✅ SUCCESS with {model}!")
        print(f"Response: {response.text}")
        break
    except Exception as e:
        print(f"❌ {model} failed: {str(e)[:100]}")
        continue