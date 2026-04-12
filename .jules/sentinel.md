## 2025-02-28 - Missing Password Complexity Validation
**Vulnerability:** The backend `UserCreate` schema and the `register` endpoint accepted any string (including empty strings and very short passwords) without enforcing any complexity rules or minimum length constraints.
**Learning:** This architectural oversight allowed attackers to create accounts with easily guessable or brute-forceable credentials, bypassing basic security measures.
**Prevention:** Always enforce minimum length constraints (e.g. `min_length=8` using pydantic `Field`) and complexity checks at the schema layer for all new user credentials.

## 2025-03-03 - Hardcoded Database Credentials in Docker Compose
**Vulnerability:** The `docker-compose.yml` file contained hardcoded database credentials (username, password, and connection string) in plain text.
**Learning:** Storing secrets in version-controlled configuration files exposes sensitive information to anyone with access to the repository, increasing the risk of unauthorized database access.
**Prevention:** Use environment variables and variable substitution in configuration files. Provide a `.env.example` file to guide environment setup without exposing actual secrets. Centralize configuration management in the application to ensure consistency and validation.
