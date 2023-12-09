from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.common.user import User, get_user
from models.database.user import DatabaseUser
from models.common.user import get_user, create_user
from utils.database import Base, engine, get_db
from utils.auth import AuthRequest, AuthResponse, authenticate_user, create_access_token
from utils.load_config import settings

Base.metadata.create_all(bind=engine)

router = FastAPI()

@router.get("/", response_model=dict, status_code=200)
def get_status():
    return {"status" : "Server up and running!"}

@router.get("/users/{roll_number}", response_model=User)
def read_user(roll_number: int, db: Session = Depends(get_db)):
    db_user = get_user(db, roll_number)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/secret")
async def info():
   return {
       "database": settings.database,
       "app": settings.app,
   }
   
@router.post("/users/add", status_code=status.HTTP_200_OK)
def add_new_user(user: User, db: Session = Depends(get_db)):
    try:
        create_user(db, user)
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not acceptable content")
    
@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(req: AuthRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, req)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(req)
    return AuthResponse(token=token)