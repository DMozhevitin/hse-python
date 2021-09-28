from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from exception.exceptions import EntityNotFoundException, IllegalArgumentException
from service import user_service
from service import account_service
from model.user import User
from model.account import Account
from model.currency_type import CurrencyType
from typing import Optional, List
from db import account_dao, user_dao
import os

app = FastAPI()

@app.on_event("startup")
async def startup():
    os.environ['USERS_DB_PATH'] = 'db/data/users.pickle'
    os.environ['ACCOUNTS_DB_PATH'] = 'db/data/accounts.pickle'

    init_accounts = {
        1: Account(id=1, owner_id=1, currency_type=CurrencyType.RUB, balance=10_000.0),
        2: Account(id=2, owner_id=1, currency_type=CurrencyType.EUR, balance=100.0),
        3: Account(id=3, owner_id=2, currency_type=CurrencyType.RUB, balance=1000.0)
    }

    init_users = {
        1: User(id=1, name='Ivan Petrov', email='ivanpetrov@gmail.com', account_ids=[1, 2]),
        2: User(id=2, name='Andrey Andreev', email='aa@yandex.ru', account_ids=[3])
    }

    account_dao.delete_all()
    user_dao.delete_all()

    for _, acc in init_accounts.items():
        account_dao.save(acc)

    for _, u in init_users.items():
        user_dao.save(u)

@app.exception_handler(IllegalArgumentException)
async def handle_value_error(request: Request, err: IllegalArgumentException):
    return JSONResponse(status_code=400, content={"detail": err.message})

@app.exception_handler(EntityNotFoundException)
async def handle_not_found_error(request: Request, err: EntityNotFoundException):
    return JSONResponse(status_code=404, content={"detail": err.message})

@app.get("/user/{id}")
async def get_user(id: int) -> User:
    user = user_service.get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User with id {} not found".format(id))
    return user

@app.get("/account/{id}")
async def get_account(id: int) -> Account:
    account = account_service.get_account_by_id(id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account with id {} not found".format(id))
    return account

@app.get("/users")
async def get_users() -> List[User]:
    return user_service.get_all()

@app.get("/accounts")
async def get_accounts() -> List[Account]:
    return account_service.get_all()

@app.post("/account/{id}/refill")
async def refill_account(id: int, amount: Optional[float] = None):
    if amount is not None:
        account_service.refill(id, amount)

@app.post("/account/{id}/withdraw")
async def withdraw_account(id: int, amount: Optional[float] = None):
    if amount is not None:
        account_service.withdraw(id, amount)

@app.post("/account/{id}/transfer")
async def transfer(id: int, to: Optional[int] = None, amount: Optional[float] = None):
    if to is not None and amount is not None:
        account_service.transfer(id, to, amount)
