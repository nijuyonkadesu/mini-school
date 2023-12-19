from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from models.user import User
from schema.user import UserCreate, UserUpdate
from crud.base import CRUDBase
from core.security import get_salted_hash, verify_password
from schema.token import AuthRequest

# update create and update schema
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    CRUD operations for anything that deals with User table
    """
    def create(self, db: Session, *, obj_in: UserCreate) -> Optional[User]:
        db_obj = User(
                roll_number=obj_in.roll_number,
                email=obj_in.email,
                hashed_password= get_salted_hash(obj_in.password),
                confirmation=obj_in.confirmation
                )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # dict is to update the entire data, or a subset of the UserUpdate propertes
    def update(self, db:Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> Optional[User]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data["password"]:
            hashed_password = get_salted_hash(update_data["password"])
            del update_data["password"]
            update_data["password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate_user(self, db: Session, req: AuthRequest):
        db_user = user.get(db, req.roll_number)
        if not db_user:
            return False
        if not verify_password(req.password, db_user.hashed_password):
            return False
        return user
            
user = CRUDUser(User)
