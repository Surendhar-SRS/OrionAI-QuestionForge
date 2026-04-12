import unittest
from unittest.mock import patch, AsyncMock
from app.services.generator_agent import GeneratorAgent, QuestionSchema


class TestGeneratorAgent(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.patcher = patch(
            "app.services.generator_agent.llm_service.generate_structured_response",
            new_callable=AsyncMock,
        )
        self.mock_generate_structured_response = self.patcher.start()

        # Also patch rag_service.retrieve_context so it doesn't fail
        self.patcher_rag = patch(
            "app.services.generator_agent.rag_service.retrieve_context",
            return_value=["Mocked context"],
        )
        self.mock_rag = self.patcher_rag.start()

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
            "difficulty": "Easy",
        }
        self.critique = "Make it harder and focus on async/await."
        self.context_str = "Python's asyncio module provides infrastructure for writing single-threaded concurrent code using coroutines."

    def tearDown(self):
        self.patcher.stop()
        self.patcher_rag.stop()

    async def test_generate_question_success(self):
        expected_schema = QuestionSchema(
            text="Write an async function in Python.",
            type="Code",
            marks=10,
            answer_key="async def foo(): pass",
            rubric="Correct syntax",
        )
        self.mock_generate_structured_response.return_value = expected_schema

        result = await self.generator.generate_question(
            self.course_id, self.bloom_level, self.difficulty, self.topic
        )
        self.assertEqual(result["text"], expected_schema.text)
        self.assertEqual(result["marks"], expected_schema.marks)

    async def test_refine_question_success(self):
        expected_schema = QuestionSchema(
            text="Explain async/await.",
            type="Short Answer",
            marks=5,
            answer_key="async makes coroutine, await calls it",
            rubric="Correct concepts",
        )
        self.mock_generate_structured_response.return_value = expected_schema

        result = await self.generator.refine_question(
            self.current_question, self.critique, self.context_str, self.topic
        )
        self.assertEqual(result["text"], expected_schema.text)

    async def test_refine_question_json_decode_error(self):
        # In structured mode, it raises an exception if parsing fails
        self.mock_generate_structured_response.side_effect = Exception("Invalid JSON")

        with patch("app.services.generator_agent.logger") as mock_logger:
            result = await self.generator.refine_question(
                self.current_question, self.critique, self.context_str, self.topic
            )
            self.assertIsNone(result)
            mock_logger.error.assert_called()

    async def test_refine_question_llm_exception(self):
        self.mock_generate_structured_response.side_effect = Exception("LLM failure")

        # Refine now catches the exception and returns None, logging the error.
        result = await self.generator.refine_question(
            self.current_question, self.critique, self.context_str, self.topic
        )
        self.assertIsNone(result)

