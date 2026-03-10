import json
import logging
from .llm_service import llm_service

logger = logging.getLogger(__name__)


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
        
        Output strictly valid JSON:
        {{
            "feedback": "...",
            "score": 0-10,
            "actions": ["Start with 'Explain' instead of 'What'", "Increase difficulty"]
        }}
        """

        response = await llm_service.generate_response(
            prompt, system_prompt="You are a strict JSON auditor."
        )

        try:
            clean_response = response.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_response)
        except Exception as e:
            logger.error(f"Error parsing audit: {e}")
            return {"feedback": "Error parsing", "score": 0, "actions": []}


auditor_agent = AuditorAgent()
