from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from ..models.bank_account import BankAccount
from ..schemas.bank_account import BankAccountCreate, BankAccountUpdate
from typing import List, Optional

class BankAccountCRUD:
    def create(self, db: Session, obj_in: BankAccountCreate) -> BankAccount:
        db_obj = BankAccount(**obj_in.dict())
        db.add(db_obj)
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            db.rollback()
            raise ValueError("Счет с таким номером уже существует в данном банке")
    
    def get(self, db: Session, id: int) -> Optional[BankAccount]:
        return db.query(BankAccount).options(
            joinedload(BankAccount.company),
            joinedload(BankAccount.bank)
        ).filter(BankAccount.id == id).first()
    
    def get_by_account_and_bank(self, db: Session, account_number: str, bank_id: int) -> Optional[BankAccount]:
        return db.query(BankAccount).filter(
            BankAccount.account_number == account_number,
            BankAccount.bank_id == bank_id
        ).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[BankAccount]:
        return db.query(BankAccount).options(
            joinedload(BankAccount.company),
            joinedload(BankAccount.bank)
        ).offset(skip).limit(limit).all()
    
    def get_by_company(self, db: Session, company_id: int) -> List[BankAccount]:
        return db.query(BankAccount).options(
            joinedload(BankAccount.bank)
        ).filter(BankAccount.company_id == company_id).all()
    
    def update(self, db: Session, db_obj: BankAccount, obj_in: BankAccountUpdate) -> BankAccount:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError:
            db.rollback()
            raise ValueError("Счет с таким номером уже существует в данном банке")
    
    def delete(self, db: Session, id: int) -> Optional[BankAccount]:
        obj = db.query(BankAccount).filter(BankAccount.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

bank_account_crud = BankAccountCRUD()
