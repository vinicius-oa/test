from application.dto.dto import RequestInsuranceQuoteDTO, ResponseInsuranceQuoteDTO
from domain.event.events import PremiumCalculatedEvent, QuoteCreatedEvent
from domain.model.aggregates import InsuranceQuote
from domain.model.entities import Car
from domain.model.value_objects import CarDetails, Deductible, Fee
from domain.service.premium_calculation_service import PremiumCalculationService


class PremiumService:
    def __init__(self, premium_calculation_service: PremiumCalculationService):
        self.premium_calculation_service = premium_calculation_service

    def create_quote(self, request: RequestInsuranceQuoteDTO) -> ResponseInsuranceQuoteDTO:
        car_details = CarDetails(
            make=request.car_details.make,
            model=request.car_details.model,
            value=request.car_details.value,
            year=request.car_details.year
        )
        broker_fee = Fee(amount=request.broker_fee)
        deductible = Deductible(percentage=request.deductible_percentage)

        car = Car(details=car_details, registration_location=request.registration_location)

        policy = self.premium_calculation_service.create_policy(
            broker_fee=broker_fee,
            car_details=car_details,
            deductible=deductible,
        )

        quote = InsuranceQuote(car=car, policy=policy)

        # Create events (in a real application, these would be published to an event bus)
        _ = QuoteCreatedEvent(quote=quote)
        _ = PremiumCalculatedEvent(
            quote_id=quote.id,
            premium_amount=policy.premium.amount
        )

        return ResponseInsuranceQuoteDTO(
            car_details=car_details,
            applied_rate=policy.applied_rate.percentage,
            calculated_premium=policy.premium.amount,
            deductible_value=policy.deductible_value,
            policy_limit=policy.policy_limit.amount,
        )