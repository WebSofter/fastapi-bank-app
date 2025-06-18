from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re

class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название компании")
    inn: str = Field(..., min_length=10, max_length=12, description="ИНН компании")
    description: Optional[str] = Field(None, max_length=1000, description="Описание компании")
    
    @validator('inn')
    def validate_inn(cls, v):
        if not re.match(r'^\d{10}$|^\d{12}$', v):
            raise ValueError('ИНН должен содержать 10 или 12 цифр')
        return v

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    inn: Optional[str] = Field(None, min_length=10, max_length=12)
    description: Optional[str] = Field(None, max_length=1000)
    
    @validator('inn')
    def validate_inn(cls, v):
        if v and not re.match(r'^\d{10}$|^\d{12}$', v):
            raise ValueError('ИНН должен содержать 10 или 12 цифр')
        return v

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    bank_accounts: List['BankAccountResponse'] = []
    
    class Config:
        from_attributes = True