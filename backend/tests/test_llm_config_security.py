import importlib
from app.core import config
from app.services import llm_service


def test_llm_config_from_env(monkeypatch):
    # Test that it respects the environment variables
    TEST_BASE_URL = "http://test-llm:11434/v1"
    TEST_MODEL = "test-model"
    TEST_API_KEY = "test-api-key"

    monkeypatch.setenv("LLM_BASE_URL", TEST_BASE_URL)
    monkeypatch.setenv("LLM_MODEL", TEST_MODEL)
    monkeypatch.setenv("LLM_API_KEY", TEST_API_KEY)
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

    importlib.reload(config)

    assert config.settings.LLM_BASE_URL == TEST_BASE_URL
    assert config.settings.LLM_MODEL == TEST_MODEL
    assert config.settings.LLM_API_KEY == TEST_API_KEY


def test_llm_service_initialization(monkeypatch):
    TEST_BASE_URL = "http://test-llm-service:11434/v1"
    TEST_MODEL = "test-model-service"
    TEST_API_KEY = "test-key-service"

    monkeypatch.setenv("LLM_BASE_URL", TEST_BASE_URL)
    monkeypatch.setenv("LLM_MODEL", TEST_MODEL)
    monkeypatch.setenv("LLM_API_KEY", TEST_API_KEY)
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

    # Reload config to get new env vars
    importlib.reload(config)

    # Reload llm_service to use new config
    importlib.reload(llm_service)

    # In conftest.py, ChatOpenAI is mocked.
    from langchain_openai import ChatOpenAI

    # Instantiate service which calls ChatOpenAI(...)
    _ = llm_service.LLMService()

    # Check if ChatOpenAI was called with correct values
    ChatOpenAI.assert_called()
    call_args = ChatOpenAI.call_args[1]
    assert call_args["base_url"] == TEST_BASE_URL
    assert call_args["model"] == TEST_MODEL
    assert call_args["api_key"] == TEST_API_KEY
