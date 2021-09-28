from model.account import Account
from typing import List, Optional, Tuple
from exception.exceptions import EntityNotFoundException, IllegalArgumentException
from db import account_dao
from service import payment_comission_service

def check_positive_amount(amount: float):
    if amount <= 0:
        raise IllegalArgumentException('Expected positive amount, but found: {}'.format(amount))

def check_enough_balance(account: int, amount: float):
    if account.balance < amount:
        raise IllegalArgumentException('Not enough balance on account with id {}'.format(account.id))

def get_account_by_id(id: int)-> Optional[Account]:
   return account_dao.load_by_id(id)

def unsafe_get_account_by_id(id: int) -> Account:
    account = get_account_by_id(id)
    if account is None:
        raise EntityNotFoundException('Account with id {} not found'.format(id))
    return account

def get_all() -> List[Account]:
    return account_dao.load_all()

def refill(account_id: int, amount: float) -> Account:
    check_positive_amount(amount)
    account = unsafe_get_account_by_id(account_id)
    account.balance += amount
    account_dao.update(account)
    return account

def withdraw(account_id: int, amount: float) -> Account:
    check_positive_amount(amount)
    account = unsafe_get_account_by_id(account_id)
    check_enough_balance(account, amount)
    account.balance -= amount
    account_dao.update(account)
    return account

def transfer(from_id: int, to_id: int, amount: float) -> Tuple[Account, Account]:
    if from_id == to_id:
        raise IllegalArgumentException('Sender and receiver ids must be different')
    check_positive_amount(amount)
    from_acc = unsafe_get_account_by_id(from_id)
    check_enough_balance(from_acc, amount)
    to_acc = unsafe_get_account_by_id(to_id)
    if from_acc.currency_type != to_acc.currency_type:
        raise IllegalArgumentException(
            'Transfers between accounts with different currency types are prohibited')

    from_acc.balance -= amount
    to_acc.balance += (amount - payment_comission_service.calculate_comission(amount))
    account_dao.update(from_acc)
    account_dao.update(to_acc)

    return (from_acc, to_acc)
