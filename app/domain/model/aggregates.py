import uuid
from datetime import datetime
from uuid import UUID

from domain.model.entities import Car, Policy
from pydantic import BaseModel, Field


class InsuranceQuote(BaseModel):
    car: Car
    created_at: datetime = Field(default_factory=datetime.today)
    id: UUID = Field(default_factory=uuid.uuid4)
    policy: Policy
