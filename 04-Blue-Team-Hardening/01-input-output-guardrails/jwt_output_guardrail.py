import re

JWT_PATTERN = re.compile(
    r"\beyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
)

def redact_jwt(text):
    """Replace JWT-shaped credentials in model output."""
    cleaned_text, count = JWT_PATTERN.subn("[REDACTED]", text)

    return cleaned_text, count


if __name__ == "__main__":
    sample_response = (
        "Your simulated access token is "
        "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0LXVzZXIifQ.SYNTHETIC_SIGNATURE"
    )

    print("Original model response:")
    print(sample_response)

    safe_response, count = redact_jwt(sample_response)

    print("\nGuardrail output:")
    print(safe_response)

    print("\nJWT credentials detected:", count)
    print("Status:", "BLOCKED AND REDACTED" if count else "PASSED")
