import pytest
from pydantic import ValidationError

from app.core.config import Settings

def test_settings_can_be_created():
    settings = Settings(
        ollama_provider_base_url = "http://localhost:11434",
        ollama_provider_timeout_seconds = 10,
        ollama_provider_default_model = "qwen3:8b",
    )

    assert settings.ollama_provider_base_url == "http://localhost:11434"
    assert settings.ollama_provider_timeout_seconds == 10
    assert settings.ollama_provider_default_model == "qwen3:8b"

@pytest.mark.parametrize(
    "invalid_timeout",
    [
        0,-1,"hello"
    ]
)
def test_settings_validations(invalid_timeout: int):
    with pytest.raises(ValidationError):
        Settings(
            ollama_provider_base_url = "http://localhost:11434",
            ollama_provider_timeout_seconds = invalid_timeout,
            ollama_provider_default_model = "qwen3:8b",
        )
