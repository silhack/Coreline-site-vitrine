import uuid
from typing import Optional
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session
from app.crud.produits import (
    create_produit,
    delete_produit,
    get_produit,
    get_all_produits,
    update_produit,
    delete_all_produits
)
from app.database import get_db
from app.schemas.produits import ProduitCreate, ProduitPublic, ProduitUpdate
from app.dependencies import get_current_admin

# Router pour la gestion des produits
router = APIRouter(tags=["produits"], prefix="/produits")

@router.post("/", response_model=ProduitPublic, status_code=status.HTTP_201_CREATED)
def route_create_produit(
    nom: str = Form(...),
    description: str = Form(...),
    accroche: str = Form(...),
    avantages: list[str] = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Crée un nouveau produit (Accès admin uniquement).
    L'image et les données sont envoyées via un formulaire multipart.
    """
    produits_data = ProduitCreate(
        nom=nom,
        description=description,
        accroche=accroche,
        avantages=avantages
    )
    return create_produit(db, produits_data, image)

@router.get("/", response_model=list[ProduitPublic], status_code=status.HTTP_200_OK)
def route_get_produits(db: Session = Depends(get_db)):
    """
    Récupère la liste de tous les produits (Accès public).
    """
    return get_all_produits(db)

@router.get("/{id_produit}", response_model=ProduitPublic, status_code=status.HTTP_200_OK)
def route_get_produit(id_produit: uuid.UUID, db: Session = Depends(get_db)):
    """
    Récupère un produit spécifique par son ID (Accès public).
    """
    return get_produit(db, id_produit)

@router.patch("/{id_produit}", response_model=ProduitPublic, status_code=status.HTTP_200_OK)
def route_update_produit(
    id_produit: uuid.UUID,
    nom: str | None = Form(None),
    description: str | None = Form(None),
    accroche: str | None = Form(None),
    avantages: list[str] | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Met à jour un produit existant (Accès admin uniquement).
    """
    update_data = ProduitUpdate(
        nom=nom,
        description=description,
        accroche=accroche,
        avantages=avantages
    )
    return update_produit(db, id_produit, update_data, image)

@router.delete("/{id_produit}", status_code=status.HTTP_200_OK)
def route_delete_produit(
    id_produit: uuid.UUID, 
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Supprime un produit et son image associée (Accès admin uniquement).
    """
    return delete_produit(db, id_produit)

@router.delete("/", status_code=status.HTTP_200_OK)
def route_delete_produits(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Supprime TOUS les produits (Accès admin uniquement).
    """
    return delete_all_produits(db)