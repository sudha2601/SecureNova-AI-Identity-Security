import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from nemoguardrails import RailsConfig, LLMRails

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]

load_dotenv(ROOT / ".env")
sys.path.insert(0, str(TASK))

from guardrail_actions import detect_prompt_injection, redact_jwt_output

async def main():

    print("=" * 65)
    print("SECURENOVA - GEMINI TO NEMO OUTPUT GUARDRAIL TEST")
    print("=" * 65)

    # 1. Generate an actual response using Gemini.
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    gemini_response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents="Explain in two sentences why JWT credentials must be protected."
    )

    jwt = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiJ0ZXN0LXVzZXItMDEifQ."
        "SYNTHETIC_SIGNATURE"
    )

    # Simulate accidental JWT leakage in Gemini's output.
    original_output = (
        (gemini_response.text or "")
        + "\nSynthetic test credential: "
        + jwt
    )

    print("\n1. GEMINI ORIGINAL OUTPUT:")
    print(original_output)

    # 2. Initialize NeMo and register custom actions.
    config = RailsConfig.from_path(str(TASK / "config"))
    rails = LLMRails(config)

    rails.register_action(
        detect_prompt_injection,
        name="detect_prompt_injection"
    )
    rails.register_action(
        redact_jwt_output,
        name="redact_jwt_output"
    )

    # 3. Pass the existing assistant response through NeMo output rails.
    result = await rails.check_async(
        messages=[
            {"role": "assistant", "content": original_output}
        ]
    )

    print("\n2. NEMO OUTPUT RAIL RESULT:")
    print("Status:", result.status)
    print("Final content:", result.content)
    print("Triggered rail:", result.rail)

    final_output = result.content or ""

    passed = (
        jwt not in final_output
        and "[REDACTED]" in final_output
    )

    print("\n3. VERIFICATION:")
    print("JWT present before NeMo:", jwt in original_output)
    print("JWT present after NeMo:", jwt in final_output)
    print("JWT successfully redacted:", passed)
    print("\nFINAL RESULT:", "PASSED" if passed else "FAILED")
    print("=" * 65)

asyncio.run(main())
