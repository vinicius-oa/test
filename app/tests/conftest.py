import datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from domain.service.premium_calculation_service import PremiumCalculationService


@pytest.fixture
def car_restrictions():
    settings_mock = MagicMock()
    settings_mock.oldest_car_year = 1980
    return settings_mock

@pytest.fixture
def current_year():
    return datetime.date.today().year

@pytest.fixture
def premium_calculation_service():
    return PremiumCalculationService(
        age_rate_increment_per_year=Decimal(0.005),
        coverage_percentage=Decimal(1.0),
        value_rate_increment_per_amount=Decimal(0.005),
        value_threshold_for_rate_increment=Decimal(10000),
    )
