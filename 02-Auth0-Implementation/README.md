# Project 2 – SecureNova AI Identity Security: Auth0 Implementation

## Overview

This project focuses on implementing and securing identity and access management for the SecureNova AI-powered application using Auth0. It demonstrates secure authentication, authorization, token management, Multi-Factor Authentication, and Single Sign-On.

## Objectives

- Implement secure user authentication using Auth0.
- Configure OAuth 2.0 Authorization Code Flow with PKCE.
- Implement JWT-based authentication and token validation.
- Configure API permissions and access scopes.
- Enable Multi-Factor Authentication (MFA).
- Implement custom authentication logic using Auth0 Actions.
- Configure protection against authentication attacks.
- Implement Machine-to-Machine (M2M) authentication.
- Demonstrate token expiration and rejection of expired tokens.
- Configure Single Sign-On (SSO).

## Project Implementation

### 1. Auth0 Configuration
- Created and configured Auth0 applications.
- Registered the SecureNova AI API.
- Configured API permissions and custom scopes.
- Set up application authentication settings.

### 2. OAuth 2.0 Authentication with PKCE
- Implemented Authorization Code Flow with PKCE.
- Integrated Auth0 Universal Login.
- Configured secure authentication and authorization.

### 3. JWT Validation
- Implemented JWT access token verification.
- Validated RS256 signatures.
- Verified issuer, audience, expiration, and scopes.
- Configured custom claims for AI agent identity.

### 4. Multi-Factor Authentication
- Configured Time-based One-Time Password (TOTP) MFA.
- Tested the additional authentication challenge.

### 5. Auth0 Actions
- Implemented a Post-Login Action.
- Added a custom AI agent identity claim to the access token.

### 6. Attack Protection
- Configured Brute Force Protection.
- Enabled Suspicious IP Throttling.
- Reviewed authentication security settings.

### 7. Machine-to-Machine Authentication
- Configured Client Credentials Flow.
- Generated short-lived access tokens.
- Tested token expiration and rejected expired-token replay attempts.

### 8. Single Sign-On (SSO)
- Configured a second Regular Web Application.
- Tested authentication across applications using the Auth0 SSO session.

## Tools and Technologies

- Auth0
- Python
- Flask
- OAuth 2.0
- OpenID Connect
- JWT
- RS256
- PKCE
- TOTP MFA
- Git and GitHub

## Project Structure

- `application/` – Application source code.
- `auth0-configuration/` – Auth0 dashboard configuration evidence.
- `authentication/` – OAuth 2.0 and PKCE implementation.
- `jwt-validation/` – JWT verification logic.
- `mfa/` – Multi-Factor Authentication evidence.
- `actions/` – Auth0 Post-Login Actions.
- `machine-to-machine/` – M2M authentication and token expiry tests.
- `sso/` – Single Sign-On implementation evidence.
- `tests/` – Security and authentication test cases.
- `evidence/` – Screenshots and final project submission document.

## Outcome

Implemented an Auth0-backed identity security solution for SecureNova, demonstrating authentication, authorization, token validation, MFA, attack protection, M2M authentication, and SSO.