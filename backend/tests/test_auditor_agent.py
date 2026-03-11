
import pytest
import sys
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

@pytest.mark.asyncio
@patch('app.services.auditor_agent.llm_service.generate_response', new_callable=AsyncMock)
async def test_audit_question_success(mock_generate_response):
    from app.services.auditor_agent import auditor_agent

    mock_generate_response.return_value = '```json\n{"feedback": "Good question", "score": 8, "actions": []}\n```'

    question_data = {"bloom_level": "Understand", "difficulty": "Easy", "text": "What is 2+2?"}
    topic = "Math"

    result = await auditor_agent.audit_question(question_data, topic)

    assert result == {"feedback": "Good question", "score": 8, "actions": []}
    mock_generate_response.assert_called_once()

@pytest.mark.asyncio
@patch('app.services.auditor_agent.llm_service.generate_response', new_callable=AsyncMock)
async def test_audit_question_parsing_error(mock_generate_response):
    from app.services.auditor_agent import auditor_agent

    # Return malformed JSON to trigger the exception block
    mock_generate_response.return_value = '```json\n{"feedback": "Good question", "score": 8, "actions": [\n```'

    question_data = {"bloom_level": "Understand", "difficulty": "Easy", "text": "What is 2+2?"}
    topic = "Math"

    result = await auditor_agent.audit_question(question_data, topic)

    assert result == {"feedback": "Error parsing", "score": 0, "actions": []}
    mock_generate_response.assert_called_once()
