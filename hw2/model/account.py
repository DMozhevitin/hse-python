from pydantic import BaseModel
from model.currency_type import CurrencyType

class Account(BaseModel):
    id: int
    owner_id: int
    currency_type: CurrencyType
    balance: float
