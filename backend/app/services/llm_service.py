import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Configuration for Local LLM (Ollama or LM Studio)
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://host.docker.internal:11434/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
LLM_API_KEY = os.getenv("LLM_API_KEY", "lm-studio")

class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            base_url=LLM_BASE_URL,
            api_key=LLM_API_KEY,
            model=LLM_MODEL,
            temperature=0.7
        )

    def generate_response(self, prompt: str, system_prompt: str = "You are a helpful AI assistant.") -> str:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ]
        response = self.llm.invoke(messages)
        return response.content

llm_service = LLMService()
