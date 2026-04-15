import instructor
from openai import AsyncOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import Type, TypeVar
from app.core.config import settings

T = TypeVar("T")


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=settings.LLM_BASE_URL,
            api_key=settings.LLM_API_KEY,
            model=settings.LLM_MODEL,
            temperature=0.7,
        )
        # Setup instructor client
        self.client = instructor.from_openai(
            AsyncOpenAI(base_url=settings.LLM_BASE_URL, api_key=settings.LLM_API_KEY),
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
            model=settings.LLM_MODEL,
            response_model=response_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response


llm_service = LLMService()
