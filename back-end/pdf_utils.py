# Génération de PDF

from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from io import BytesIO
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models, schemas

# Générer un certificat PDF en mémoire, à partir d'une émission d'actions
def generate_certificate(issuance: schemas.IssuanceOut, db: Session) -> BytesIO:
    if not issuance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Issuance not found")
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    #Dimensions et marges
    margin = 50
    text_x = margin
    text_y = height - margin

    # Texte du certificat
    c.setFont("Helvetica", 12)
    c.drawString(text_x, text_y, f"Certificate of Shares")
    text_y -= 20
    c.drawString(text_x, text_y, f"Shareholder: {issuance.shareholder.name}")
    text_y -= 20
    c.drawString(text_x, text_y, f"Email: {issuance.shareholder.email}")
    text_y -= 20
    c.drawString(text_x, text_y, f"Number of Shares: {issuance.number_of_shares}")
    text_y -= 20
    c.drawString(text_x, text_y, f"Price per Share: {issuance.price_per_share:.2f} EUR")
    text_y -= 20
    c.drawString(text_x, text_y, f"Issuance Date: {issuance.date.strftime('%Y-%m-%d')}")

    # signature simulated
    text_y -= 40
    c.drawString(text_x, text_y, "_________________________")
    text_y -= 20
    c.drawString(text_x, text_y, "Authorized Signature")

    # Filigrame
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.8, 0.8, 0.8)
    c.drawString(width - margin - 100, height - margin - 20, "Company Name")
    c.setFillColorRGB(0, 0, 0)

    # Finalisation du PDF
    c.showPage()
    c.save()
    buffer.seek(0)

    return buffer


"""🔍 Pourquoi ReportLab ?

Très robuste, sans dépendances complexes.

Permet la création de PDF à la volée, avec textes, images, filigrane, etc."""