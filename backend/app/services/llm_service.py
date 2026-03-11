import os
import instructor
from openai import AsyncOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Type, TypeVar

T = TypeVar("T")

# Configuration for Local LLM (Ollama or LM Studio)
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://host.docker.internal:11434/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
LLM_API_KEY = os.getenv("LLM_API_KEY", "lm-studio")


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=LLM_BASE_URL, api_key=LLM_API_KEY, model=LLM_MODEL, temperature=0.7
        )
        # Setup instructor client
        self.client = instructor.from_openai(
            AsyncOpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY),
            mode=instructor.Mode.JSON,
        )

    async def generate_response(
        self, prompt: str, system_prompt: str = "You are a helpful AI assistant."
    ) -> str:
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=prompt)]
        response = await self.llm.ainvoke(messages)
        return response.content

    async def generate_structured_response(
        self,
        prompt: str,
        response_model: Type[T],
        system_prompt: str = "You are a strict JSON generator.",
    ) -> T:
        response = await self.client.chat.completions.create(
            model=LLM_MODEL,
            response_model=response_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response


llm_service = LLMService()
