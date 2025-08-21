# Fonctions CRUD principales

"""
📌 Commentaires importants
🔐 create_user : fonction générique réutilisée pour actionnaire et admin.

👤 create_shareholder : crée d'abord un utilisateur, puis un actionnaire.

📊 get_all_shareholders_with_totals : agrège les actions par actionnaire.

✅ create_issuance : inclut validation, journalisation (audit), simulation e-mail.

🔍 get_issuances : la logique s’adapte au rôle (admin ou actionnaire).

🕵️ get_audit_log : accessible seulement côté admin.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, auth
from audit import log_event
from email_simulator import send_email  # Hypothétique service d'envoi d'email


#------------------------------------
# CRUD pour les utilisateurs (admin et actionnaires)
#------------------------------------

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#------------------------------------
# Créer un actionnaire (admin uniquement)
#------------------------------------
def create_shareholder(db: Session, shareholder: schemas.ShareholderCreate) -> models.Shareholder:
    # Créer d'abord l'utilisateur
    user = schemas.UserCreate(
        email=shareholder.email,
        password=shareholder.password,
        role='shareholder'
    )
    db_user = create_user(db, user)

    # Puis créer l'actionnaire
    db_shareholder = models.Shareholder(
        user_id=db_user.id,
        name=shareholder.name,
        email=shareholder.email
    )
    db.add(db_shareholder)
    db.commit()
    db.refresh(db_shareholder)
    # journalisation + notification (bonus)
    log_event(bd, "create", f"Shareholder {db_shareholder.name} created with ID {db_shareholder.id}")
    send_email(
        to=db_shareholder.email,
        subject="Shareholder Created",
        body=f"Dear {db_shareholder.name}, your shareholder account has been created successfully."
    )
    return db_shareholder

#------------------------------------
# Récupérer tous les actionnaires avec le total des actions
#------------------------------------

def get_all_shareholders_with_totals(db: Session) -> list[schemas.ShareholderOut]:
    shareholders = db.query(
        models.Shareholder,
        func.sum(models.Issuance.number_of_shares).label('total_shares')
    ).join(models.Issuance, models.Shareholder.id == models.Issuance.shareholder_id, isouter=True) \
      .group_by(models.Shareholder.id).all()

    return [
        schemas.ShareholderOut(
            id=sh.id,
            name=sh.name,
            total_shares=total.total_shares if total.total_shares else 0
        ) for sh, total in shareholders
    ]

#------------------------------------
# Obtenir un utilisateur par email
#------------------------------------

def get_shareholder_by_email(db: Session, email: str) -> models.Shareholder:
    return db.query(models.Shareholder).filter(models.Shareholder.email == email).first()

#------------------------------------
# Créer une émission d'actions (admin uniquement)
#------------------------------------

def create_issuance(db: Session, issuance: schemas.IssuanceCreate) -> models.Issuance:
    # Vérification de l'existence de l'actionnaire
    if issuance.number_of_shares <= 0 or issuance.price_per_share <= 0:
        raise ValueError("Number of shares and price per share must be greater than zero.")

    shareholder = db.query(models.Shareholder).filter(models.Shareholder.id == issuance.shareholder_id).first()
    if not shareholder:
        raise ValueError("Shareholder not found.")
    
    # Création de l'émission
    db_issuance = models.Issuance(
        shareholder_id=shareholder.id,
        number_of_shares=issuance.number_of_shares,
        price_per_share=issuance.price_per_share,
        date=issuance.date
    )
    db.add(db_issuance)
    db.commit()
    db.refresh(db_issuance)
    # Journalisation + notification (bonus)
    log_event(db, "create", f"Issuance created for shareholder {shareholder.id} with {issuance.number_of_shares} shares at {issuance.price_per_share} each.")
    send_email(
        to=shareholder.email,
        subject="Issuance Created",
        body=f"Dear {shareholder.name}, your issuance of {issuance.number_of_shares} shares has been created successfully."
    )
    return db_issuance

#------------------------------------
# récupérer toutes les émissions d'actions(admin ou actionnaire)
#------------------------------------

def get_issuances(db: Session, user: models.User) -> list[schemas.IssuanceOut]:
    if user.role == 'admin':
        issuances = db.query(models.Issuance).all()
    elif user.role == 'shareholder':
        issuances = db.query(models.Issuance).filter(models.Issuance.shareholder_id == user.id).all()
    else:
        raise ValueError("Invalid user role.")

    return [schemas.IssuanceOut.from_orm(issuance) for issuance in issuances]

#------------------------------------
# Obtenir une émission par ID
#------------------------------------

def get_issuance_by_id(db: Session, issuance_id: int) -> schemas.IssuanceOut:
    issuance = db.query(models.Issuance).filter(models.Issuance.id == issuance_id).first()
    if not issuance:
        raise ValueError("Issuance not found.")
    return schemas.IssuanceOut.from_orm(issuance)

#------------------------------------
# Obtention du journal d'audit (admin uniquement)
#------------------------------------

def get_audit_log(db: Session) -> list[schemas.AuditEventOut]:
    audit_events = db.query(models.AuditEvent).all()
    return [schemas.AuditEventOut.from_orm(event) for event in audit_events]