from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from exception.exceptions import EntityNotFoundException, IllegalArgumentException
from service import account_service
from typing import Optional
import graphql_api
import bootstrap

app = FastAPI()
app.add_route("/", graphql_api.app)

@app.on_event("startup")
async def startup():
    bootstrap.init_db()

@app.exception_handler(IllegalArgumentException)
async def handle_value_error(request: Request, err: IllegalArgumentException):
    return JSONResponse(status_code=400, content={"detail": err.message})

@app.exception_handler(EntityNotFoundException)
async def handle_not_found_error(request: Request, err: EntityNotFoundException):
    return JSONResponse(status_code=404, content={"detail": err.message})

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
