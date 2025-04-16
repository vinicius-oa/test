from decimal import Decimal

import pytest
from freezegun import freeze_time

from domain.model.value_objects import CarDetails, Rate, Deductible, Fee
from domain.service.premium_calculation_service import PremiumCalculationService


@freeze_time("2025-04-15")
def test_calculate_base_rate(premium_calculation_service):
    car_details = CarDetails(
        make="Toyota",
        model="Corolla",
        year=2015,
        value=Decimal('100000.0')
    )
    rate = premium_calculation_service.calculate_base_rate(car_details)
    assert rate.percentage == Decimal('0.1')


@freeze_time("2025-04-15")
@pytest.mark.parametrize(
    "car_year, car_value, expected_rate", [
        (2020, Decimal('20000.0'), Decimal('0.035')),
        (2000, Decimal('50000.0'), Decimal('0.15')),
        (2023, Decimal('5000.0'), Decimal('0.0125')),
    ]
)
def test_calculate_base_rate_parameterized(car_year, car_value, expected_rate, premium_calculation_service):
    car_details = CarDetails(
        make="Toyota",
        model="Corolla",
        year=car_year,
        value=car_value
    )

    rate = premium_calculation_service.calculate_base_rate(car_details)
    assert pytest.approx(rate.percentage, abs=1e-10) == expected_rate


def test_calculate_premium():
    car_details = CarDetails(
        make="Toyota",
        model="Corolla",
        year=2015,
        value=Decimal('100000.0')
    )

    base_rate = Rate(percentage=Decimal('0.1'))
    deductible = Deductible(percentage=Decimal('0.05'))
    broker_fee = Fee(amount=Decimal('50.0'))

    premium = PremiumCalculationService.calculate_premium(
        car_details, base_rate, deductible, broker_fee
    )

    assert premium == Decimal('9550.0')


@pytest.mark.parametrize(
    "car_value, rate_percentage, deductible_percentage, broker_fee_amount, expected_premium", [
        (Decimal('50000'), Decimal('0.08'), Decimal('0.1'), Decimal('100.0'), Decimal('3700.0')),
        (Decimal('20000'), Decimal('0.05'), Decimal('0.0'), Decimal('25.0'), Decimal('1025.0')),
        (Decimal('100000'), Decimal('0.12'), Decimal('0.2'), Decimal('200.0'), Decimal('9800.0')),
    ]
)
def test_calculate_premium_parameterized(
        car_value, rate_percentage, deductible_percentage, broker_fee_amount, expected_premium
):
    car_details = CarDetails(
        make="Toyota",
        model="Corolla",
        year=2015,
        value=car_value
    )

    base_rate = Rate(percentage=rate_percentage)
    deductible = Deductible(percentage=deductible_percentage)
    broker_fee = Fee(amount=broker_fee_amount)

    premium = PremiumCalculationService.calculate_premium(
        car_details, base_rate, deductible, broker_fee
    )

    assert premium == expected_premium

def test_calculate_policy(premium_calculation_service):
    car_details = CarDetails(
        make="Toyota",
        model="Corolla",
        year=2015,
        value=Decimal('100000.0')
    )

    deductible = Deductible(percentage=Decimal('0.1'))

    final_policy_limit, deductible_value = premium_calculation_service.calculate_policy(
        car_details, deductible
    )

    assert final_policy_limit == Decimal('90000.0')
    assert deductible_value == Decimal('10000.0')


@pytest.mark.parametrize(
    "car_value, coverage_percentage, deductible_percentage, expected_policy_limit, expected_deductible_value", [
        (Decimal('50000.0'), Decimal('1.0'), Decimal('0.1'), Decimal('45000.0'), Decimal('5000.0')),
        (Decimal('20000.0'), Decimal('0.8'), Decimal('0.05'), Decimal('15200.0'), Decimal('800.0')),
        (Decimal('100000.0'), Decimal('1.2'), Decimal('0.15'), Decimal('102000.0'), Decimal('18000.0')),
    ]
)
def test_calculate_policy_parameterized(
        car_value, coverage_percentage, deductible_percentage,
        expected_policy_limit, expected_deductible_value
):
    premium_calculation_service = PremiumCalculationService(
        age_rate_increment_per_year=Decimal(0.005),
        coverage_percentage=coverage_percentage,
        value_rate_increment_per_amount=Decimal(0.005),
        value_threshold_for_rate_increment=Decimal(10000.0),
    )

    car_details = CarDetails(
        make="Toyota",
        model="Corolla",
        year=2015,
        value=car_value
    )

    deductible = Deductible(percentage=deductible_percentage)

    final_policy_limit, deductible_value = premium_calculation_service.calculate_policy(
        car_details, deductible
    )

    assert final_policy_limit == expected_policy_limit
    assert deductible_value == expected_deductible_value
