from pydantic import BaseModel, Field
from typing import Optional , List
from datetime import datetime


class ExpenseCreate(BaseModel):
    user_id: int
    name: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)  # Ensures amount is positive
    category: str = Field(..., min_length=2, max_length=50)


class ExpenseResponse(ExpenseCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Enables ORM mode if needed later


class ExpenseListResponse(BaseModel):
    expenses: List[ExpenseResponse]  # List of expenses


class ExpenseUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)  # Ensures amount is positive
    category: str = Field(..., min_length=2, max_length=50)