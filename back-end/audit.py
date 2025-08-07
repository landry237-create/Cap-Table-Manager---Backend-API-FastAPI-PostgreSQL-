# audit.py

from sqlalchemy.orm import Session
import models
from datetime import datetime

# Fonction pour enregistrer un événement critique
def log_event(db: Session, event_type: str, description: str):
    event = models.AuditEvent(
        event_type=event_type,
        description=description,
        timestamp=datetime.utcnow()
    )
    db.add(event)
    db.commit()
