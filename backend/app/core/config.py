from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "IntelliSaaS"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/intellisaas"
    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = "change-this-to-a-random-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ANTHROPIC_API_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzNjE2YzJiZC1jNDYzLTQ4MzMtOTNiZi0xMmYyNTQxZTk4NTYiLCJlbWFpbCI6Im5ld3VzZXJAZXhhbXBsZS5jb20iLCJyb2xlIjoidXNlciIsImV4cCI6MTc3ODkxODM5NywidHlwZSI6ImFjY2VzcyJ9.SutZOL87g2D7vlKqk1mz5-VBtMUAIfRhypBrkGsDL_8"
    OPENAI_API_KEY: str = ""

    AWS_REGION: str = "ap-south-1"
    S3_BUCKET_NAME: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()