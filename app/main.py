from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .database import Base
from .routers import companies_router, banks_router, bank_accounts_router

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banking API",
    description="API для управления банковскими счетами компаний",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(companies_router)
app.include_router(banks_router)
app.include_router(bank_accounts_router)

@app.get("/")
def read_root():
    return {
        "message": "Banking API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}