import json
import logging
from typing import List
from pydantic import BaseModel, Field
from .llm_service import llm_service

logger = logging.getLogger(__name__)


class AuditFeedback(BaseModel):
    feedback: str = Field(description="Detailed feedback on the question.")
    score: int = Field(
        description="A score between 0 and 10 representing question quality."
    )
    actions: List[str] = Field(
        description="List of actionable suggestions to improve the question."
    )


class AuditorAgent:
    async def audit_question(self, question_data: dict, topic: str):
        prompt = f"""
        Role: Academic Quality Auditor.
        Question: {json.dumps(question_data)}
        Topic: {topic}
        Task: Critique this question for alignment with Bloom's Level '{question_data.get("bloom_level")}' and Difficulty '{question_data.get("difficulty")}'.
        Check for:
        1. Clarity
        2. Alignment
        3. Correctness
        """

        try:
            audit_result = await llm_service.generate_structured_response(
                prompt=prompt,
                response_model=AuditFeedback,
                system_prompt="You are a strict JSON auditor.",
            )
            return audit_result.model_dump()
        except Exception as e:
            logger.error(f"Error parsing audit: {e}")
            return {"feedback": "Error parsing", "score": 0, "actions": []}


auditor_agent = AuditorAgent()
