from instructor.core import InstructorError
from openai import OpenAIError
import json
import logging
import asyncio
from pydantic import BaseModel, ValidationError
from openai import OpenAIError
from .llm_service import llm_service
from .rag_service import rag_service

logger = logging.getLogger(__name__)


class QuestionSchema(BaseModel):
    text: str
    type: str
    marks: int
    answer_key: str
    rubric: str


class GeneratorAgent:
    async def generate_question(
        self, course_id: int, bloom_level: str, difficulty: str, topic: str
    ):
        # 1. Retrieve Context in a background thread to prevent blocking
        context = await asyncio.to_thread(
            rag_service.retrieve_context,
            f"{topic} {bloom_level} {difficulty}",
            course_id,
        )
        context_str = "\n".join(context)

        # 2. Prompt
        prompt = f"""
        Role: Academic Question Generator.
        Context: {context_str}
        Task: Create a {difficulty} {bloom_level} question about "{topic}".
        """

        # 3. Call LLM with structured output
        try:
            data = await llm_service.generate_structured_response(
                prompt=prompt,
                response_model=QuestionSchema,
                system_prompt="You are an academic generator that outputs strictly valid JSON.",
            )
            data_dict = data.model_dump()
            data_dict["bloom_level"] = bloom_level
            data_dict["difficulty"] = difficulty
            return data_dict
        except (ValidationError, OpenAIError) as e:
            logger.error(f"Error parsing generation: {e}")
            return None

    async def refine_question(
        self, current_question: dict, critique: str, context_str: str, topic: str
    ):
        prompt = f"""
        Role: Academic Question Refiner.
        Task: Improve the following question based on the critique.
        
        Original Question: {json.dumps(current_question)}
        Critique: {critique}
        Context: {context_str}
        
        Requirements:
        1. Address all points in the critique.
        2. Keep valid JSON format identical to the original schema.
        3. Maintain the same Bloom's level and difficulty if not asked to change.
        """

        try:
            data = await llm_service.generate_structured_response(
                prompt=prompt,
                response_model=QuestionSchema,
                system_prompt="You are an academic generator that outputs strictly valid JSON. Return ONLY the JSON.",
            )
            data_dict = data.model_dump()
            data_dict["bloom_level"] = current_question.get("bloom_level", "Understand")
            data_dict["difficulty"] = current_question.get("difficulty", "Medium")
            return data_dict
        except (ValidationError, OpenAIError) as e:
            logger.error(f"Error parsing refinement: {e}")
            return None


generator_agent = GeneratorAgent()
