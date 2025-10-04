from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    SECRET_KEY: str = Field("dev-secret-change-me")
    DATABASE_URL: str = Field("sqlite:///./rico.db")
    demo_fiscal_fake: bool = Field(default=False, alias="DEMO_FISCAL_FAKE")

    class Config:
        env_file = ".env"

settings = Settings()
