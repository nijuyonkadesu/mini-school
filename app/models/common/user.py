from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.database.user import DatabaseUser

# Like Data Access Objects - to create, del, update actions with "models" (entities)
class User(BaseModel):
    roll_number: int
    email: str
    password: str
    confirmation: str
    # if user choose option F (dropout) his creds will be deleted 

    class config:
        orm_mode = True

## All user related CRUD activities are present here:
def get_user(db: Session, roll_number: int):
    return db.query(DatabaseUser).filter(DatabaseUser.roll_number == roll_number).first()

def create_user(db: Session, user: User):
    # TODO: use proper salting
    fake_hashed_password = user.password + "notreallyhashed"

    db_user = DatabaseUser(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return

# Thing sent to and from server are of these classes