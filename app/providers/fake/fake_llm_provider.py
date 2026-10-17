from app.schemas.common_llm_request_response import LLMRequest, LLMResponse
from app.providers.base.llm_interface_provider import LLMInterfaceProvider


class FakeLLMProvider(LLMInterfaceProvider):

    async def generate(self, request: LLMRequest) -> LLMResponse:
        return LLMResponse(
            model=request.model,
            provider="fake",
            content=
                """{
                    "request_type": "refund",
                    "order_id": "ex2",
                    "reason": "ex3",
                    "summary": "ex4"
                }""",
            input_tokens=10,
            output_tokens=24,
            latency_ms=100,
            finish_reason="stop"
        )
