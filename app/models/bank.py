from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Bank(Base):
    __tablename__ = "banks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    bik = Column(String(9), nullable=False, unique=True, index=True)  # БИК банка
    correspondent_account = Column(String(20), nullable=True)  # Корреспондентский счет
    address = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связь с банковскими счетами
    bank_accounts = relationship("BankAccount", back_populates="bank", cascade="all, delete-orphan")