#Schémas Pydantic (entrées/sorties)

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Generic, TypeVar
from pydantic.generics import GenericModel
from datetime import datetime


""" Ce projet simule une plateforme d’administration du tableau de capitalisation d’entreprise, permettant à un administrateur de :
gérer les actionnaires,
émettre des actions,
générer des certificats PDF,
consulter les journaux d’audit.
Les actionnaires peuvent consulter leurs actions et télécharger leurs certificats.
"""

"""🔍 Pourquoi ?

Les schémas Pydantic sont utilisés pour valider les données entrantes et formater les réponses sortantes."""
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    #username: str
    #role: Optional[str] = None  # 'admin' or 'user'
    email: Optional[EmailStr] = None

class UserCreate(BaseModel):
    #username: str
    #id: Optional[int] = None
    
    email: EmailStr
    #full_name: Optional[str] = None
    password: str
    role: str # 'admin' or 'shareholder'

class UserOut(BaseModel):
    id: int
    email: EmailStr
    #full_name: Optional[str] = None
    role: str  # 'admin' or 'shareholder'
    is_active: bool = True

    class Config:
        orm_mode = True

class ShareholderCreate(BaseModel):
    name: str
    email: EmailStr
    #number_of_shares: int
    #price_per_share: float
    password: str

class ShareholderOut(BaseModel):
    id: int
    name: str
    #email: EmailStr
    #number_of_shares: int
    #price_per_share: float
    #created_at: datetime
    total_shares: int

    class Config:
        orm_mode = True

class IssuanceCreate(BaseModel):
    shareholder_id: int
    number_of_shares: int
    price_per_share: float

class IssuanceOut(BaseModel):
    id: int
    shareholder_id: int
    number_of_shares: int
    price_per_share: float
    date: datetime

    class Config:
        orm_mode = True

class AuditEventCreate(BaseModel):
    event_type: str  # e.g., 'create', 'update', 'delete'
    description: str
    user_id: int

class AuditEventOut(BaseModel):
    id: int
    event_type: str
    description: str
    timestamp: datetime
    #user_id: int

    class Config:
        orm_mode = True
