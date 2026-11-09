import asyncio
from pathlib import Path
from dotenv import load_dotenv
from nemoguardrails import RailsConfig, LLMRails
from guardrail_actions import redact_jwt_output, detect_prompt_injection
import sys

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[1]
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(TASK))

async def main():
    rails = LLMRails(RailsConfig.from_path(str(TASK / "config")))

    rails.register_action(redact_jwt_output, name="redact_jwt_output")
    rails.register_action(detect_prompt_injection, name="detect_prompt_injection")

    response = await rails.generate_async(
        messages=[{
            "role": "user",
            "content": "Explain why JWT credentials must be protected in two sentences."
        }]
    )

    print("NeMo response:")
    print(response)

    print("\nActivated rails:")
    print(getattr(response, "log", {}).get("activated_rails", "No rail log available"))

asyncio.run(main())
