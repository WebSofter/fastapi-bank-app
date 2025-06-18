from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class BankAccountBase(BaseModel):
    account_number: str = Field(..., min_length=20, max_length=20, description="Номер банковского счета")
    company_id: int = Field(..., description="ID компании")
    bank_id: int = Field(..., description="ID банка")
    currency: str = Field("RUB", min_length=3, max_length=3, description="Валюта счета")
    is_active: str = Field("Y", pattern="^[YN]$", description="Активен ли счет (Y/N)")
    
    @field_validator('account_number')
    def validate_account_number(cls, v):
        if not re.match(r'^\d{20}$', v):
            raise ValueError('Номер счета должен содержать 20 цифр')
        return v

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountUpdate(BaseModel):
    account_number: Optional[str] = Field(None, min_length=20, max_length=20)
    company_id: Optional[int] = None
    bank_id: Optional[int] = None
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    is_active: Optional[str] = Field(None, pattern="^[YN]$")
    
    @field_validator('account_number')
    def validate_account_number(cls, v):
        if v and not re.match(r'^\d{20}$', v):
            raise ValueError('Номер счета должен содержать 20 цифр')
        return v

class BankAccountResponse(BankAccountBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    company: Optional['CompanyResponse'] = None
    bank: Optional['BankResponse'] = None
    
    class Config:
        from_attributes = True

# Обновляем forward references
from .company import CompanyResponse
from .bank import BankResponse
BankAccountResponse.model_rebuild()
CompanyResponse.model_rebuild()
BankResponse.model_rebuild()