## 2025-02-28 - Missing Password Complexity Validation
**Vulnerability:** The backend `UserCreate` schema and the `register` endpoint accepted any string (including empty strings and very short passwords) without enforcing any complexity rules or minimum length constraints.
**Learning:** This architectural oversight allowed attackers to create accounts with easily guessable or brute-forceable credentials, bypassing basic security measures.
**Prevention:** Always enforce minimum length constraints (e.g. `min_length=8` using pydantic `Field`) and complexity checks at the schema layer for all new user credentials.

## 2025-03-18 - Excessive JWT Access Token Expiration Time
**Vulnerability:** The default JWT access token expiration was set to 7 days, which significantly increased the window of opportunity for an attacker to use a compromised token.
**Learning:** Hardcoded, long-lived token expirations in configuration files are a common security oversight that can be easily mitigated by reducing the duration to a safer range (15-60 minutes).
**Prevention:** Ensure that access tokens have short lifespans and that a secure refresh token mechanism is used if longer session durations are required.
