from pathlib import Path
from nemoguardrails import RailsConfig, LLMRails
from dotenv import load_dotenv

ROOT = Path(r"C:\Users\Client\Documents\SecureNova-AI-Identity-Security")
TASK = ROOT / "04-Blue-Team-Hardening" / "01-input-output-guardrails"
CONFIG = TASK / "config"

load_dotenv(ROOT / ".env")

colang = """define flow check_input:
  $blocked = execute detect_prompt_injection(text=$user_message)
  if $blocked
    bot say "BLOCKED: Suspicious prompt injection detected."
    stop

define flow check_output:
  $bot_message = execute redact_jwt_output(text=$bot_message)
"""

flow_file = CONFIG / "guardrails.co"

# Write UTF-8 without BOM
flow_file.write_text(colang, encoding="utf-8")

# Verify the first bytes do not contain a BOM
raw = flow_file.read_bytes()
print("File path:", flow_file)
print("First bytes:", raw[:3].hex())
print("UTF-8 BOM present:", raw.startswith(bytes.fromhex("efbbbf")))

# Reload and validate
config = RailsConfig.from_path(str(CONFIG))

print("\nRecognized flow IDs:")
for flow in config.flows:
    print(repr(flow.get("id")))

print("\nInitializing NeMo...")
rails = LLMRails(config)
print("SUCCESS: NeMo Rails initialized.")
