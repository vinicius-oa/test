import datetime
from decimal import Decimal
from typing import Optional

from domain.model.value_objects import CarDetails
from infrastructure.config.settings import get_settings
from pydantic import BaseModel, field_validator
from pydantic_extra_types.coordinate import Coordinate


class DecimalRoundingUpMixin(BaseModel):

    @field_validator("value", "deductible_percentage", "broker_fee", "applied_rate", "policy_limit", "calculated_premium", "deductible_value", check_fields=False)
    @classmethod
    def format_decimal_values(cls, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.0001"))


class CarDetailsDTO(DecimalRoundingUpMixin):
    make: str
    model: str
    year: int
    value: Decimal

    @field_validator("year")
    @classmethod
    def validate_car_year(cls, year: int) -> int:
        year_as_str = str(year)
        car_restrictions = get_settings()
        if len(year_as_str) != 4 or year > datetime.date.today().year:
            raise ValueError("Invalid car's year.")
        if year < (ocy := car_restrictions.oldest_car_year):
            raise ValueError(f"Car's year too old, minimum is: {ocy}")
        return year


class RequestInsuranceQuoteDTO(DecimalRoundingUpMixin):
    car_details: CarDetailsDTO
    deductible_percentage: Decimal
    broker_fee: Decimal
    registration_location: Optional[Coordinate] = None


class ResponseInsuranceQuoteDTO(DecimalRoundingUpMixin):
    car_details: CarDetails
    applied_rate: Decimal
    policy_limit: Decimal
    calculated_premium: Decimal
    deductible_value: Decimal
