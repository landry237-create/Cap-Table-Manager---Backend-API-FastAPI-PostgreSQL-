
"""
Ce projet simule une plateforme d’administration du tableau de capitalisation d’entreprise, permettant à un administrateur de :

gérer les actionnaires,
émettre des actions,
générer des certificats PDF,
consulter les journaux d’audit.
Les actionnaires peuvent consulter leurs actions et télécharger leurs certificats.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

# Définition des modèles SQlAlchemy

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String)
    role = Column(String, default='user')  # 'admin' or 'user'

    # Additional fields for user management
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Shareholder
    shareholders = relationship("Shareholder", back_populates="user")

class Shareholder(Base):
    __tablename__ = 'issuances'
    id = Column(Integer, primary_key=True, index=True)
    Shareholder_id = Column(Integer, ForeignKey('shareholder.id'))
    number_of_shares = Column(Integer, nullable=False)
    price_per_share = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    # Relationship with User
    Shareholder = relationship("User", back_populates="shareholders")

class AuditEvent(Base):
    __tablename__ = 'audit_events'
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)  # e.g., 'create', 'update', 'delete'
    description = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Additional fields for audit logging
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="audit_events")

class Issuance(Base):
    __tablename__ = 'issuances'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    Shareholder_id = Column(Integer, ForeignKey('shareholders.id'))
    number_of_shares=Column(Integer)
    price_per_share = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    Shareholder = relationship('Shareholder', back_populates = 'issuances')
    


