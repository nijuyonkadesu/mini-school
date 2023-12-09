from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.common.user import User, get_user

SECRET_KEY = "pythonvenvadventurestoriesinsidewinhoes10"
ALGORITHM = "HS256"
EXPIRE_DAYS = 30

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
# Hashes are automatically salted, the salt is in the hash itself
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthRequest(BaseModel):
    roll_number: int
    password: str

class AuthResponse(BaseModel):
    token: str

class TokenClaim(BaseModel):
    roll_number: int
    expiry: datetime

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_salted_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, req: AuthRequest):
    user = get_user(db, req.roll_number)
    if not user:
        return False
    if not verify_password(req.password, user.hashed_password):
        return False
    return user

def create_access_token(data: AuthRequest) -> str:
    expiry = (datetime.utcnow() + timedelta(days=EXPIRE_DAYS)).timestamp()
    token_data = {
        "roll_number": data.roll_number,
        "expiry": expiry
    }
    encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str, db: Session) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenClaim(
            roll_number=payload.get("roll_number"),
            expiry=payload.get("expiry")
        )

        if token_data.roll_number is None or token_data.expiry < datetime.utcnow():
            raise credentials_exception
        else:
            user = get_user(db, token_data.roll_number)
            if user is None:
              raise credentials_exception
            return user
        
    except JWTError:
        raise credentials_exception
