from typing import Literal

from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    user_id: str
    amount: float = Field(gt=0)
    type: Literal["credit", "debit"]
    transaction_id: str


class TransactionResponse(BaseModel):
    success: bool
    message: str
    balance: float
    transaction_id: str


class UserSummary(BaseModel):
    user_id: str
    balance: float
    total_credited: float
    total_debited: float
    transaction_count: int
    account_age_days: int


class RankedUser(BaseModel):
    rank: int
    user_id: str
    score: float
    balance: float
    transaction_count: int
