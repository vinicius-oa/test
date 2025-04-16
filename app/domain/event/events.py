import uuid
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from domain.model.aggregates import InsuranceQuote
from pydantic import BaseModel, Field


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.today)


class PremiumCalculatedEvent(Event):
    premium_amount: Decimal
    quote_id: UUID = Field(default_factory=uuid.uuid4)


class QuoteCreatedEvent(Event):
    quote: InsuranceQuote
