from sqlalchemy.orm import Session, joinedload
from ..models.bank import Bank
from ..schemas.bank import BankCreate, BankUpdate
from typing import List, Optional

class BankCRUD:
    def create(self, db: Session, obj_in: BankCreate) -> Bank:
        db_obj = Bank(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Bank]:
        return db.query(Bank).options(joinedload(Bank.bank_accounts)).filter(Bank.id == id).first()
    
    def get_by_bik(self, db: Session, bik: str) -> Optional[Bank]:
        return db.query(Bank).filter(Bank.bik == bik).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Bank]:
        return db.query(Bank).options(joinedload(Bank.bank_accounts)).offset(skip).limit(limit).all()
    
    def update(self, db: Session, db_obj: Bank, obj_in: BankUpdate) -> Bank:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> Optional[Bank]:
        obj = db.query(Bank).filter(Bank.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

bank_crud = BankCRUD()