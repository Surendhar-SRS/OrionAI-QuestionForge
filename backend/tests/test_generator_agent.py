
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import json
from app.services.generator_agent import GeneratorAgent

class TestGeneratorAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.patcher = patch('app.services.generator_agent.llm_service.generate_response', new_callable=AsyncMock)
        self.mock_generate_response = self.patcher.start()

        self.generator = GeneratorAgent()

        self.course_id = 1
        self.bloom_level = "Apply"
        self.difficulty = "Hard"
        self.topic = "Python Concurrency"

        self.current_question = {
            "text": "What is asyncio?",
            "type": "Short Answer",
            "marks": 5,
            "bloom_level": "Remember",
            "difficulty": "Easy"
        }
        self.critique = "Make it harder and focus on async/await."
        self.context_str = "Python's asyncio module provides infrastructure for writing single-threaded concurrent code using coroutines."

    def tearDown(self):
        self.patcher.stop()

    async def test_generate_question_success(self):
        expected_json = {
            "text": "Write an async function in Python.",
            "type": "Code",
            "marks": 10,
            "answer_key": "async def foo(): pass",
            "rubric": "Correct syntax"
        }
        self.mock_generate_response.return_value = json.dumps(expected_json)

        result = await self.generator.generate_question(self.course_id, self.bloom_level, self.difficulty, self.topic)
        self.assertEqual(result["text"], expected_json["text"])
        self.assertEqual(result["marks"], expected_json["marks"])

    async def test_refine_question_success(self):
        expected_json = {
            "text": "Explain async/await.",
            "type": "Short Answer",
            "marks": 5,
            "answer_key": "async makes coroutine, await calls it",
            "rubric": "Correct concepts"
        }
        self.mock_generate_response.return_value = json.dumps(expected_json)

        result = await self.generator.refine_question(self.current_question, self.critique, self.context_str, self.topic)
        self.assertEqual(result["text"], expected_json["text"])

    async def test_refine_question_json_decode_error(self):
        self.mock_generate_response.return_value = "Invalid JSON"

        with patch('app.services.generator_agent.logger') as mock_logger:
            result = await self.generator.refine_question(self.current_question, self.critique, self.context_str, self.topic)
            self.assertIsNone(result)
            mock_logger.error.assert_called()

    async def test_refine_question_llm_exception(self):
        self.mock_generate_response.side_effect = Exception("LLM failure")

        with self.assertRaises(Exception) as cm:
            await self.generator.refine_question(self.current_question, self.critique, self.context_str, self.topic)
        self.assertEqual(str(cm.exception), "LLM failure")

    async def test_refine_question_with_markdown_json(self):
        expected_json = {
            "text": "Explain async/await.",
            "type": "Short Answer",
            "marks": 5,
            "answer_key": "async makes coroutine, await calls it",
            "rubric": "Correct concepts"
        }
        self.mock_generate_response.return_value = f"```json\n{json.dumps(expected_json)}\n```"

        result = await self.generator.refine_question(self.current_question, self.critique, self.context_str, self.topic)
        self.assertEqual(result["text"], expected_json["text"])
