import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import json

# Mock missing dependencies to allow importing GeneratorAgent in restricted environments
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_core'] = MagicMock()
sys.modules['langchain_core.messages'] = MagicMock()
sys.modules['langchain_community'] = MagicMock()
sys.modules['langchain_community.document_loaders'] = MagicMock()
sys.modules['langchain_text_splitters'] = MagicMock()
sys.modules['langchain_huggingface'] = MagicMock()
sys.modules['langchain_postgres'] = MagicMock()
sys.modules['langchain_postgres.vectorstores'] = MagicMock()
sys.modules['sqlalchemy'] = MagicMock()
sys.modules['sqlalchemy.ext'] = MagicMock()
sys.modules['sqlalchemy.ext.asyncio'] = MagicMock()
sys.modules['sqlmodel'] = MagicMock()
sys.modules['sqlmodel.ext'] = MagicMock()
sys.modules['sqlmodel.ext.asyncio'] = MagicMock()
sys.modules['sqlmodel.ext.asyncio.session'] = MagicMock()

from app.services.generator_agent import GeneratorAgent

class TestGeneratorAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.generator = GeneratorAgent()
        self.current_question = {
            "text": "What is 2+2?",
            "bloom_level": "Remember",
            "difficulty": "Easy"
        }
        self.critique = "Make it more challenging."
        self.context_str = "Basic arithmetic."
        self.topic = "Math"

    @patch('app.services.generator_agent.llm_service')
    async def test_refine_question_success(self, mock_llm):
        # Happy path: LLM returns valid JSON
        refined_json = {
            "text": "What is 2+2*2?",
            "type": "MCQ",
            "marks": 5,
            "answer_key": "6",
            "rubric": "Correct answer gets 5 marks"
        }
        mock_llm.generate_response = AsyncMock(return_value=json.dumps(refined_json))

        result = await self.generator.refine_question(
            self.current_question,
            self.critique,
            self.context_str,
            self.topic
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["text"], "What is 2+2*2?")
        # Verify bloom_level and difficulty are persisted
        self.assertEqual(result["bloom_level"], "Remember")
        self.assertEqual(result["difficulty"], "Easy")

    @patch('app.services.generator_agent.llm_service')
    async def test_refine_question_json_decode_error(self, mock_llm):
        # Error path: LLM returns invalid JSON
        mock_llm.generate_response = AsyncMock(return_value="Invalid JSON response")

        with patch('app.services.generator_agent.logger') as mock_logger:
            result = await self.generator.refine_question(
                self.current_question,
                self.critique,
                self.context_str,
                self.topic
            )

            self.assertIsNone(result)
            mock_logger.error.assert_called()
            args, _ = mock_logger.error.call_args
            self.assertIn("Error parsing refinement", args[0])

    @patch('app.services.generator_agent.llm_service')
    async def test_refine_question_llm_exception(self, mock_llm):
        # Error path: LLM service raises an exception
        mock_llm.generate_response = AsyncMock(side_effect=Exception("LLM failure"))

        with self.assertRaises(Exception) as cm:
            await self.generator.refine_question(
                self.current_question,
                self.critique,
                self.context_str,
                self.topic
            )
        self.assertEqual(str(cm.exception), "LLM failure")

    @patch('app.services.generator_agent.llm_service')
    async def test_refine_question_with_markdown_json(self, mock_llm):
        # Happy path: LLM returns JSON wrapped in markdown
        refined_json = {
            "text": "Refined question",
            "bloom_level": "Understand",
            "difficulty": "Medium"
        }
        mock_llm.generate_response = AsyncMock(return_value=f"```json\n{json.dumps(refined_json)}\n```")

        result = await self.generator.refine_question(
            self.current_question,
            self.critique,
            self.context_str,
            self.topic
        )

        self.assertIsNotNone(result)
        self.assertEqual(result["text"], "Refined question")
        # In the actual code, bloom_level and difficulty from current_question OVERWRITE what's in refined_json
        self.assertEqual(result["bloom_level"], "Remember")
        self.assertEqual(result["difficulty"], "Easy")

if __name__ == '__main__':
    unittest.main()
