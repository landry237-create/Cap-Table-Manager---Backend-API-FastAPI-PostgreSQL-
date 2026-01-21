# Cap-Table-Manager---Backend-API-FastAPI-PostgreSQL-
Ce projet simule une plateforme d’administration du tableau de capitalisation d’entreprise, permettant à un administrateur de : - gérer les actionnaires, - émettre des actions, - générer des certificats PDF, - consulter les journaux d’audit.  Les actionnaires peuvent consulter leurs actions et télécharger leurs certificats.
je vous invite vite vivement à lire le fichier README.ipynb pour avoir la description détaillé du projet


# 🏢 Cap Table Manager – Backend API (FastAPI + PostgreSQL)

Ce projet simule une plateforme d’administration du tableau de capitalisation d’entreprise, permettant à un administrateur de :
- gérer les actionnaires,
- émettre des actions,
- générer des certificats PDF,
- consulter les journaux d’audit.

Les actionnaires peuvent consulter leurs actions et télécharger leurs certificats.

---

## ⚙️ Technologies utilisées

- ✅ Python 3.10+
- ✅ FastAPI (API REST)
- ✅ PostgreSQL (base de données)
- ✅ SQLAlchemy (ORM)
- ✅ JWT (authentification)
- ✅ ReportLab (génération PDF)
- ✅ Pytest (tests)

---

## 🛠️ Installation locale

### 1. Cloner le projet

```bash
git clone https://github.com/votre-user/cap-table-backend.git
cd cap-table-backend
```
### 2 Créer un environement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```
### 3 installer les dependances

``` bash
pip install -r requirements.txt
```

### 4 Configurer la base de données PostgreSQL
##### Assure-toi d’avoir PostgreSQL installé localement. Puis crée une base de données :

```sql
CREATE DATABASE cap_table;
```

### 5 Ajouter un fichier .env (optionnel mais recommandé)
##### Crée un fichier .env à la racine :

```ini
DATABASE_URL=postgresql://postgres:motdepasse@localhost/cap_table
SECRET_KEY=votre_cle_secrete
```

⚠️ Remplace motdepasse par celui de ton compte PostgreSQL.

### ▶️ Lancer l’API

uvicorn app.main:app --reload

L’API sera disponible à :
📍 http://localhost:8000
📄 Documentation Swagger : http://localhost:8000/docs



### 👥 Utilisateurs de test (codés en dur)
on peut les créer via /api/shareholders/ ou en base manuellement

| Rôle        | Email                                         | Mot de passe |
| ----------- | --------------------------------------------- | ------------ |
| Admin       | [admin@example.com](mailto:admin@example.com) | admin123     |
| Actionnaire | [user@example.com](mailto:user@example.com)   | user123      |


### 🔐 Authentification via JWT
##### 1 Envoie une requête POST à :

POST /api/token/
Content-Type: application/x-www-form-urlencoded

username=admin@example.com
password=admin123

##### 2 réponse

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "token_type": "bearer"
}
```
##### 3 utilise le token dans l'en-tête Authorisation
``` makefile
Authorization: Bearer <votre_token>
```

### 🧪 Lancer les tests

pytest tests/

### 📦 Endpoints principaux

| Méthode | Endpoint                           | Rôle  | Description                               |
| ------- | ---------------------------------- | ----- | ----------------------------------------- |
| POST    | `/api/token/`                      | Tous  | Connexion et génération de JWT            |
| GET     | `/api/shareholders/`               | Admin | Liste des actionnaires + nombre d’actions |
| POST    | `/api/shareholders/`               | Admin | Créer un nouvel actionnaire               |
| GET     | `/api/issuances/`                  | Tous  | Liste des émissions (perso ou toutes)     |
| POST    | `/api/issuances/`                  | Admin | Émettre des actions à un actionnaire      |
| GET     | `/api/issuances/{id}/certificate/` | Tous  | Télécharger le certificat PDF             |


### 🧩 Bonus implémentés
✅ Journalisation (audit)
✅ Validation anti-nombre négatif
✅ Simulation d’e-mail (console)
✅ Filigrane sur PDF

### 📌 À faire (Frontend / extensions)
Intégrer avec un frontend React.js utilisant Material Design.

Ajouter une interface graphique d'administration.

Envoyer les vrais emails (ex : SendGrid, Mailjet).

Gérer les erreurs avec des statuts HTTP + messages clairs.


### 🤝 Contribuer
vous pouvez améliorer ce backend ou créer votre propre frontend compatible.
N’hésitez pas à collaborer ou a proposer des améliorations pour le projet !

### 🧑‍💻 Auteur

##### Noumbissi Ange Landry
###### Landrynoumbissi23@gmail.com


Ce backend a été conçu comme solution technique à un test simulé d’entreprise SaaS de type « Corporate OS ».

