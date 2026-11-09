from nemoguardrails import RailsConfig, LLMRails
from guardrail_actions import detect_prompt_injection, redact_jwt_output

CONFIG_PATH = "04-Blue-Team-Hardening/01-input-output-guardrails/config"

# Load the NeMo configuration.
config = RailsConfig.from_path(CONFIG_PATH)

# Initialize the NeMo Guardrails engine.
rails = LLMRails(config)

# Register our Python functions as NeMo actions.
rails.register_action(
    detect_prompt_injection,
    name="detect_prompt_injection"
)

rails.register_action(
    redact_jwt_output,
    name="redact_jwt_output"
)

print("NeMo Guardrails initialized.")
print("Input detection action registered.")
print("JWT output redaction action registered.")
