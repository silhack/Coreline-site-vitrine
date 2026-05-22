from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from contextlib import asynccontextmanager
from app.routers import actualites, produits, contacts, auth
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de cycle de vie de l'application.
    Les actions ici sont exécutées au démarrage et à la fermeture.
    Note : Les tables sont créées via Alembic en production, 
    mais ceci assure qu'elles existent en local.
    """
    # Base.metadata.create_all(bind=engine) # Optionnel si on utilise exclusivement Alembic
    yield

# Initialisation de l'application FastAPI
app = FastAPI(
    title="API AKIBA SOLUTION",
    description="API pour le site vitrine et le panneau d'administration d'Akiba Solution",
    version="1.0.0",
    lifespan=lifespan
)

BASE_DIR = Path(__file__).resolve().parent

# Configuration CORS (Cross-Origin Resource Sharing)
# Permet au frontend React de communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origines autorisées (Frontend Vite)
    allow_credentials=True,
    allow_methods=["*"],                      # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],                      # Autorise tous les headers
)

# Montage du dossier statique pour servir les images uploadées
app.mount("/app/static", StaticFiles(directory=BASE_DIR / "app/static"), name="static")

# Inclusion des différents routeurs de l'application
app.include_router(actualites.router)
app.include_router(contacts.router)
app.include_router(produits.router)
app.include_router(auth.router)

# Point d'entrée de base pour vérifier si l'API fonctionne
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenue: l'API AKIBA est opérationnelle 🚀"}

if __name__ == "__main__":
    # Lancement du serveur uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
