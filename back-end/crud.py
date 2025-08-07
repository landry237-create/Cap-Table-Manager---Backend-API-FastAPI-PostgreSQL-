#Fonctions CRUD (Create, Read, Update, Delete)

# crud.py

from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, auth
from audit import log_event
from email_simulator import send_email

# -------------------------------
# Créer un utilisateur (admin ou actionnaire)
# -------------------------------
def create_user(db: Session, email: str, password: str, role: str):
    hashed_pw = auth.hash_password(password)
    user = models.User(email=email, hashed_password=hashed_pw, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# -------------------------------
# Créer un actionnaire (admin uniquement)
# -------------------------------
def create_shareholder(db: Session, shareholder_data: schemas.ShareholderCreate):
    # Crée d'abord l'utilisateur lié
    user = create_user(db, shareholder_data.email, shareholder_data.password, "shareholder")
    
    # Puis le profil actionnaire
    shareholder = models.Shareholder(name=shareholder_data.name, user_id=user.id)
    db.add(shareholder)
    db.commit()
    db.refresh(shareholder)

    # Journalisation + notification (bonus)
    log_event(db, "create_shareholder", f"Actionnaire {shareholder.name} ajouté.")
    send_email(f"[Notification] Nouveau compte pour {shareholder.name}", shareholder_data.email)

    return shareholder

# -------------------------------
# Lister tous les actionnaires avec le total de leurs actions
# -------------------------------
def get_all_shareholders_with_totals(db: Session):
    result = db.query(
        models.Shareholder.id,
        models.Shareholder.name,
        func.coalesce(func.sum(models.Issuance.number_of_shares), 0).label("total_shares")
    ).outerjoin(models.Issuance).group_by(models.Shareholder.id).all()

    return [{"id": r.id, "name": r.name, "total_shares": r.total_shares} for r in result]

# -------------------------------
# Obtenir un utilisateur par e-mail
# -------------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# -------------------------------
# Obtenir un actionnaire par utilisateur connecté
# -------------------------------
def get_shareholder_by_user(db: Session, user: models.User):
    return db.query(models.Shareholder).filter(models.Shareholder.user_id == user.id).first()

# -------------------------------
# Créer une émission d'actions (admin)
# -------------------------------
def create_issuance(db: Session, issuance_data: schemas.IssuanceCreate):
    # Vérification : nombre positif
    if issuance_data.number_of_shares <= 0:
        raise ValueError("Le nombre d'actions doit être positif")

    shareholder = db.query(models.Shareholder).filter(models.Shareholder.id == issuance_data.shareholder_id).first()
    if not shareholder:
        raise ValueError("Actionnaire inexistant")

    issuance = models.Issuance(
        shareholder_id=issuance_data.shareholder_id,
        number_of_shares=issuance_data.number_of_shares,
        price_per_share=issuance_data.price_per_share
    )
    db.add(issuance)
    db.commit()
    db.refresh(issuance)

    # Journalisation + notification
    log_event(db, "issuance", f"Émission de {issuance.number_of_shares} actions à {shareholder.name}")
    send_email(
        subject=f"[Actions émises] {issuance.number_of_shares} actions ajoutées",
        recipient=shareholder.user.email
    )

    return issuance

# -------------------------------
# Récupérer toutes les émissions (admin ou actionnaire)
# -------------------------------
def get_issuances(db: Session, user: models.User):
    if user.role == "admin":
        return db.query(models.Issuance).all()
    elif user.role == "shareholder":
        shareholder = get_shareholder_by_user(db, user)
        return db.query(models.Issuance).filter(models.Issuance.shareholder_id == shareholder.id).all()
    else:
        return []

# -------------------------------
# Obtenir une émission par ID
# -------------------------------
def get_issuance_by_id(db: Session, issuance_id: int):
    return db.query(models.Issuance).filter(models.Issuance.id == issuance_id).first()

# -------------------------------
# Obtenir tous les événements d'audit (admin uniquement)
# -------------------------------
def get_audit_log(db: Session):
    return db.query(models.AuditEvent).order_by(models.AuditEvent.timestamp.desc()).all()


"""
📌 Commentaires importants
🔐 create_user : fonction générique réutilisée pour actionnaire et admin.

👤 create_shareholder : crée d'abord un utilisateur, puis un actionnaire.

📊 get_all_shareholders_with_totals : agrège les actions par actionnaire.

✅ create_issuance : inclut validation, journalisation (audit), simulation e-mail.

🔍 get_issuances : la logique s’adapte au rôle (admin ou actionnaire).

🕵️ get_audit_log : accessible seulement côté admin.
"""