from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AnalyzingContext"
    base_url: str = 'http://localhost'


settings = Settings()