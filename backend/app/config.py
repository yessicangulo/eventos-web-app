import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost/mis_eventos"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    BACKEND_CORS_ORIGINS: str | list[str] = os.getenv(
        "BACKEND_CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
    )
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Mis Eventos API")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    API_V1_PREFIX: str = os.getenv("API_V1_PREFIX", "/api/v1")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            self.BACKEND_CORS_ORIGINS = [
                origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()
            ]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
