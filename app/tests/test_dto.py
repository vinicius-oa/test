import datetime
from decimal import Decimal
from unittest.mock import patch

import pytest
from pydantic import ValidationError

from application.dto.dto import CarDetailsDTO


@pytest.mark.parametrize(
    "car_year, expected_valid", [
        (2020, True),
        (datetime.date.today().year, True),
        (1980, True),
        (1979, False),
        (datetime.date.today().year + 1, False),
        (123, False),
    ]
)
def test_car_year_validator(car_year, expected_valid, car_restrictions):
    with patch('application.dto.dto.get_settings', return_value=car_restrictions):
        if expected_valid:
            car_details = CarDetailsDTO(
                make="Toyota",
                model="Corolla",
                year=car_year,
                value=Decimal('10000.0')
            )
            assert car_details.year == car_year
        else:
            with pytest.raises(ValidationError):
                CarDetailsDTO(
                    make="Toyota",
                    model="Corolla",
                    year=car_year,
                    value=Decimal('10000.0')
                )