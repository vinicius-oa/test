from application.dto.dto import RequestInsuranceQuoteDTO, ResponseInsuranceQuoteDTO
from application.service.premium_service import PremiumService
from domain.service.premium_calculation_service import PremiumCalculationService
from fastapi import APIRouter, Depends
from infrastructure.config.settings import Settings, get_settings

router = APIRouter()

def get_premium_calculation_service(settings: Settings = Depends(get_settings)) -> PremiumCalculationService:
    return PremiumCalculationService(
        age_rate_increment_per_year=settings.age_rate_increment_per_year,
        coverage_percentage=settings.coverage_percentage,
        value_rate_increment_per_amount=settings.value_rate_increment_per_amount,
        value_threshold_for_rate_increment=settings.value_threshold_for_rate_increment
    )

def get_premium_service(
    premium_calculation_service: PremiumCalculationService = Depends(get_premium_calculation_service)
) -> PremiumService:
    return PremiumService(premium_calculation_service=premium_calculation_service)

@router.post("/quote", response_model=ResponseInsuranceQuoteDTO)
async def create_quote(
    request: RequestInsuranceQuoteDTO,
    premium_service: PremiumService = Depends(get_premium_service)
) -> ResponseInsuranceQuoteDTO:
    return premium_service.create_quote(request)
