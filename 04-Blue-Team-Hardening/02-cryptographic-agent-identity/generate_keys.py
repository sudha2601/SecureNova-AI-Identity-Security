from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

BASE = Path(__file__).resolve().parent
KEY_DIR = BASE / "keys"
KEY_DIR.mkdir(exist_ok=True)

# Generate Ed25519 key pair
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Save private key
private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Save public key
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

(KEY_DIR / "agent_a_private.pem").write_bytes(private_bytes)
(KEY_DIR / "agent_a_public.pem").write_bytes(public_bytes)

print("=" * 55)
print("SECURENOVA - ED25519 KEY GENERATION")
print("=" * 55)
print("Algorithm: Ed25519")
print("Private key: keys/agent_a_private.pem")
print("Public key : keys/agent_a_public.pem")
print("Private key generated:", (KEY_DIR / "agent_a_private.pem").exists())
print("Public key generated :", (KEY_DIR / "agent_a_public.pem").exists())
print("RESULT: PASSED")
print("=" * 55)
