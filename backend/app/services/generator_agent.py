import json
import copy
import logging
from cachetools import TTLCache
from .llm_service import llm_service
from .rag_service import rag_service

logger = logging.getLogger(__name__)

class GeneratorAgent:
    def __init__(self):
        # Cache up to 100 questions for 1 hour to prevent identical redundant generation
        self._cache = TTLCache(maxsize=100, ttl=3600)

    async def generate_question(self, course_id: int, bloom_level: str, difficulty: str, topic: str):
        cache_key = f"{course_id}_{bloom_level}_{difficulty}_{topic}"

        cached_data = self._cache.get(cache_key)
        if cached_data:
            logger.info(f"Returning cached question for {cache_key}")
            return copy.deepcopy(cached_data)

        # 1. Retrieve Context
        context = rag_service.retrieve_context(f"{topic} {bloom_level} {difficulty}", course_id)
        context_str = "\n".join(context)

        # 2. Prompt
        prompt = f"""
        Role: Academic Question Generator.
        Context: {context_str}
        Task: Create a {difficulty} {bloom_level} question about "{topic}".
        Requirements:
        - Output strictly valid JSON.
        - Schema: {{ "text": "...", "type": "MCQ/Short/Long", "marks": 5, "answer_key": "...", "rubric": "..." }}
        """

        # 3. Call LLM
        response = await llm_service.generate_response(prompt, system_prompt="You are a strict JSON generator.")
        
        # 4. Parse JSON (Basic cleanup)
        try:
            # removing ```json and ``` if present
            clean_response = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_response)
            data['bloom_level'] = bloom_level
            data['difficulty'] = difficulty
            self._cache[cache_key] = data
            return data
        except Exception as e:
            logger.error(f"Error parsing generation: {e}")
            return None

    async def refine_question(self, current_question: dict, critique: str, context_str: str, topic: str):
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
        
        response = await llm_service.generate_response(prompt, system_prompt="You are a strict JSON generator. Return ONLY the JSON.")
        
        try:
            clean_response = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_response)
            # Ensure critical fields persist if LLM misses them
            data['bloom_level'] = current_question.get('bloom_level', 'Understand')
            data['difficulty'] = current_question.get('difficulty', 'Medium')
            return data
        except Exception as e:
            logger.error(f"Error parsing refinement: {e}")
            return None

generator_agent = GeneratorAgent()
