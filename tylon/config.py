# tylon/config.py
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import os
import json

class Settings(BaseSettings):
    google_api_key: str

    class Config:
        env_file = ".env"

class ProjectConfig(BaseModel):
    project_type: str = "unknown"
    language: str = "python"
    frameworks: list[str] = []

def load_project_config() -> ProjectConfig:
    if os.path.exists(".tylonrc"):
        with open(".tylonrc", "r") as f:
            return ProjectConfig.model_validate(f.read())
    return ProjectConfig()

settings = Settings()
project_config = load_project_config()