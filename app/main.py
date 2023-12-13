from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

# TODO fix class
from schema.user import UserCreate, UserUpdate, User 
from crud.crud_user import user
from core.database import Base, engine, get_db
from core.load_config import settings
from schema.token import AuthRequest, AuthResponse
from core.security import create_access_token

Base.metadata.create_all(bind=engine)

router = FastAPI()

@router.get("/", response_model=dict, status_code=200)
def get_status():
    return {"status" : "Server up and running!"}

@router.get("/users/{roll_number}", response_model=User)
def read_user(roll_number: int, db: Session = Depends(get_db)):
    db_user = user.get(db, roll_number)
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
def add_new_user(req: UserCreate, db: Session = Depends(get_db)):
    try:
        user.create(db=db, obj_in=req)
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not acceptable content")
    
@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(req: AuthRequest, db: Session = Depends(get_db)):
    db_user = user.authenticate_user(db, req)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(req)
    return AuthResponse(token=token)
