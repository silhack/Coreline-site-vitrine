# Coreline Alliance — Mail API (Backend)

Micro-service **FastAPI** dédié à la gestion du formulaire de contact du site vitrine Coreline Alliance. Il reçoit les soumissions du frontend, les valide, et expédie un e-mail de notification HTML à la boîte professionnelle via SMTP.

---

## Table des Matières

- [Architecture](#architecture)
- [Stack Technique](#stack-technique)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement](#lancement)
- [Endpoints API](#endpoints-api)
- [Sécurité](#sécurité)
- [Template E-mail](#template-e-mail)
- [Mode Simulation (dev)](#mode-simulation-dev)
- [Dépendances](#dépendances)

---

## Architecture

```
server/
├── main.py              # Point d'entrée — app FastAPI, routes, logique métier
├── requirements.txt     # Dépendances Python
├── templates/
│   └── email.html       # Template Jinja2 de l'e-mail de notification
├── .env                 # Variables d'environnement (ignoré par git)
├── .env.example         # Modèle de configuration
└── venv/                # Environnement virtuel Python (ignoré par git)
```

L'application est monolithique et volontairement simple : un seul fichier `main.py` contient l'intégralité de la logique (configuration, validation, envoi SMTP). Ce choix est adapté à un micro-service de messagerie à responsabilité unique.

---

## Stack Technique

| Technologie         | Version | Rôle                                |
| ------------------- | ------- | ----------------------------------- |
| **Python**          | 3.10+   | Langage                             |
| **FastAPI**         | 0.115.0 | Framework web asynchrone            |
| **Uvicorn**         | 0.31.0  | Serveur ASGI                        |
| **Pydantic**        | 2.9.2   | Validation des données d'entrée     |
| **fastapi-mail**    | 1.4.1   | Envoi d'e-mails SMTP avec templates |
| **Jinja2**          | 3.1.4   | Moteur de templates HTML            |
| **SlowAPI**         | 0.1.9   | Rate limiting par IP                |
| **Bleach**          | ≥ 6.0.0 | Assainissement HTML (anti-XSS)      |
| **python-dotenv**   | 1.0.1   | Chargement des variables `.env`     |
| **email-validator** | ≥ 2.0.0 | Validation des adresses e-mail      |

---

## Prérequis

- **Python 3.10** ou supérieur
- **pip** (gestionnaire de paquets Python)
- Un serveur SMTP fonctionnel (Gmail, Outlook, OVH, Hostinger, etc.) — _optionnel en développement, voir [Mode Simulation](#mode-simulation-dev)_

---

## Installation

### 1. Cloner le dépôt et se placer dans le dossier

```bash
cd server
```

### 2. Créer un environnement virtuel

**Linux / macOS :**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows :**

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Configuration

Copier le fichier modèle et le remplir avec vos informations :

```bash
cp .env.example .env
```

### Variables d'environnement

| Variable         | Description                                          | Valeur par défaut       | Obligatoire     |
| ---------------- | ---------------------------------------------------- | ----------------------- | --------------- |
| `ALLOWED_ORIGIN` | Origines CORS autorisées (séparées par des virgules) | `http://localhost:5173` | ✅              |
| `MAIL_USERNAME`  | Adresse e-mail du compte SMTP                        | _(vide)_                | ⚠️ _Non en dev_ |
| `MAIL_PASSWORD`  | Mot de passe d'application SMTP                      | _(vide)_                | ⚠️ _Non en dev_ |
| `MAIL_SERVER`    | Serveur SMTP (ex: `smtp.gmail.com`)                  | _(vide)_                | ⚠️ _Non en dev_ |
| `MAIL_PORT`      | Port SMTP                                            | `587`                   | ❌              |
| `MAIL_FROM`      | Adresse expéditrice affichée                         | `MAIL_USERNAME`         | ❌              |
| `MAIL_TO`        | Adresse destinataire des notifications               | `MAIL_USERNAME`         | ❌              |
| `MAIL_STARTTLS`  | Activer STARTTLS                                     | `True`                  | ❌              |
| `MAIL_SSL_TLS`   | Activer SSL/TLS direct                               | `False`                 | ❌              |
| `ENV`            | Environnement (`production` pour désactiver Swagger) | _(vide)_                | ❌              |

> **💡 Astuce Gmail :** Utilisez un [mot de passe d'application](https://myaccount.google.com/apppasswords) au lieu de votre mot de passe habituel. Activez la validation en 2 étapes au préalable.

### Exemple `.env`

```env
ALLOWED_ORIGIN=http://localhost:5173
MAIL_USERNAME=votre_email@gmail.com
MAIL_PASSWORD=votre_mot_de_passe_application
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_FROM=contact@votre-domaine.com
MAIL_TO=contact@votre-domaine.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

---

## Lancement

### Développement

```bash
# Avec rechargement automatique
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Ou directement via le script :

```bash
python main.py
```

Le serveur démarre sur **http://127.0.0.1:8000**.

### Production

```bash
# Avec Gunicorn (Linux uniquement) — recommandé
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

```bash
# Avec Uvicorn directement
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Documentation interactive

| URL                           | Description                          |
| ----------------------------- | ------------------------------------ |
| `http://localhost:8000/docs`  | Swagger UI (désactivé en production) |
| `http://localhost:8000/redoc` | ReDoc (désactivé en production)      |

---

## Endpoints API

### `GET /`

Vérification du statut du service.

**Réponse :**

```json
{
  "status": "online",
  "service": "Coreline Alliance Mail API",
  "version": "1.0.0"
}
```

---

### `GET /health`

Health check pour les outils de monitoring.

**Réponse :**

```json
{
  "status": "ok"
}
```

---

### `POST /api/contact`

Envoi d'un message de contact. **Limité à 5 requêtes par minute par IP.**

**Corps de la requête (JSON) :**

```json
{
  "name": "Jean Dupont",
  "email": "jean.dupont@entreprise.com",
  "subject": "Demande de partenariat",
  "message": "Bonjour, je souhaite discuter d'un partenariat..."
}
```

| Champ     | Type       | Contraintes                   | Obligatoire |
| --------- | ---------- | ----------------------------- | ----------- |
| `name`    | `string`   | 2 – 100 caractères            | ✅          |
| `email`   | `EmailStr` | Format email valide           | ✅          |
| `subject` | `string`   | Max 150 caractères            | ❌          |
| `message` | `string`   | 10 – 5 000 caractères         | ✅          |
| `website` | `string`   | Max 100 caractères (honeypot) | ❌          |

**Réponse succès (200) :**

```json
{
  "status": "success",
  "message": "Votre message a été envoyé avec succès."
}
```

**Erreurs possibles :**

| Code  | Description                                           |
| ----- | ----------------------------------------------------- |
| `400` | Requête invalide (injection CRLF, validation échouée) |
| `422` | Données non conformes au schéma Pydantic              |
| `429` | Rate limit dépassé (> 5 requêtes/minute)              |
| `500` | Erreur SMTP lors de l'envoi                           |

---

## Sécurité

L'API implémente plusieurs couches de protection :

| Mécanisme               | Description                                                                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **Honeypot**            | Champ `website` invisible côté UI. Si rempli, la requête est silencieusement ignorée (faux `200 OK` renvoyé au bot).         |
| **Rate Limiting**       | 5 requêtes/minute par IP via SlowAPI.                                                                                        |
| **Validation Pydantic** | Typage strict, longueurs min/max sur tous les champs.                                                                        |
| **Anti-CRLF**           | Détection de caractères `\r` et `\n` dans les champs `name`, `email`, `subject` pour empêcher l'injection d'en-têtes e-mail. |
| **Sanitisation HTML**   | Le contenu du message est nettoyé via `bleach.clean()` avant injection dans le template (suppression de toute balise HTML).  |
| **CORS**                | Origines autorisées configurables via `ALLOWED_ORIGIN`.                                                                      |
| **Swagger désactivé**   | En mode `production`, les endpoints `/docs` et `/redoc` sont masqués.                                                        |

---

## Template E-mail

Le template HTML (`templates/email.html`) est un e-mail responsive au design professionnel :

- **Header** bleu marine avec le nom « Coreline Alliance »
- **Carte expéditeur** avec nom, email, sujet (bordure accent dorée)
- **Corps du message** encadré en italique
- **Bouton CTA** « Répondre directement » avec `mailto:` pré-rempli
- **Footer** avec mentions de copyright

Les variables Jinja2 injectées :

| Variable             | Contenu                       |
| -------------------- | ----------------------------- |
| `{{ body.name }}`    | Nom de l'expéditeur           |
| `{{ body.email }}`   | E-mail de l'expéditeur        |
| `{{ body.title }}`   | Sujet du message              |
| `{{ body.message }}` | Contenu du message (sanitisé) |

---

## Mode Simulation (dev)

Si les variables `MAIL_USERNAME` ou `MAIL_SERVER` sont vides, l'API bascule automatiquement en **mode simulation** : les e-mails ne sont pas envoyés mais leur contenu est affiché dans les logs de la console.

```
INFO:     [SIMULATION MAIL] Reçu depuis IP: 127.0.0.1
INFO:     De: jean.dupont@exemple.com
INFO:     Nom: Jean Dupont
INFO:     Sujet: Test
INFO:     Message: Ceci est un test de contact.
```

Cela permet de développer et tester le frontend sans avoir de serveur SMTP configuré.

---

## Dépendances

Contenu de `requirements.txt` :

```
fastapi==0.115.0
uvicorn[standard]==0.31.0
fastapi-mail==1.4.1
python-dotenv==1.0.1
pydantic==2.9.2
pydantic-settings==2.5.2
Jinja2==3.1.4
slowapi==0.1.9
email-validator>=2.0.0
bleach>=6.0.0
```

---

## Support

Pour toute question technique, contactez l'équipe de développement **Coreline Alliance**.
