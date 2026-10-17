from abc import ABC, abstractmethod

from app.schemas.common_llm_request_response import LLMRequest, LLMResponse


class LLMInterfaceProvider(ABC):
    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        pass