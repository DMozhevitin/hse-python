from model.user import User
from typing import List, Optional
import db.user_dao

def get_user_by_id(id: int) -> Optional[User]:
    return db.user_dao.load_by_id(id)

def get_all() -> List[User]:
    return db.user_dao.load_all()
