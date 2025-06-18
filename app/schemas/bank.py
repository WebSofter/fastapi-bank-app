from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import re


class BankBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название банка")
    bik: str = Field(..., min_length=9, max_length=9, description="БИК банка")
    correspondent_account: Optional[str] = Field(None, min_length=20, max_length=20, description="Корреспондентский счет")
    address: Optional[str] = Field(None, max_length=500, description="Адрес банка")
    
    @field_validator('bik')
    def validate_bik(cls, v):
        if not re.match(r'^\d{9}$', v):
            raise ValueError('БИК должен содержать 9 цифр')
        return v
    
    @field_validator('correspondent_account')
    def validate_correspondent_account(cls, v):
        if v and not re.match(r'^\d{20}$', v):
            raise ValueError('Корреспондентский счет должен содержать 20 цифр')
        return v

class BankCreate(BankBase):
    pass

class BankUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    bik: Optional[str] = Field(None, min_length=9, max_length=9)
    correspondent_account: Optional[str] = Field(None, min_length=20, max_length=20)
    address: Optional[str] = Field(None, max_length=500)
    
    @field_validator('bik')
    def validate_bik(cls, v):
        if v and not re.match(r'^\d{9}$', v):
            raise ValueError('БИК должен содержать 9 цифр')
        return v
    
    @field_validator('correspondent_account')
    def validate_correspondent_account(cls, v):
        if v and not re.match(r'^\d{20}$', v):
            raise ValueError('Корреспондентский счет должен содержать 20 цифр')
        return v

class BankResponse(BankBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    bank_accounts: List['BankAccountResponse'] = []
    
    class Config:
        from_attributes = True
