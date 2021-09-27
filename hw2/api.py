from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from exception.exceptions import EntityNotFoundException, IllegalArgumentException
from service import user_service
from service import account_service
from model.user import User
from model.account import Account
from typing import Optional, List

app = FastAPI()

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
    user_service.get_all()

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
