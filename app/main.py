from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models.common.user import User, get_user
from utils.database import Base, engine, get_db
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
   