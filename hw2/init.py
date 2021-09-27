from model.account import Account
from model.currency_type import CurrencyType
from model.user import User
from db import account_dao, user_dao

init_accounts = {
    1: Account(id=1, owner_id=1, currency_type=CurrencyType.RUB, balance=10_000.0),
    2: Account(id=2, owner_id=1, currency_type=CurrencyType.EUR, balance=100.0),
    3: Account(id=3, owner_id=2, currency_type=CurrencyType.RUB, balance=1000.0)
}

init_users = {
    1: User(id=1, name='Ivan Petrov', email='ivanpetrov@gmail.com', account_ids=[1, 2]),
    2: User(id=2, name='Andrey Andreev', email='aa@yandex.ru', account_ids=[3])
}

for _, acc in init_accounts.items():
    account_dao.save(acc)

for _, u in init_users.items():
    user_dao.save(u)
