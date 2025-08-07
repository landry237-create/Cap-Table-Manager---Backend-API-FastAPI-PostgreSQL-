# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models, schemas, auth, crud
from database import Base, engine, SessionLocal

# Crée automatiquement les tables dans la base de données si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dépendance de session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route pour la connexion : retourne un token JWT
@app.post("/api/token/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    
    token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}



"""
✅ Explications

OAuth2PasswordRequestForm permet de soumettre username et password (le champ username correspond à l’email ici).

Le JWT est généré si l’utilisateur est valide.

Cette route est celle qui alimente le frontend pour l’authentification (POST /api/token/).


"""

# ... suite de main.py ...

from fastapi.responses import StreamingResponse
from app import pdf_utils

# -------------------------
# 🔐 Récupérer la liste des actionnaires (admin)
# -------------------------
@app.get("/api/shareholders/")
def list_shareholders(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    return crud.get_all_shareholders_with_totals(db)

# -------------------------
# ➕ Ajouter un nouvel actionnaire (admin)
# -------------------------
@app.post("/api/shareholders/")
def add_shareholder(payload: schemas.ShareholderCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    return crud.create_shareholder(db, payload)

# -------------------------
# 🧾 Émettre des actions pour un actionnaire (admin)
# -------------------------
@app.post("/api/issuances/")
def issue_shares(payload: schemas.IssuanceCreate, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Accès refusé")
    try:
        return crud.create_issuance(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -------------------------
# 📋 Lister les émissions d’actions (admin ou actionnaire)
# -------------------------
@app.get("/api/issuances/")
def list_issuances(db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    return crud.get_issuances(db, current_user)

# -------------------------
# 📄 Télécharger un certificat PDF (admin ou actionnaire concerné)
# -------------------------
@app.get("/api/issuances/{issuance_id}/certificate/")
def download_certificate(issuance_id: int, db: Session = Depends(get_db), current_user = Depends(auth.get_current_user)):
    issuance = crud.get_issuance_by_id(db, issuance_id)

    if current_user.role == "shareholder":
        shareholder = crud.get_shareholder_by_user(db, current_user)
        if issuance.shareholder_id != shareholder.id:
            raise HTTPException(status_code=403, detail="Non autorisé")

    pdf_file = pdf_utils.generate_certificate_pdf(issuance)
    return StreamingResponse(pdf_file, media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=certificat_{issuance.id}.pdf"
    })
