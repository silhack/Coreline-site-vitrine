# Coreline Alliance

Plateforme complète pour le site vitrine de **Coreline Alliance**, une alliance internationale d'experts spécialisée dans l'accélération du développement de projets durables et l'investissement institutionnel en Afrique.

Ce monorepo contient le **frontend React** (site vitrine public) et le **backend FastAPI** (micro-service de messagerie).

---

## Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture du Monorepo](#architecture-du-monorepo)
- [Stack Technique](#stack-technique)
- [Prérequis Globaux](#prérequis-globaux)
- [Démarrage Rapide](#démarrage-rapide)
- [Structure des Dossiers](#structure-des-dossiers)
- [Environnements](#environnements)
- [Contribution](#contribution)
- [Support](#support)

---

## Vue d'ensemble

| Module                          | Technologie                  | Description                                                                             |
| ------------------------------- | ---------------------------- | --------------------------------------------------------------------------------------- |
| **`client/`**                   | React 19 + Vite 6            | Site vitrine public avec formulaire de contact, pages services, actualités, SEO complet |
| **`server/`**                   | FastAPI + Uvicorn            | Micro-service d'envoi d'e-mails (formulaire de contact → SMTP)                          |
| **`[DÉPRÉCIÉ] sql/`**           | PostgreSQL 17                | Dump de l'ancienne base de données                                                      |
| **`[DÉPRÉCIÉ] server_backup/`** | FastAPI + SQLModel + Alembic | Ancien backend complet de secours (API CRUD)                                            |

> **⚠️ Note Importante :** Les dossiers `sql/` et `server_backup/` sont **dépréciés** et désactivés. Ils étaient utilisés lorsqu'on s'appelait encore "Akiba Solution" et qu'on présentait des produits, actualités, etc. Actuellement, **le seul service backend actif est `server/`** qui gère uniquement la messagerie.

### Flux de communication

```
┌──────────────┐     POST /api/contact     ┌──────────────┐     SMTP      ┌──────────┐
│              │  ───────────────────────►  │              │  ──────────►  │          │
│   Frontend   │                           │   Backend    │               │  Boîte   │
│   (React)    │  ◄───────────────────────  │  (FastAPI)   │               │   Mail   │
│   :5173      │     JSON Response         │   :8000      │               │          │
└──────────────┘                           └──────────────┘               └──────────┘
```

---

## Architecture du Monorepo

```
Coreline-site-vitrine/
├── client/                  # 🖥️  Frontend React (site vitrine)
│   ├── public/              #     Assets statiques, sitemap, robots.txt
│   ├── src/                 #     Code source React
│   │   ├── components/      #     Composants réutilisables
│   │   ├── pages/           #     Pages de l'application
│   │   ├── App.jsx          #     Routeur principal
│   │   ├── main.jsx         #     Point d'entrée React
│   │   └── coreline.css     #     Feuille de styles globale
│   ├── .env.example         #     Modèle de configuration
│   ├── package.json         #     Dépendances Node.js
│   └── vite.config.js       #     Configuration Vite
│
├── server/                  # ⚙️  Backend FastAPI (micro-service mail)
│   ├── main.py              #     Application FastAPI
│   ├── templates/
│   │   └── email.html       #     Template HTML de l'e-mail
│   ├── .env.example         #     Modèle de configuration SMTP
│   └── requirements.txt     #     Dépendances Python
│
├── [DÉPRÉCIÉ] sql/          # 🗄️  Ancienne base de données
│   └── akibadb.sql          #     Dump PostgreSQL
│
├── [DÉPRÉCIÉ] server_backup/ # 📦  Ancien backend (désactivé)
│   ├── app/                 #     Code applicatif (models, routers, crud)
│   ├── alembic/             #     Migrations de base de données
│   └── ...
│
└── .gitignore               # Règles d'exclusion Git
```

---

## Stack Technique

### Frontend

| Technologie        | Version | Rôle                 |
| ------------------ | ------- | -------------------- |
| React              | 19.0.0  | Bibliothèque UI      |
| Vite               | 6.2.0   | Bundler / dev server |
| React Router       | 7.14.1  | Navigation SPA       |
| Framer Motion      | 12.6.2  | Animations           |
| Lucide React       | 1.8.0   | Icônes               |
| React Helmet Async | 3.0.0   | SEO dynamique        |
| Vanilla CSS        | —       | Styling              |

### Backend

| Technologie  | Version | Rôle              |
| ------------ | ------- | ----------------- |
| Python       | 3.10+   | Langage           |
| FastAPI      | 0.115.0 | Framework API     |
| Uvicorn      | 0.31.0  | Serveur ASGI      |
| fastapi-mail | 1.4.1   | Envoi SMTP        |
| Pydantic     | 2.9.2   | Validation        |
| SlowAPI      | 0.1.9   | Rate limiting     |
| Bleach       | ≥ 6.0.0 | Sanitisation HTML |

---

## Prérequis Globaux

| Outil       | Version minimale |
| ----------- | ---------------- |
| **Node.js** | 18+              |
| **npm**     | 9+               |
| **Python**  | 3.10+            |
| **pip**     | Dernière version |

---

## Démarrage Rapide

### 1. Cloner le dépôt

```bash
git clone <repository-url>
cd Coreline-site-vitrine
```

### 2. Démarrer le backend (serveur mail)

```bash
cd server

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Linux/macOS :
source venv/bin/activate
# Windows :
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos informations SMTP (optionnel en dev)

# Lancer le serveur
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

> **💡** Sans configuration SMTP, le backend fonctionne en **mode simulation** : les e-mails sont affichés dans la console.

### 3. Démarrer le frontend

```bash
cd client

# Installer les dépendances
npm install

# Configurer l'environnement
cp .env.example .env
# Éditer .env si nécessaire

# Lancer le serveur de développement
npm run dev
```

### 4. Ouvrir dans le navigateur

| Service                | URL                        |
| ---------------------- | -------------------------- |
| **Site vitrine**       | http://localhost:5173      |
| **API Backend**        | http://localhost:8000      |
| **Swagger (API docs)** | http://localhost:8000/docs |

---

## Environnements

### Fichiers de configuration

| Fichier       | Localisation | Description                |
| ------------- | ------------ | -------------------------- |
| `client/.env` | Frontend     | URL de l'API, ID Formspree |
| `server/.env` | Backend      | Configuration SMTP, CORS   |

### Mode développement vs production

| Aspect           | Développement              | Production                           |
| ---------------- | -------------------------- | ------------------------------------ |
| **Frontend**     | `npm run dev` (HMR activé) | `npm run build` → fichiers statiques |
| **Backend**      | `uvicorn --reload`         | `gunicorn` avec workers Uvicorn      |
| **Swagger**      | Activé (`/docs`, `/redoc`) | Désactivé (`ENV=production`)         |
| **Console logs** | Conservés                  | Supprimés automatiquement (esbuild)  |
| **SMTP**         | Mode simulation (console)  | Envoi réel via serveur SMTP          |

---

## Contribution

1. **Fork** du projet
2. Créer une **branche feature** : `git checkout -b feature/nouvelle-fonctionnalite`
3. **Commit** : `git commit -m 'Ajout nouvelle fonctionnalité'`
4. **Push** : `git push origin feature/nouvelle-fonctionnalite`
5. Ouvrir une **Pull Request**

### Conventions

- **Commits** : Messages en français, descriptifs et concis
- **Branches** : `feature/`, `fix/`, `chore/` suivi d'un nom descriptif
- **Code** : Respecter le linting ESLint (frontend) et les conventions PEP 8 (backend)

---

## Support

Projet développé par **Coreline Alliance** — [www.corelinealliance.com](http://www.corelinealliance.com)

Pour toute question ou assistance technique, contactez l'équipe de développement.
