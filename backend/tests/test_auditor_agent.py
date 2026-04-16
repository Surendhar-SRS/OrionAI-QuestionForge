import pytest
from unittest.mock import patch, AsyncMock
from app.services.auditor_agent import AuditFeedback


@pytest.mark.asyncio
@patch(
    "app.services.auditor_agent.llm_service.generate_structured_response",
    new_callable=AsyncMock,
)
async def test_audit_question_success(mock_generate_structured_response):
    from app.services.auditor_agent import auditor_agent

    mock_generate_structured_response.return_value = AuditFeedback(
        feedback="Good question", score=8, actions=[]
    )

    question_data = {
        "bloom_level": "Understand",
        "difficulty": "Easy",
        "text": "What is 2+2?",
    }
    topic = "Math"
    result = await auditor_agent.audit_question(question_data, topic)

    assert result == {"feedback": "Good question", "score": 8, "actions": []}
    mock_generate_structured_response.assert_called_once()


@pytest.mark.asyncio
@patch(
    "app.services.auditor_agent.llm_service.generate_structured_response",
    new_callable=AsyncMock,
)
async def test_audit_question_parsing_error(mock_generate_structured_response):
    from app.services.auditor_agent import auditor_agent

    mock_generate_structured_response.side_effect = ValueError("Parse error")

    question_data = {
        "bloom_level": "Understand",
        "difficulty": "Easy",
        "text": "What is 2+2?",
    }
    topic = "Math"
    result = await auditor_agent.audit_question(question_data, topic)

    assert result == {"feedback": "Error parsing", "score": 0, "actions": []}
    mock_generate_structured_response.assert_called_once()
