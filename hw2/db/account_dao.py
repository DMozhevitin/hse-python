import pickle
from model.account import Account
import os
from typing import List, Optional
from exception.exceptions import EntityNotFoundException

def get_db_path():
    return os.environ.get('ACCOUNTS_DB_PATH')

def load_all() -> List[Account]:
    db_path = get_db_path()
    with open(db_path, 'rb') as f:
        accounts = pickle.load(f)
        return accounts

def save(account: Account):
    db_path = get_db_path()
    accounts = load_all()
    if len(list(filter(lambda a: a.id == account.id, accounts))) > 0:
        return

    accounts.append(account)
    with open(db_path, 'wb') as f:
        pickle.dump(accounts, f)

def load_by_id(id: int) -> Optional[Account]:
    accounts = load_all()
    lst = list(filter(lambda a: a.id == id, accounts))
    if len(lst) > 0:
        return lst[0]
    else:
        return None

def load_by_owner_id(owner_id: int) -> List[Account]:
    accounts = load_all()
    owner_accounts = filter(lambda a: a.owner_id == owner_id, accounts)

    return owner_accounts

def update(account: Account):
    db_path = get_db_path()
    accounts = load_all()
    i = None

    for idx, acc in enumerate(accounts):
        if acc.id == account.id:
            i = idx
            break

    if i is None:
        raise EntityNotFoundException("Account with id {} doesn't exist".format(account.id))

    accounts[i] = account
    with open (db_path, 'wb') as f:
        pickle.dump(accounts, f)

def delete_all():
    db_path = get_db_path()
    with open(db_path, 'wb') as f:
        pickle.dump([], f)
