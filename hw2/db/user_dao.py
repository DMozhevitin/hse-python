import pickle
from model.user import User
from typing import List, Optional
import os

DB_PATH = 'db/data/users.pickle'

def init():
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'wb') as f:
            pickle.dump([], f)

init()

def load_all() -> List[User]:
    with open(DB_PATH, 'rb') as f:
        users = pickle.load(f)
        return users

def save(user: User):
    users = load_all()
    if len(list(filter(lambda u: u.id == user.id, users))) > 0:
        return

    users.append(user)
    with open(DB_PATH, 'wb') as f:
        pickle.dump(users, f)

def load_by_id(id: int) -> Optional[User]:
    users = load_all()
    lst = list(filter(lambda u: u.id == id, users))
    if len(lst) > 0:
        return lst[0]
    else:
        return None
