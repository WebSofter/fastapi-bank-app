from sqlalchemy.orm import Session, joinedload
from ..models.company import Company
from ..schemas.company import CompanyCreate, CompanyUpdate
from typing import List, Optional

class CompanyCRUD:
    def create(self, db: Session, obj_in: CompanyCreate) -> Company:
        db_obj = Company(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get(self, db: Session, id: int) -> Optional[Company]:
        return db.query(Company).options(joinedload(Company.bank_accounts)).filter(Company.id == id).first()
    
    def get_by_inn(self, db: Session, inn: str) -> Optional[Company]:
        return db.query(Company).filter(Company.inn == inn).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Company]:
        return db.query(Company).options(joinedload(Company.bank_accounts)).offset(skip).limit(limit).all()
    
    def update(self, db: Session, db_obj: Company, obj_in: CompanyUpdate) -> Company:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> Optional[Company]:
        obj = db.query(Company).filter(Company.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

company_crud = CompanyCRUD()