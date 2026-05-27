from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    supported_languages: set[str] = {"en", "es", "fr", "de"}
    min_prompt_length: int = 5
    page_size_default: int = 10
    page_size_max: int = 50


@lru_cache
def get_settings() -> Settings:
    return Settings()

