## 2025-02-28 - Missing Password Complexity Validation
**Vulnerability:** The backend `UserCreate` schema and the `register` endpoint accepted any string (including empty strings and very short passwords) without enforcing any complexity rules or minimum length constraints.
**Learning:** This architectural oversight allowed attackers to create accounts with easily guessable or brute-forceable credentials, bypassing basic security measures.
**Prevention:** Always enforce minimum length constraints (e.g. `min_length=8` using pydantic `Field`) and complexity checks at the schema layer for all new user credentials.
