from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.bank_account import BankAccountCreate, BankAccountUpdate, BankAccountResponse
from ..crud.bank_account import bank_account_crud
from ..crud.company import company_crud
from ..crud.bank import bank_crud

router = APIRouter(prefix="/bank-accounts", tags=["bank-accounts"])

@router.post("/", response_model=BankAccountResponse, status_code=status.HTTP_201_CREATED)
def create_bank_account(account: BankAccountCreate, db: Session = Depends(get_db)):
    """Создать новый банковский счет"""
    # Проверяем существование компании
    company = company_crud.get(db, id=account.company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Компания не найдена"
        )
    
    # Проверяем существование банка
    bank = bank_crud.get(db, id=account.bank_id)
    if not bank:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Банк не найден"
        )
    
    # Проверяем уникальность номера счета в банке
    existing_account = bank_account_crud.get_by_account_and_bank(
        db, account_number=account.account_number, bank_id=account.bank_id
    )
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Счет с таким номером уже существует в данном банке"
        )
    
    try:
        return bank_account_crud.create(db=db, obj_in=account)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[BankAccountResponse])
def get_bank_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список банковских счетов"""
    return bank_account_crud.get_multi(db=db, skip=skip, limit=limit)

@router.get("/{account_id}", response_model=BankAccountResponse)
def get_bank_account(account_id: int, db: Session = Depends(get_db)):
    """Получить банковский счет по ID"""
    account = bank_account_crud.get(db=db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Банковский счет не найден"
        )
    return account

@router.get("/company/{company_id}", response_model=List[BankAccountResponse])
def get_company_accounts(company_id: int, db: Session = Depends(get_db)):
    """Получить банковские счета компании"""
    # Проверяем существование компании
    company = company_crud.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Компания не найдена"
        )
    
    return bank_account_crud.get_by_company(db=db, company_id=company_id)

@router.put("/{account_id}", response_model=BankAccountResponse)
def update_bank_account(account_id: int, account_update: BankAccountUpdate, db: Session = Depends(get_db)):
    """Обновить банковский счет"""
    account = bank_account_crud.get(db=db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Банковский счет не найден"
        )
    
    # Проверяем существование компании при обновлении
    if account_update.company_id and account_update.company_id != account.company_id:
        company = company_crud.get(db, id=account_update.company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Компания не найдена"
            )
    
    # Проверяем существование банка при обновлении
    if account_update.bank_id and account_update.bank_id != account.bank_id:
        bank = bank_crud.get(db, id=account_update.bank_id)
        if not bank:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Банк не найден"
            )
    
    # Проверяем уникальность номера счета в банке при обновлении
    if (account_update.account_number and account_update.account_number != account.account_number) or \
       (account_update.bank_id and account_update.bank_id != account.bank_id):
        
        check_account_number = account_update.account_number or account.account_number
        check_bank_id = account_update.bank_id or account.bank_id
        
        existing_account = bank_account_crud.get_by_account_and_bank(
            db, account_number=check_account_number, bank_id=check_bank_id
        )
        if existing_account and existing_account.id != account.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Счет с таким номером уже существует в данном банке"
            )
    
    try:
        return bank_account_crud.update(db=db, db_obj=account, obj_in=account_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank_account(account_id: int, db: Session = Depends(get_db)):
    """Удалить банковский счет"""
    account = bank_account_crud.delete(db=db, id=account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Банковский счет не найден"
        )
