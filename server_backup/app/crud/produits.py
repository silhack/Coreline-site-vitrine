from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.produits import Produit
from app.schemas.produits import ProduitCreate, ProduitUpdate
from app.utils.utils_produits import save_image, delete_image_file
from fastapi import HTTPException, UploadFile

def create_produit(db: Session, produit_data: ProduitCreate, image: UploadFile = None):
    """
    Crée un produit dans la base de données.
    Sauvegarde l'image si elle est fournie.
    """
    image_url = save_image(image) if image else None
    db_produit = Produit(
        nom=produit_data.nom,
        description=produit_data.description,
        accroche=produit_data.accroche,
        avantages=produit_data.avantages,
        image=image_url
    )
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit

def get_all_produits(db: Session):
    """
    Récupère tous les produits.
    """
    return db.execute(select(Produit)).scalars().all()

def get_produit(db: Session, id_produit: uuid.UUID):
    """
    Récupère un produit par son ID unique.
    Lève une erreur 404 s'il n'existe pas.
    """
    produit = db.get(Produit, id_produit)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit

def update_produit(
    db: Session,
    id_produit: uuid.UUID,
    produit_update: ProduitUpdate,
    image: UploadFile = None
):
    """
    Met à jour les informations d'un produit. 
    Gère le remplacement de l'image (suppression de l'ancienne).
    """
    db_produit = get_produit(db, id_produit) 

    if produit_update.nom:
        db_produit.nom = produit_update.nom
    if produit_update.description:
        db_produit.description = produit_update.description
    if produit_update.accroche:
        db_produit.accroche = produit_update.accroche
    if produit_update.avantages is not None:
        db_produit.avantages = produit_update.avantages

    if image:
        if db_produit.image:
            delete_image_file(db_produit.image)
        db_produit.image = save_image(image)

    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit

def delete_produit(db: Session, id_produit: uuid.UUID):
    """
    Supprime un produit et son image du disque.
    """
    db_produit = get_produit(db, id_produit)
    if db_produit.image:
        delete_image_file(db_produit.image)
    db.delete(db_produit)
    db.commit()
    return {"message": f"Produit '{db_produit.nom}' supprimé"}

def delete_all_produits(db: Session):
    """
    Supprime tous les produits et toutes les images associées.
    """
    produits = get_all_produits(db)
    for produit in produits:
        if produit.image:
            delete_image_file(produit.image)
        db.delete(produit)
    db.commit()
    return {"message": "Tous les produits ont été supprimés"}
