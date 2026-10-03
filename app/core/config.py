from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # service metadata
    PROJECT_NAME: str = "Production Multitask Pipeline Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # compute settings
    DEVICE: int = -1 

    # Hugging Face Model Repos
    ZERO_SHOT_MODEL: str = "valhalla/distilbart-mnli-12-3"
    NER_MODEL: str = "dslim/bert-base-NER"

    # Inference Constraints
    MAX_INPUT_TEXT_LENGTH: int = 2000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()