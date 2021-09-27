from pydantic import BaseModel
from typing import List
from model.account import Account

class User(BaseModel):
    id: int
    name: str
    email: str
    account_ids: List[int]
