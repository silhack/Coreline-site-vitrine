# AKIBA API - Actualités, Produits & Contact Form

Ce projet est un serveur backend FastAPI pour gérer les actualités, les produits et les formulaires de contact d’un site vitrine. Il utilise PostgreSQL pour la base de données et SQLModel pour l'ORM.

## Structure du projet

```
app/
├── crud/
├── models/
├── routers/
├── database.py
├── main.py
.env
requirements.txt
README.md
```


## Prérequis

- **Python 3.10+**
- **PostgreSQL** installé et en cours d'exécution
- **Git** (facultatif mais recommandé)


## Installation (Environnement virtuel)

### Sous **Linux/macOS** :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Sous **Windows** :

```cmd
python -m venv .venv
.venv\Scripts\activate
```


## Installation des dépendances

```bash
pip install -r requirements.txt
```


## Configuration de l'environnement

Crée un fichier `.env` à la racine du projet et configure les variables nécessaires, consulte le [.env.example](./.env.example) pour plus d'infos concernant les variables nécessaires


## Initialiser la base de données

```bash
 alembic revision --autogenerate -m "<message>"
```
```bash
 alembic upgrade head
```

> Assurez-vous d'avoir configuré `alembic.ini` et `env.py` correctement.


## Lancer le serveur FastAPI

```bash
uvicorn app.main:app --reload
```


## Accès à la documentation

Une fois le serveur lancé, accédez à la documentation automatique :

- Swagger UI : [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc : [http://localhost:8000/redoc](http://localhost:8000/redoc)


## Export des dépendances (optionnel)

```bash
pip freeze > requirements.txt
```


## Notes

- Le code suit l’architecture **CRUD + Router + Models** avec `SQLModel`.


## À faire

- [ ] Ajout de tests avec `pytest`
- [ ] Dockerisation du projet


## Auteur

Projet développé par **Akiba Solution — [www.akibasolution.com](http://www.akibasolution.com)**.


list des command pour la base de donnée

- create database akiba_db
- create user postgres with encrypted password 'password'
- create database akiba_db owner postgres;
- grant all privileges on database akiba_db to postgres
- ALTER SCHEMA public owner to postgres;
- GRANT USAGE, CREATE ON SCHEMA public TO postgres;
