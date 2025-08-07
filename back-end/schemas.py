# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # 'admin' ou 'shareholder'

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class ShareholderCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class ShareholderOut(BaseModel):
    id: int
    name: str
    total_shares: int

    class Config:
        orm_mode = True

class IssuanceCreate(BaseModel):
    shareholder_id: int
    number_of_shares: int
    price_per_share: float

class IssuanceOut(BaseModel):
    id: int
    number_of_shares: int
    price_per_share: float
    date: datetime

    class Config:
        orm_mode = True

class AuditEventOut(BaseModel):
    id: int
    event_type: str
    description: str
    timestamp: datetime

    class Config:
        orm_mode = True
