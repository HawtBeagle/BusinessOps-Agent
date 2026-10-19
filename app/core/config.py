from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DB_FILENAME = "workflow.db"
DEFAULT_WORKFLOW_DB_PATH = PROJECT_ROOT / WORKFLOW_DB_FILENAME


class Settings(BaseSettings):
    ollama_provider_base_url: str
    ollama_provider_timeout_seconds: int = Field(gt=0)
    ollama_provider_default_model: str
    max_tool_calls_per_request: int = Field(default=3, gt=0)
    tool_timeout_seconds: float = Field(default=5.0, gt=0, allow_inf_nan=False)
    log_level: str = "INFO"
    workflow_db_path: Path = DEFAULT_WORKFLOW_DB_PATH
    workflow_max_steps: int = Field(default=10, ge=1)
    postgres_db_url: PostgresDsn | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
