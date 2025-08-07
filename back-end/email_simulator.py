# email_simulator.py

# Simule un envoi d’e-mail en l’affichant dans la console
def send_email(subject: str, recipient: str):
    print(f"\n[📧 EMAIL SIMULÉ]")
    print(f"À : {recipient}")
    print(f"Sujet : {subject}")
    print("Contenu : Cet email est une simulation de notification.")
    print("-" * 50)

"""
🔍 Pourquoi simuler ?

Répond à la contrainte du test : pas besoin de serveur SMTP réel.

Facilement remplaçable par un vrai système (SMTP, SendGrid, Mailjet…).
"""
