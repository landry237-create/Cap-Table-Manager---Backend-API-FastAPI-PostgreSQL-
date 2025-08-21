#Database.py
 
# Connection à PostgreSQL



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Connexion à PostgreSQL via URL 

#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/cap_table")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/cap_table2")

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Session locale pour interagir avec la base de données
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base de modèle pour déclarer les tables
Base = declarative_base()

"""
🔍 Pourquoi ?

engine : moteur de connexion.

SessionLocal : pour interagir avec la base dans chaque requête.

Base : pour définir les modèles SQLAlchemy

"""