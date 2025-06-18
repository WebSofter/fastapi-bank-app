from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(20), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    bank_id = Column(Integer, ForeignKey("banks.id"), nullable=False)
    currency = Column(String(3), nullable=False, default="RUB")  # Валюта счета
    is_active = Column(String(1), nullable=False, default="Y")  # Активен ли счет
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    company = relationship("Company", back_populates="bank_accounts")
    bank = relationship("Bank", back_populates="bank_accounts")
    
    # Уникальность номера счета в пределах одного банка
    __table_args__ = (
        UniqueConstraint('account_number', 'bank_id', name='unique_account_per_bank'),
    )