# email_simulator.py

# simulateur d'envoi d'emails pour les tests en l'affichant dans la console

"""def send_email(subject: str, body: str, to: str, recipient_name: str = None):
    print(f"Email sent to {to} ({recipient_name}):")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print("-" * 40)
    db_user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Log de l'évènement
    log_event(db, schemas.AuditLogCreate(
        action="send_email",
        user_id=db_user.id,
        details=f"Email sent to {to} with subject '{subject}'."
    ))
    
    return {"message": "Email sent successfully."}

🔍 Pourquoi un simulateur d'email ?"""

# email_simulator.py

# Simule un envoi d’e-mail en l’affichant dans la console
def send_email(subject: str, recipient: str):
    print(f"\n[📧 EMAIL SIMULÉ]")
    print(f"À : {recipient}")
    print(f"Sujet : {subject}")
    print("Contenu : Cet email est une simulation de notification.")
    print("-" * 50)
# Utilisé pour les tests et le développement
# Permet de vérifier le format et le contenu sans envoyer de vrais emails
# Utile pour les environnements de test ou de développement où l'envoi d'emails n'est pas souhaité
# Évite les dépendances externes et les configurations d'email en production
# Permet de valider la logique d'envoi d'emails sans effets secondaires

"""🔍 Pourquoi simuler ?

Répond à la contrainte du test : pas besoin de serveur SMTP réel.

Facilement remplaçable par un vrai système (SMTP, SendGrid, Mailjet…)."""