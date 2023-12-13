from typing import Optional 

from pydantic import BaseModel
from pydantic import EmailStr 

# Like Data Access Objects - to create, del, update actions with "schema" pydantic model / (entities)
class UserBase(BaseModel):
    roll_number: Optional[int] = None
    email:Optional[EmailStr] = None
    confirmation: Optional[str] = "A"
    # if user choose option F (dropout) his creds will be deleted 

    class config:
        orm_mode = True


# These are received to the API
class UserCreate(UserBase):
    roll_number: int
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: str


#------------- DB Classes ------------

class UserInDBBase(UserBase): 
    password: Optional[str] = None

    class Config:
        orm_mode = True

# Only this class must be exposed via API
class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str


