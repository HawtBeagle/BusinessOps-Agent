import asyncio
import json

from app.providers.base.llm_interface_provider import LLMInterfaceProvider
from app.providers.fake.fake_llm_provider import FakeLLMProvider
from app.schemas.common_llm_request_response import LLMMessage, LLMRequest, Role


def test_fake_provider_returns_a_known_response():
    provider = FakeLLMProvider()
    request = LLMRequest(
        model="test-model",
        messages=[LLMMessage(role=Role.USER, content="Please refund my order.")],
        temperature=0,
    )

    response = asyncio.run(provider.generate(request))

    assert isinstance(provider, LLMInterfaceProvider)
    assert response.model == "test-model"
    assert response.provider == "fake"
    assert json.loads(response.content) == {
        "request_type": "refund",
        "order_id": "ex2",
        "reason": "ex3",
        "summary": "ex4",
    }
    assert response.input_tokens == 10
    assert response.output_tokens == 24
    assert response.total_tokens == 34
    assert response.latency_ms == 100
    assert response.finish_reason == "stop"
    assert response.tool_calls == []


def test_fake_provider_is_deterministic_not_an_intent_classifier():
    provider = FakeLLMProvider()
    requests = [
        LLMRequest(
            model="test-model",
            messages=[LLMMessage(role=Role.USER, content=prompt)],
            temperature=0,
        )
        for prompt in ("Please refund my order.", "Hello!")
    ]

    responses = [asyncio.run(provider.generate(request)) for request in requests]

    assert responses[0].model_dump() == responses[1].model_dump()
