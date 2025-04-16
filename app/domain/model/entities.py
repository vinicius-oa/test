import uuid
from decimal import Decimal
from typing import Optional
from uuid import UUID

from domain.model.value_objects import CarDetails, Deductible, Fee, PolicyLimit, Premium, Rate
from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Coordinate


class Car(BaseModel):
    details: CarDetails
    id: UUID = Field(default_factory=uuid.uuid4)
    registration_location: Optional[Coordinate] = None


class Policy(BaseModel):
    applied_rate: Rate
    broker_fee: Fee
    deductible: Deductible
    deductible_value: Decimal
    id: UUID = Field(default_factory=uuid.uuid4)
    policy_limit: PolicyLimit
    premium: Premium
