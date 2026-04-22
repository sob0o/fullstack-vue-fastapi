from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Task Manager API"
    app_env: str = "development"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    mongodb_url: str = "mongodb://mongodb:27017"
    mongodb_db: str = "taskdb"

    frontend_origin: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()