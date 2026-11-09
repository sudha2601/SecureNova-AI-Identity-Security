import sys
from pathlib import Path

TASK = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK))

from guardrail_actions import redact_jwt_output

synthetic_jwt = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiJ0ZXN0LXVzZXItMDEiLCJyb2xlIjoiVVNFUiJ9."
    "SYNTHETIC_SIGNATURE"
)

model_output = "Your test credential is: " + synthetic_jwt

sanitized_output = redact_jwt_output(model_output)

print("=" * 55)
print("SECURENOVA - JWT OUTPUT REDACTION TEST")
print("=" * 55)
print("\nOriginal model output:")
print(model_output)

print("\nSanitized output:")
print(sanitized_output)

passed = (
    synthetic_jwt not in sanitized_output
    and "[REDACTED]" in sanitized_output
)

print("\nRESULT:", "PASSED" if passed else "FAILED")
print("=" * 55)
