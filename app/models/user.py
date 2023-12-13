from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from core.database import Base

# like ROOM Entities 
# mapping fns, type converstion eveything should come here
class User(Base):
    __tablename__ = "users"

    roll_number = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    confirmation = Column(String)

    # TODO: items = relationship("Item", back_populates="owner") smth like this is needed later
    # ref: https://fastapi.tiangolo.com/tutorial/sql-databases/



# Classes that are finally used to interact with database. 
# Not sent to anyone from the server
