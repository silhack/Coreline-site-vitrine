import uuid
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session
from app.crud.actualites import (
    create_actualites,
    delete_actualite,
    get_actualite,
    get_all_actualites,
    update_actualites,
    delete_all_actualites
)
from app.database import get_db
from app.schemas.actualites import ActualiteCreate, ActualitePublic, ActualiteUpdate, Categorie
from app.dependencies import get_current_admin

# Router pour la gestion des actualités (articles de blog, nouvelles, etc.)
router = APIRouter(tags=["actualites"], prefix="/actualites")

@router.post("/", response_model=ActualitePublic, status_code=status.HTTP_201_CREATED)
def route_create_actualites(
    titre: str = Form(...),
    description: str = Form(...),
    sources: list[str] = Form([]),
    categorie: Categorie = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Crée une nouvelle actualité (Accès admin uniquement).
    Supporte l'upload d'image et une liste de sources.
    """
    actualites_data = ActualiteCreate(titre=titre, description=description, sources=sources, categorie=categorie)
    return create_actualites(db, actualites_data, image)

@router.get("/", response_model=list[ActualitePublic], status_code=status.HTTP_200_OK)
def route_get_actualites(db: Session = Depends(get_db)):
    """
    Récupère la liste de toutes les actualités (Accès public).
    """
    return get_all_actualites(db)

@router.get("/{id_actualites}", response_model=ActualitePublic, status_code=status.HTTP_200_OK)
def route_get_actualite(id_actualites: uuid.UUID, db: Session = Depends(get_db)):
    """
    Récupère une actualité spécifique par son ID (Accès public).
    """
    return get_actualite(db, id_actualites)

@router.patch("/{id_actualites}", response_model=ActualitePublic, status_code=status.HTTP_200_OK)
def route_update_actualites(
    id_actualites: uuid.UUID,
    titre: str | None = Form(None),
    description: str | None = Form(None),
    sources: list[str] | None = Form(None),
    categorie: Categorie | None = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Met à jour une actualité existante (Accès admin uniquement).
    Gère la mise à jour partielle des champs et le remplacement d'image.
    """
    update_data = ActualiteUpdate(
        titre=titre,
        description=description,
        sources=sources,
        categorie=categorie
    )
    return update_actualites(db, id_actualites, update_data, image)

@router.delete("/{id_actualites}", status_code=status.HTTP_200_OK)
def route_delete_actualite(
    id_actualites: uuid.UUID, 
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Supprime une actualité (Accès admin uniquement).
    """
    return delete_actualite(db, id_actualites)

@router.delete("/", status_code=status.HTTP_200_OK)
def route_delete_actualites(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Supprime TOUTES les actualités (Accès admin uniquement).
    """
    return delete_all_actualites(db)