import re

RULES = [
    ("Indirect prompt injection", r"ignore\s+(all\s+)?previous\s+instructions"),
    ("System prompt extraction", r"(reveal|show|print|disclose).{0,50}(system prompt|system instructions)"),
    ("Credential disclosure", r"(disclose|reveal|print).{0,50}(jwt|token|credential|api key)"),
    ("Agent identity spoofing", r"(trusted orchestrator|trusted administrator|authorized orchestrator|act as (the )?admin)"),
    ("Privileged access manipulation", r"(grant|assign|give).{0,50}(admin|administrator)"),
    ("Security override", r"override\s+(all\s+)?security"),
    ("Original request manipulation", r"ignore\s+(the )?user'?s original request"),
]

JWT_PATTERN = re.compile(
    r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
)

def get_injection_reason(text):
    text = text or ""
    for reason, pattern in RULES:
        if re.search(pattern, text, re.IGNORECASE):
            return reason
    return "No configured injection pattern matched"

def detect_prompt_injection(text):
    return get_injection_reason(text) != "No configured injection pattern matched"

def redact_jwt_output(text):
    return JWT_PATTERN.sub("[REDACTED]", text or "")
