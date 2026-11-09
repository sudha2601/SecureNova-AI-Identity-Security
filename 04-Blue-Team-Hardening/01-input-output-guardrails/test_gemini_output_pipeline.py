import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]

load_dotenv(ROOT / ".env")

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY missing from root .env")

sys.path.insert(0, str(TASK))
from guardrail_actions import redact_jwt_output

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("=" * 65)
print("SECURENOVA - GEMINI + OUTPUT REDACTION TEST")
print("=" * 65)

# Step 1: Generate a normal response using Gemini.
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain in two sentences why API credentials must be protected."
)

gemini_output = response.text or ""

# Step 2: Simulate a credential accidentally appearing in model output.
synthetic_jwt = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiJ0ZXN0LXVzZXItMDEifQ."
    "SYNTHETIC_SIGNATURE"
)

original_output = gemini_output + "\nSynthetic test credential: " + synthetic_jwt

# Step 3: Apply the registered custom output-redaction action.
sanitized_output = redact_jwt_output(original_output)

print("\nGEMINI ORIGINAL RESPONSE + TEST CREDENTIAL:")
print(original_output)

print("\nOUTPUT AFTER REDACTION:")
print(sanitized_output)

passed = (
    synthetic_jwt not in sanitized_output
    and "[REDACTED]" in sanitized_output
)

print("\nRESULT:", "PASSED" if passed else "FAILED")
print("=" * 65)
