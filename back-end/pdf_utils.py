# pdf_utils.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from fastapi import HTTPException
import models

# Génère un certificat PDF en mémoire, à partir d’une émission d’actions
def generate_certificate_pdf(issuance: models.Issuance) -> BytesIO:
    if not issuance:
        raise HTTPException(status_code=404, detail="Émission introuvable")

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Dimensions
    width, height = A4

    # Texte du certificat
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 100, "Certificat d'Émission d'Actions")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, f"Nom de l'actionnaire : {issuance.shareholder.name}")
    c.drawString(100, height - 170, f"Nombre d'actions émises : {issuance.number_of_shares}")
    c.drawString(100, height - 190, f"Prix par action : {issuance.price_per_share} €")
    c.drawString(100, height - 210, f"Date d'émission : {issuance.date.strftime('%d/%m/%Y')}")

    # Signature simulée
    c.drawString(100, height - 260, "Signature de l'entreprise : ___________________")

    # Filigrane (simple)
    c.setFont("Helvetica-Bold", 60)
    c.setFillGray(0.85, 0.5)
    c.saveState()
    c.translate(width / 3, height / 3)
    c.rotate(45)
    c.drawCentredString(0, 0, "CONFIDENTIEL")
    c.restoreState()

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
