from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from ..crud.company import company_crud

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Создать новую компанию"""
    # Проверяем уникальность ИНН
    existing_company = company_crud.get_by_inn(db, inn=company.inn)
    if existing_company:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Компания с таким ИНН уже существует"
        )
    return company_crud.create(db=db, obj_in=company)

@router.get("/", response_model=List[CompanyResponse])
def get_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список компаний"""
    return company_crud.get_multi(db=db, skip=skip, limit=limit)

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    """Получить компанию по ID"""
    company = company_crud.get(db=db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Компания не найдена"
        )
    return company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, company_update: CompanyUpdate, db: Session = Depends(get_db)):
    """Обновить компанию"""
    company = company_crud.get(db=db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Компания не найдена"
        )
    
    # Проверяем уникальность ИНН при обновлении
    if company_update.inn and company_update.inn != company.inn:
        existing_company = company_crud.get_by_inn(db, inn=company_update.inn)
        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Компания с таким ИНН уже существует"
            )
    
    return company_crud.update(db=db, db_obj=company, obj_in=company_update)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Удалить компанию"""
    company = company_crud.delete(db=db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Компания не найдена"
        )