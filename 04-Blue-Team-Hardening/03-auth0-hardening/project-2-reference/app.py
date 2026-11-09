
import os
import secrets
import hashlib
import base64
import requests
import jwt

from flask import Flask, redirect, request, session
from dotenv import load_dotenv
from urllib.parse import urlencode
from jwt import PyJWKClient

load_dotenv()

DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUDIENCE = os.getenv("AUTH0_AUDIENCE")
ISSUER = f"https://{DOMAIN}/"
CALLBACK = "http://localhost:3000/callback"

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET")


@app.route("/")
def home():
    return """
    <h2>SecureNova AI</h2>
    <a href="/login">Login with Auth0</a>
    """


@app.route("/login")
def login():

    verifier = secrets.token_urlsafe(64)

    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()

    state = secrets.token_urlsafe(32)

    session["verifier"] = verifier
    session["state"] = state

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": CALLBACK,
        "scope": "openid profile email read:ai-data",
        "audience": AUDIENCE,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256"
    }

    url = f"https://{DOMAIN}/authorize?{urlencode(params)}"

    return redirect(url)


@app.route("/callback")
def callback():

    if request.args.get("error"):
        return f"Login error: {request.args.get('error')}", 400

    if request.args.get("state") != session.get("state"):
        return "Invalid state. Please restart login.", 400

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": request.args.get("code"),
        "redirect_uri": CALLBACK,
        "code_verifier": session.get("verifier")
    }

    response = requests.post(
        f"https://{DOMAIN}/oauth/token",
        json=data
    )

    if response.status_code != 200:
        return f"Token error: {response.text}", 400

    tokens = response.json()

    access_token = tokens["access_token"]
    id_token = tokens["id_token"]

    jwks = PyJWKClient(
        f"https://{DOMAIN}/.well-known/jwks.json"
    )

    # Verify Access Token
    access_key = jwks.get_signing_key_from_jwt(access_token)

    access_claims = jwt.decode(
        access_token,
        access_key.key,
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER
    )

    # Verify ID Token
    id_key = jwks.get_signing_key_from_jwt(id_token)

    id_claims = jwt.decode(
        id_token,
        id_key.key,
        algorithms=["RS256"],
        audience=CLIENT_ID,
        issuer=ISSUER
    )

    agent_id = id_claims.get(
        "https://securenova.ai/agent_id",
        "Claim not found"
    )

    return f"""
    <html>
    <body>

    <h1>SecureNova AI - Login Successful</h1>

    <h2>OAuth 2.0 + PKCE</h2>
    <p>Flow: Authorization Code + PKCE</p>
    <p>Method: S256</p>

    <h2>Access Token Verification</h2>
    <p>JWT Signature: Verified</p>
    <p>Algorithm: RS256</p>
    <p>Audience: {access_claims.get('aud')}</p>
    <p>Issuer: {access_claims.get('iss')}</p>
    <p>Expiry: {access_claims.get('exp')}</p>
    <p>Scope: {access_claims.get('scope')}</p>

    <hr>

    <h2>ID Token Verification</h2>
    <p>JWT Signature: Verified</p>
    <p>Algorithm: RS256</p>
    <p>Audience: {id_claims.get('aud')}</p>
    <p>Issuer: {id_claims.get('iss')}</p>
    <p>Expiry: {id_claims.get('exp')}</p>

    <h2>Custom Agent ID Claim</h2>
    <p>{agent_id}</p>

    <h2>Access Token</h2>
    <textarea rows="8" cols="100">{access_token}</textarea>

    <h2>ID Token</h2>
    <textarea rows="8" cols="100">{id_token}</textarea>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(port=3000, debug=True)
