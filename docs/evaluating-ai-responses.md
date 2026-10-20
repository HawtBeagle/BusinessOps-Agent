# What does PASS mean for an AI response?

The M02 evaluator checks a frozen set of 15 customer-message cases against a compatible request-analysis API. It compares structured fields rather than requiring an exact generated sentence.

Examples include an absent order ID, preserving `00123` as an identifier, reporting damage without requesting a refund, and instructions embedded inside a customer message. These are expected behaviours, not guarantees that a model always follows them.

## Run evaluator unit tests without a model

```bash
uv sync --frozen
uv run python -m pytest tests/test_m02_evaluator.py -q
```

The tests check the evaluator itself using supplied responses. They do not call Ollama or the API and do not measure live-model accuracy.

## Optional live evaluation

```bash
uv run python -m scripts.evaluate_m02 --help
uv run python -m scripts.evaluate_m02 --url http://localhost:8000/requests/analyse --model qwen3:8b
```

The second command requires a separately running compatible API and Ollama. That application entry point is not yet published in this incremental snapshot, so this repository alone cannot start the live service. Importing the evaluator or running its unit tests does not send requests.

The evaluator sends `X-provider: real` and saves each request, actual response, HTTP status, selected expected fields, failed checks and elapsed request time under `evaluations/results/<timestamp>/`. Do not commit runtime captures containing real customer data.

## Interpreting results

- A field-check PASS means schema validation and selected comparisons passed. It is not proof that the entire generated answer is correct.
- Request type and order ID are compared with reviewed expected values. Missing business fields are compared as lists.
- A damage reason is checked for presence, not semantic faithfulness. The generated summary is not compared for meaning.
- Each record therefore retains `semantic_review: pending`; summaries and reasons need separate review.
- The endpoint does not expose repair usage, so the report does not infer first-pass validity or repair counts.
- Local prompt/schema hashes identify files on disk, not proof of what a running server loaded. The long-input case is not a context-limit benchmark.
