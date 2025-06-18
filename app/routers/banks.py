from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.bank import BankCreate, BankUpdate, BankResponse
from ..crud.bank import bank_crud

router = APIRouter(prefix="/banks", tags=["banks"])

@router.post("/", response_model=BankResponse, status_code=status.HTTP_201_CREATED)
def create_bank(bank: BankCreate, db: Session = Depends(get_db)):
    """Создать новый банк"""
    # Проверяем уникальность БИК
    existing_bank = bank_crud.get_by_bik(db, bik=bank.bik)
    if existing_bank:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Банк с таким БИК уже существует"
        )
    return bank_crud.create(db=db, obj_in=bank)

@router.get("/", response_model=List[BankResponse])
def get_banks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список банков"""
    return bank_crud.get_multi(db=db, skip=skip, limit=limit)

@router.get("/{bank_id}", response_model=BankResponse)
def get_bank(bank_id: int, db: Session = Depends(get_db)):
    """Получить банк по ID"""
    bank = bank_crud.get(db=db, id=bank_id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Банк не найден"
        )
    return bank

@router.put("/{bank_id}", response_model=BankResponse)
def update_bank(bank_id: int, bank_update: BankUpdate, db: Session = Depends(get_db)):
    """Обновить банк"""
    bank = bank_crud.get(db=db, id=bank_id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Банк не найден"
        )
    
    # Проверяем уникальность БИК при обновлении
    if bank_update.bik and bank_update.bik != bank.bik:
        existing_bank = bank_crud.get_by_bik(db, bik=bank_update.bik)
        if existing_bank:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Банк с таким БИК уже существует"
            )
    
    return bank_crud.update(db=db, db_obj=bank, obj_in=bank_update)

@router.delete("/{bank_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank(bank_id: int, db: Session = Depends(get_db)):
    """Удалить банк"""
    bank = bank_crud.delete(db=db, id=bank_id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Банк не найден"
        )