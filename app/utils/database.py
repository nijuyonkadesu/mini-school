from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.load_config import settings
secrets = settings.database

DATABASE_URL = f"postgresql://{secrets["user"]}:{secrets["password"]}@{secrets["host"]}:{secrets["port"]}/{secrets["dbname"]}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# this is used to create sql tables
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
