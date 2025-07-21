from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuration(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "decision-helper"
    app_port: int = 8000
    app_host: str = "0.0.0.0"

    openai_api_key: str
    tavily_api_key: str

    langsmith_project: str
    langsmith_api_key: str
    langchain_tracing_v2: str

    database_url: str

    google_application_credentials: str