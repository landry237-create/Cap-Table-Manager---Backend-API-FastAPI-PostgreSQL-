# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Connexion à PostgreSQL via URL (tu dois adapter à ton .env)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/cap_table")

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Session locale pour interagir avec la base de données
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base de modèle pour déclarer les tables
Base = declarative_base()
