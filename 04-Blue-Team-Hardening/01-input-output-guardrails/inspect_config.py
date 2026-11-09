import os
from pathlib import Path
from dotenv import load_dotenv
from nemoguardrails import RailsConfig, LLMRails

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / "04-Blue-Team-Hardening" / "01-input-output-guardrails"

load_dotenv(ROOT / ".env")

config = RailsConfig.from_path(str(TASK / "config"))

print("Recognized flow IDs:")
for flow in config.flows:
    print("-", repr(flow.get("id")))

print("\nCreating NeMo Rails...")
rails = LLMRails(config)

print("SUCCESS: NeMo Rails initialized without configuration errors.")
