# Enregistrement des évènements critiques

from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas

# fonction pour enregistrer un évènement critique dans la base de données
def log_event(db: Session, event: schemas.AuditEventCreate) -> models.AuditEvent:
    db_event = models.AuditLog(
        action=event.action,
        user_id=event.user_id,
        timestamp=datetime.utcnow(),
        details=event.details
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

    # Envoi d'un email de confirmation (hypothétique)
    send_email(
        to=db_shareholder.email,
        subject="Shareholder Created",
        body=f"Dear {db_shareholder.name}, your shareholder account has been created."
    )

    # Log de l'évènement
    log_event(db, schemas.AuditLogCreate(
        action="create_shareholder",
        user_id=db_user.id,
        details=f"Shareholder {db_shareholder.name} created."
    ))

    return db_shareholder
"""🔍 Permet de traquer toutes les actions sensibles dans le système :

Création d'actionnaire

Connexion

Émission d’actions"""