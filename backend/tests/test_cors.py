from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

client = TestClient(app)

def test_cors_allowed_origin():
    # Test an allowed origin
    headers = {
        "Origin": "http://localhost:5173",
        "Access-Control-Request-Method": "GET"
    }
    response = client.options("/", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"

def test_cors_disallowed_origin():
    # Test a disallowed origin
    headers = {
        "Origin": "http://evil.com",
        "Access-Control-Request-Method": "GET"
    }
    response = client.options("/", headers=headers)
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
