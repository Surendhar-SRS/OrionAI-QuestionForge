import pytest
import sys
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Mock dependencies
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_community'] = MagicMock()
sys.modules['langchain_community.document_loaders'] = MagicMock()
sys.modules['langchain_community.vectorstores'] = MagicMock()
sys.modules['langchain_huggingface'] = MagicMock()

sys.modules['backend.app.services.rag_service'] = MagicMock()
sys.modules['backend.app.services.llm_service'] = MagicMock()

import backend.app.services.generator_agent as ga

@pytest.mark.asyncio
async def test_caching():
    ga.rag_service.retrieve_context = MagicMock(return_value=["Context 1"])
    ga.llm_service.generate_response = AsyncMock()

    async def delayed_generate(*args, **kwargs):
        await asyncio.sleep(0.5)
        return '```json\n{"text": "Q", "type": "MCQ", "marks": 5, "answer_key": "A", "rubric": "R"}\n```'

    ga.llm_service.generate_response.side_effect = delayed_generate

    # Run once
    import time
    start = time.time()
    res1 = await ga.generator_agent.generate_question(1, "Remember", "Easy", "Math")
    t1 = time.time() - start

    # Run again with same args
    start = time.time()
    res2 = await ga.generator_agent.generate_question(1, "Remember", "Easy", "Math")
    t2 = time.time() - start

    # Verify cached output is same as uncached
    assert res1 == res2
    # Verify time saved
    assert t2 < t1 / 2, f"Second run should be much faster. t1={t1:.4f}, t2={t2:.4f}"
