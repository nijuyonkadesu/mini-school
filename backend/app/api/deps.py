from datetime import datetime 

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from crud.crud_user import user 
from models.user import User
from schema.token import TokenClaim

from core.load_config import settings

config = settings.app
SECRET_KEY = config["secret_key"]
ALGORITHM = config["algorithm"]

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        token_data = TokenClaim(**payload)

        if token_data.roll_number is None or token_data.expiry < datetime.utcnow():
            raise credentials_exception
        else:
            db_user = user.get(db=db, roll_number=token_data.roll_number)
            if db_user is None:
              raise credentials_exception
            return db_user
        
    except JWTError:
        raise credentials_exception

# this file exsits to prevent cyclic import issues?
# if you see here, the get_current_user function cannot be placed inside core.security 
# because if you place there, core.security will be depend on crud.crud_user
# and, crud.crud_user is already dependent on core.security (see? <-> now there's a loop)
