from datetime import datetime

from pydantic import BaseModel

class AuthRequest(BaseModel):
    roll_number: int
    password: str

class AuthResponse(BaseModel):
    token: str

class TokenClaim(BaseModel):
    roll_number: int
    expiry: datetime
