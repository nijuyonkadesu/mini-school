from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

from schema.token import AuthRequest
from .load_config import settings

config = settings.app
SECRET_KEY = config["secret_key"]
ALGORITHM = config["algorithm"]
EXPIRE_DAYS = config["expire_days"]

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

# Hashes are automatically salted, the salt is in the hash itself
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_salted_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: AuthRequest) -> str:
    expiry = (datetime.utcnow() + timedelta(days=EXPIRE_DAYS)).timestamp()
    token_data = {
            "roll_number": data.roll_number,
            "expiry": expiry
            }
    encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

