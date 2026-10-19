# BusinessOps-Agent

A personal project for learning **agentic AI engineering** through business-operations workflows. Built by [Bhanu Prakash](https://www.linkedin.com/in/bhanu-prakash-0825a9225/), a backend engineer exploring how models, tools and retrieval fit together.

## Current public snapshot

This repository currently contains the model-integration foundations. It is an incremental learning project, not a complete deployed agent.

- A provider interface with an asynchronous `generate(LLMRequest) -> LLMResponse` contract.
- Typed messages for system, user, assistant and tool roles.
- Tool definitions and tool-call representations.
- Request fields for model selection, temperature, structured-output schemas and tools.
- Response fields for content, tool calls, token usage, latency and finish reason.

A deterministic FakeLLM provider implements this contract and returns a fixed sample response for offline tests. It does not classify messages or evaluate model quality. A real model provider, runnable agent workflow and retrieval service are not published in this snapshot yet.

## What I'm learning

My broader local learning work explores:

- **Model integration:** provider boundaries, structured responses, token budgets and finish reasons.
- **Tools and workflows:** validating model-proposed actions, executing tools and keeping tool results distinct from model claims.
- **Retrieval:** document chunking, Ollama embeddings, PostgreSQL/pgvector and a FastAPI retrieval path.
- **Evaluation:** inspecting source chunks and similarity scores, comparing chunking strategies, and checking relevant and unrelated queries against synthetic policy documents.

These learning areas are being published incrementally. Local experiments may be ahead of the code on `main`; the list above is not a claim that every component is available in this checkout.

## Repository layout

```text
app/
  providers/base/llm_interface_provider.py  # Provider boundary
  providers/fake/fake_llm_provider.py       # Fixed response for offline tests
  schemas/common_llm_request_response.py   # Shared messages, requests, responses and tools
tests/test_fake_llm_provider.py             # Fake response contract and determinism
pyproject.toml                            # Python requirements and dependencies
uv.lock                                   # Dependency lockfile
```

## Requirements

The project declares Python **3.12+** and dependencies on FastAPI, Ollama, pydantic-settings and python-dotenv. pytest is declared as a development dependency. See [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock) for the exact dependency definitions.

There is no application entry point or end-to-end setup procedure in this public snapshot yet. PostgreSQL retrieval setup belongs to the local work described above and is not required to read the published contracts.

## Engineering focus

The request-analysis schema, prompt and business-information checks are published as a standalone boundary, not a runnable endpoint. See [why valid JSON is not proof of customer intent](docs/schema-vs-intent.md) for the damaged-order example and reproducible tests.

Run the published provider tests without Ollama or a database:

```bash
uv sync --frozen
uv run python -m pytest tests/test_fake_llm_provider.py -q
```

The sample token counts and latency returned by FakeLLM are constants for tests, not measurements from a model call.

I am applying familiar backend practices to AI systems: explicit contracts, separation of responsibilities, typed data, observable behavior and verification. A successful model call does not by itself prove that an action was executed or an answer is correct.

## Follow the work

I share experiments, mistakes and lessons on [LinkedIn](https://www.linkedin.com/in/bhanu-prakash-0825a9225/).
