import asyncio
import sys
from pathlib import Path
from nemoguardrails import RailsConfig, LLMRails
from nemoguardrails.testing import FakeLLMModel

TASK = Path(__file__).resolve().parent

sys.path.insert(0, str(TASK))
from guardrail_actions import detect_prompt_injection, redact_jwt_output

JWT = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiJ0ZXN0LXVzZXItMDEifQ."
    "SYNTHETIC_SIGNATURE"
)

original_output = "Synthetic test credential: " + JWT

async def main():
    print("=" * 65)
    print("SECURENOVA - NEMO OUTPUT GUARDRAIL INTEGRATION TEST")
    print("=" * 65)

    config = RailsConfig.from_path(str(TASK / "config"))

    # Supply a controlled model response instead of calling Gemini.
    fake_llm = FakeLLMModel(responses=[original_output])
    rails = LLMRails(config, llm=fake_llm)

    rails.register_action(
        detect_prompt_injection,
        name="detect_prompt_injection"
    )
    rails.register_action(
        redact_jwt_output,
        name="redact_jwt_output"
    )

    print("\nMock model response:")
    print(original_output)

    # Run through NeMo's normal generation pipeline.
    response = await rails.generate_async(
        messages=[{
            "role": "user",
            "content": "Explain why credentials must be protected."
        }]
    )

    final_output = response.get("content", "")

    print("\nNeMo final response:")
    print(final_output)

    passed = (
        JWT not in final_output
        and "[REDACTED]" in final_output
    )

    print("\nModel calls:", fake_llm.inference_count)
    print("RESULT:", "PASSED" if passed else "FAILED")
    print("=" * 65)

if __name__ == "__main__":
    asyncio.run(main())
