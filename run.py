#!/usr/bin/env python3
"""
Скрипт для запуска приложения и выполнения базовых операций
"""

import uvicorn
import asyncio
import httpx
import json
from app.main import app

async def test_api():
    """Тестирование основных API endpoints"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("🚀 Тестирование Banking API...")
        
        # 1. Создание банка
        print("\n1. Создание банка...")
        bank_data = {
            "name": "Сбербанк России",
            "bik": "044525225",
            "correspondent_account": "30101810400000000225",
            "address": "Москва, ул. Вавилова, 19"
        }
        
        response = await client.post(f"{base_url}/banks/", json=bank_data)
        if response.status_code == 201:
            bank = response.json()
            bank_id = bank["id"]
            print(f"✅ Банк создан: {bank['name']} (ID: {bank_id})")
        else:
            print(f"❌ Ошибка создания банка: {response.text}")
            return
        
        # 2. Создание компании
        print("\n2. Создание компании...")
        company_data = {
            "name": "ООО Тестовая Компания",
            "inn": "7707083893",
            "description": "Тестовая компания для демонстрации API"
        }
        
        response = await client.post(f"{base_url}/companies/", json=company_data)
        if response.status_code == 201:
            company = response.json()
            company_id = company["id"]
            print(f"✅ Компания создана: {company['name']} (ID: {company_id})")
        else:
            print(f"❌ Ошибка создания компании: {response.text}")
            return
        
        # 3. Создание банковского счета
        print("\n3. Создание банковского счета...")
        account_data = {
            "account_number": "40702810200000000001",
            "company_id": company_id,
            "bank_id": bank_id,
            "currency": "RUB",
            "is_active": "Y"
        }
        
        response = await client.post(f"{base_url}/bank-accounts/", json=account_data)
        if response.status_code == 201:
            account = response.json()
            account_id = account["id"]
            print(f"✅ Банковский счет создан: {account['account_number']} (ID: {account_id})")
        else:
            print(f"❌ Ошибка создания банковского счета: {response.text}")
            return
        
        # 4. Получение компании со счетами
        print("\n4. Получение компании со счетами...")
        response = await client.get(f"{base_url}/companies/{company_id}")
        if response.status_code == 200:
            company_with_accounts = response.json()
            print(f"✅ Компания получена: {company_with_accounts['name']}")
            print(f"   Количество счетов: {len(company_with_accounts['bank_accounts'])}")
        else:
            print(f"❌ Ошибка получения компании: {response.text}")
        
        # 5. Получение банка со счетами
        print("\n5. Получение банка со счетами...")
        response = await client.get(f"{base_url}/banks/{bank_id}")
        if response.status_code == 200:
            bank_with_accounts = response.json()
            print(f"✅ Банк получен: {bank_with_accounts['name']}")
            print(f"   Количество счетов: {len(bank_with_accounts['bank_accounts'])}")
        else:
            print(f"❌ Ошибка получения банка: {response.text}")
        
        # 6. Получение банковского счета
        print("\n6. Получение банковского счета...")
        response = await client.get(f"{base_url}/bank-accounts/{account_id}")
        if response.status_code == 200:
            account_detail = response.json()
            print(f"✅ Банковский счет получен: {account_detail['account_number']}")
            print(f"   Компания: {account_detail['company']['name']}")
            print(f"   Банк: {account_detail['bank']['name']}")
        else:
            print(f"❌ Ошибка получения банковского счета: {response.text}")
        
        print("\n🎉 Тестирование завершено успешно!")

def run_server():
    """Запуск сервера"""
    print("🚀 Запуск Banking API сервера...")
    print("📖 Документация доступна по адресу: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Запуск тестов
        asyncio.run(test_api())
    else:
        # Запуск сервера
        run_server()