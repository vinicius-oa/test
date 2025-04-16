from decimal import Decimal

from pydantic import BaseModel


class CarDetails(BaseModel):
    make: str
    model: str
    year: int
    value: Decimal


class Deductible(BaseModel):
    percentage: Decimal


class Fee(BaseModel):
    amount: Decimal


class PolicyLimit(BaseModel):
    amount: Decimal


class Premium(BaseModel):
    amount: Decimal


class Rate(BaseModel):
    percentage: Decimal