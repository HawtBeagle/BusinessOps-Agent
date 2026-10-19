# A valid schema is not proof of customer intent

In a local learning experiment, the customer message was "My order #123 is damaged". The model classified it as a refund request even though the customer had not requested a refund.

The JSON was structurally valid: `refund` is an allowed request type, the order ID and reason were strings, and the summary was present. `AnalyseResult` cannot detect that the requested action was inferred. `find_missing_business_information` checks required information for the chosen action; it does not verify whether that action matches the original message.

The published analysis prompt now distinguishes reporting damage from asking for money back. It explicitly maps a damage-only report to `unknown`, and instructs the model not to claim that an action has been approved or completed. This is guidance, not a deterministic correctness guarantee.

For an unclear action, clarification is the intended next step. This publication contains no clarification executor or runnable analysis endpoint yet.

## Reproduce the validation boundary

```bash
uv sync --frozen
uv run python -m pytest tests/test_business_response_validation.py tests/test_analysis_field_types.py -q
```

`test_valid_schema_cannot_detect_an_inferred_refund_intent` supplies a deliberately misclassified response and confirms that structural and missing-field checks accept it. It does not call a model or prove the prompt fixes the classification.

The surrounding tests check allowed enum values, required-but-nullable fields, extra-field rejection, field types, preserved identifiers and missing business information. Live model classification still requires a separate evaluation against reviewed expected decisions.
