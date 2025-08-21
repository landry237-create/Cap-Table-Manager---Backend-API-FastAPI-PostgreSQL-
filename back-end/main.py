# Point d'entrée de l'application FastAPI

"""
Ce projet simule une plateforme d’administration du tableau de capitalisation d’entreprise, permettant à un administrateur de :

gérer les actionnaires,
émettre des actions,
générer des certificats PDF,
consulter les journaux d’audit.
Les actionnaires peuvent consulter leurs actions et télécharger leurs certificats.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth, crud
from database import SessionLocal, engine, Base
from pdf_utils import generate_certificate
from fastapi.responses import JSONResponse, StreamingResponse


# Création de l'application FastAPI
app = FastAPI()

# Dependance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour la connexion : retourne un token JWT
@app.post("/api/token/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"email": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
# Crée automatiquement les tables dans la base de données si elles n'existent pas
#Base.metadata.create_all(bind=engine)

#from fastapi.response import JSONResponse, StreamingResponse

import pdf_utils

#--------------------------------------
# Récupérer la liste des actionnaires(admin uniquement)
#--------------------------------------
@app.get("/api/shareholders/", response_model=list[schemas.ShareholderOut])
def get_all_shareholders(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    shareholders = crud.get_all_shareholders_with_totals(db)
    return shareholders

#--------------------------------------
# Emettre des actions (admin uniquement)
#--------------------------------------
@app.post("/api/shareholders/{shareholder_id}/issuances/", response_model=schemas.ShareholderOut)
def create_issuance(shareholder_id: int, issuance: schemas.IssuanceCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    db_issuance = crud.create_issuance(db, issuance, shareholder_id)
    return db_issuance

#--------------------------------------
# Lister les émissions d'actions (admin ou actionnaire)
#--------------------------------------
@app.get("/api/shareholders/{shareholder_id}/issuances/", response_model=list[schemas.IssuanceCreate])
def get_issuances(shareholder_id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    if current_user.role not in ['admin', 'shareholder']:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    issuances = crud.get_issuances_by_shareholder(db, shareholder_id)
    return issuances

#--------------------------------------
# Telecharger le certificat PDF d'un (admin ou actionnaire concerné)
#--------------------------------------
@app.get("/api/shareholders/{shareholder_id}/certificate/", response_class=StreamingResponse)
def download_certificate(shareholder_id: int, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    if current_user.role not in ['admin', 'shareholder']:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    shareholder = crud.get_shareholder_by_id(db, shareholder_id)
    if not shareholder:
        raise HTTPException(status_code=404, detail="Shareholder not found")
    
    # Générer le certificat PDF
    pdf_content = pdf_utils.generate_certificate(shareholder)
    
    # Retourner le PDF en tant que réponse
    return StreamingResponse(pdf_content, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=certificate_{shareholder_id}.pdf"})

#--------------------------------------
# Enregistrer un nouvel actionnaire (admin uniquement)
#--------------------------------------
@app.post("/api/shareholders/", response_model=schemas.ShareholderOut)
def create_shareholder(shareholder: schemas.ShareholderCreate, db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
    
    # Vérification de l'existence de l'actionnaire
    existing_shareholder = crud.get_shareholder_by_email(db, shareholder.email)
    if existing_shareholder:
        raise HTTPException(status_code=400, detail="Shareholder already exists")
    
    # Création de l'actionnaire
    db_shareholder = crud.create_shareholder(db, shareholder)
    
    # Journalisation de l'évènement
    auth.log_event(db, schemas.AuditLogCreate(
        action="create_shareholder",
        user_id=current_user.id,
        details=f"Shareholder {db_shareholder.name} created."
    ))
    
    return db_shareholder