from datetime import datetime
from decimal import Decimal
from typing import Tuple

from domain.model.entities import Policy
from domain.model.value_objects import CarDetails, Deductible, Fee, PolicyLimit, Premium, Rate


class PremiumCalculationService:
    def __init__(
            self,
        age_rate_increment_per_year: Decimal,
        coverage_percentage: Decimal,
        value_rate_increment_per_amount: Decimal,
        value_threshold_for_rate_increment: Decimal,
    ):
        self.age_rate_increment_per_year = age_rate_increment_per_year
        self.coverage_percentage = coverage_percentage
        self.value_rate_increment_per_amount = value_rate_increment_per_amount
        self.value_threshold_for_rate_increment = value_threshold_for_rate_increment


    def calculate_base_rate(self, car_details: CarDetails) -> Rate:
        current_year = datetime.now().year
        car_age = Decimal(current_year - car_details.year)

        age_rate = car_age * self.age_rate_increment_per_year

        value_rate = (car_details.value / self.value_threshold_for_rate_increment) * self.value_rate_increment_per_amount
        total_rate = age_rate + value_rate
        return Rate(percentage=total_rate.quantize(Decimal("0.0001")))

    @staticmethod
    def calculate_premium(car_details: CarDetails, base_rate: Rate, deductible: Deductible, broker_fee: Fee) -> Decimal:
        base_premium_amount = car_details.value * base_rate.percentage
        deductible_discount = base_premium_amount * deductible.percentage
        final_premium_amount = base_premium_amount - deductible_discount + broker_fee.amount
        return final_premium_amount

    def calculate_policy(self, car_details: CarDetails, deductible: Deductible) -> Tuple[Decimal, Decimal]:
        base_policy_limit = car_details.value * self.coverage_percentage
        deductible_value = base_policy_limit * deductible.percentage
        final_policy_limit = base_policy_limit - deductible_value
        return final_policy_limit, deductible_value

    def calculate(
        self,
        broker_fee: Fee,
        car_details: CarDetails,
        deductible: Deductible,
    ) -> Tuple[Rate, Premium, PolicyLimit, Decimal]:
        base_rate = self.calculate_base_rate(car_details)
        final_premium_amount = self.calculate_premium(car_details=car_details, base_rate=base_rate, deductible=deductible, broker_fee=broker_fee)
        final_policy_limit, deductible_value = self.calculate_policy(car_details=car_details, deductible=deductible)
        return base_rate, Premium(amount=final_premium_amount), PolicyLimit(amount=final_policy_limit), deductible_value

    def create_policy(
            self,
            broker_fee: Fee,
            car_details: CarDetails,
            deductible: Deductible,
    ) -> Policy:
        applied_rate, premium, policy_limit, deductible_value = self.calculate(
            broker_fee=broker_fee,
            car_details=car_details,
            deductible=deductible,
        )

        return Policy(
            applied_rate=applied_rate,
            broker_fee=broker_fee,
            deductible=deductible,
            deductible_value=deductible_value,
            policy_limit=policy_limit,
            premium=premium
        )
