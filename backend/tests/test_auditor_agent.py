import pytest
import sys
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

@pytest.fixture(autouse=True)
def mock_dependencies():
    # Define the mocks
    mocks = {
        'langchain_openai': MagicMock(),
        'langchain_community': MagicMock(),
        'langchain_community.document_loaders': MagicMock(),
        'langchain_community.vectorstores': MagicMock(),
        'langchain_huggingface': MagicMock(),
        'backend.app.services.rag_service': MagicMock(),
        'backend.app.services.llm_service': MagicMock(),
    }

    # Apply the patch.dict context manager to sys.modules
    with patch.dict('sys.modules', mocks):
        yield

@pytest.mark.asyncio
async def test_audit_question_success(mock_dependencies):
    # Import inside the test after dependencies are mocked
    from backend.app.services.auditor_agent import auditor_agent, llm_service

    llm_service.generate_response = AsyncMock(return_value='```json\n{"feedback": "Good question", "score": 8, "actions": []}\n```')

    question_data = {"bloom_level": "Understand", "difficulty": "Easy", "text": "What is 2+2?"}
    topic = "Math"

    result = await auditor_agent.audit_question(question_data, topic)

    assert result == {"feedback": "Good question", "score": 8, "actions": []}
    llm_service.generate_response.assert_called_once()

@pytest.mark.asyncio
async def test_audit_question_parsing_error(mock_dependencies):
    # Import inside the test after dependencies are mocked
    from backend.app.services.auditor_agent import auditor_agent, llm_service

    # Return malformed JSON to trigger the exception block
    llm_service.generate_response = AsyncMock(return_value='```json\n{"feedback": "Good question", "score": 8, "actions": [\n```')

    question_data = {"bloom_level": "Understand", "difficulty": "Easy", "text": "What is 2+2?"}
    topic = "Math"

    result = await auditor_agent.audit_question(question_data, topic)

    assert result == {"feedback": "Error parsing", "score": 0, "actions": []}
    llm_service.generate_response.assert_called_once()
