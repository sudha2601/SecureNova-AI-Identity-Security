
import os
import jwt
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from jwt import PyJWKClient

load_dotenv()

DOMAIN = os.getenv("AUTH0_DOMAIN")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")
ISSUER = f"https://{DOMAIN}/"

jwks = PyJWKClient(
    f"https://{DOMAIN}/.well-known/jwks.json"
)

app = Flask(__name__)


@app.route("/chat", methods=["POST"])
def chat():

    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401

    token = auth_header.split(" ", 1)[1]

    try:
        signing_key = jwks.get_signing_key_from_jwt(token)

        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=ISSUER,
            leeway=0
        )

        scopes = claims.get("scope", "").split()

        if "read:ai-data" not in scopes:
            return jsonify({"error": "Insufficient scope"}), 403

        return jsonify({
            "message": "AI chat request successful",
            "status": "200 OK"
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({
            "error": "Unauthorized",
            "message": "Access token has expired"
        }), 401

    except jwt.InvalidTokenError:
        return jsonify({
            "error": "Unauthorized",
            "message": "Invalid access token"
        }), 401


if __name__ == "__main__":
    print("SecureNova AI API running on port 5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
