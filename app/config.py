from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "morning-briefing-agent"
    app_env: str = "development"
    timezone: str = "America/Denver"

    google_client_secret_file: str
    google_token_file: str

    weather_api_base_url: str = "https://api.open-meteo.com/v1/forecast"
    weather_latitude: float
    weather_longitude: float

    openclaw_enabled: bool = False
    openclaw_delivery_mode: str = "stdout"
    openclaw_channel: str = ""
    openclaw_recipient: str = ""

    database_url: str = "sqlite:////root/openclaw_project/data/app.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()