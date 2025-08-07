# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # 'admin' ou 'shareholder'
    
    shareholder = relationship("Shareholder", back_populates="user", uselist=False)

class Shareholder(Base):
    __tablename__ = "shareholders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="shareholder")
    issuances = relationship("Issuance", back_populates="shareholder")

class Issuance(Base):
    __tablename__ = "issuances"
    id = Column(Integer, primary_key=True, index=True)
    shareholder_id = Column(Integer, ForeignKey("shareholders.id"))
    number_of_shares = Column(Integer)
    price_per_share = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    shareholder = relationship("Shareholder", back_populates="issuances")

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
