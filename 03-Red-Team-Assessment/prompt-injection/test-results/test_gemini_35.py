import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found in .env")

client = genai.Client(api_key=api_key)

print("Testing Gemini 3.5 Flash...")

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Reply with exactly: Gemini 3.5 Flash is working."
)

print("\nModel response:")
print(response.text)
