from decimal import Decimal
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


    # Car details restrictions
    oldest_car_year: int

    # Application settings
    app_name: str = "Car Insurance Premium Simulator"

    # Premium calculation settings
    age_rate_increment_per_year: Decimal
    coverage_percentage: Decimal
    value_rate_increment_per_amount: Decimal
    value_threshold_for_rate_increment: Decimal


@lru_cache
def get_settings() -> Settings:
    return Settings()