import pickle
from model.user import User
from typing import List, Optional
import os

def get_db_path():
    return os.environ.get('USERS_DB_PATH')

def load_all() -> List[User]:
    db_path = get_db_path()
    with open(db_path, 'rb') as f:
        users = pickle.load(f)
        return users

def save(user: User):
    db_path = get_db_path()
    users = load_all()
    if len(list(filter(lambda u: u.id == user.id, users))) > 0:
        return

    users.append(user)
    with open(db_path, 'wb') as f:
        pickle.dump(users, f)

def load_by_id(id: int) -> Optional[User]:
    users = load_all()
    lst = list(filter(lambda u: u.id == id, users))
    if len(lst) > 0:
        return lst[0]
    else:
        return None

def delete_all():
    db_path = get_db_path()
    with open(db_path, 'wb') as f:
        pickle.dump([], f)
