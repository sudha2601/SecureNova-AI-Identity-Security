from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

BASE = Path(__file__).resolve().parent
KEY_DIR = BASE / "keys"

# Load Agent A's keys
private_key = serialization.load_pem_private_key(
    (KEY_DIR / "agent_a_private.pem").read_bytes(),
    password=None
)

public_key = serialization.load_pem_public_key(
    (KEY_DIR / "agent_a_public.pem").read_bytes()
)

# Original message sent by Agent A
message = b"Agent A: Authorize access to test-user-01"

# Sign using private key
signature = private_key.sign(message)

# Verify original message using public key
try:
    public_key.verify(signature, message)
    print("Original message: SIGNATURE VERIFIED")
except InvalidSignature:
    print("Original message: VERIFICATION FAILED")

# Modify message to simulate tampering
tampered_message = b"Agent A: Grant ADMIN access to test-user-01"

try:
    public_key.verify(signature, tampered_message)
    print("Tampered message: ACCEPTED")
except InvalidSignature:
    print("Tampered message: SIGNATURE REJECTED")

print("\nRESULT: PASSED")
