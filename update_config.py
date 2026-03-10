import sys

with open("backend/app/core/config.py", "r") as f:
    content = f.read()

new_content = content.replace(
    '    PROJECT_NAME: str = "Question Bank Generator"',
    '    PROJECT_NAME: str = "Question Bank Generator"\n    BACKEND_CORS_ORIGINS: list[str] = [origin.strip() for origin in os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:5173,http://localhost:5176,http://localhost:8000").split(",") if origin.strip()]'
)

with open("backend/app/core/config.py", "w") as f:
    f.write(new_content)
