from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.actualites import Actualite, Source
from app.schemas.actualites import ActualiteCreate, ActualiteUpdate
from app.utils.utils_actualites import save_image, delete_image_file
from fastapi import HTTPException, UploadFile

def get_or_create_sources(db: Session, sources_noms: list[str]):
    """
    Récupère les sources existantes par leur nom ou les crée si elles n'existent pas.
    Utile pour la relation Many-to-Many entre Actualités et Sources.
    """
    sources = []
    for nom in sources_noms:
        source = db.execute(select(Source).where(Source.nom == nom)).scalar_one_or_none()
        if not source:
            source = Source(nom=nom)
            db.add(source)
            db.commit()
            db.refresh(source)
        sources.append(source)
    return sources

def create_actualites(db: Session, actualite_data: ActualiteCreate, image: UploadFile = None):
    """
    Crée une nouvelle actualité avec ses sources et son image.
    """
    image_url = save_image(image) if image else None
    sources_objs = get_or_create_sources(db, actualite_data.sources)
    
    db_actualite = Actualite(
        titre=actualite_data.titre,
        description=actualite_data.description,
        categorie=actualite_data.categorie,
        image=image_url,
        sources=sources_objs
    )
    db.add(db_actualite)
    db.commit()
    db.refresh(db_actualite)
    return db_actualite

def get_all_actualites(db: Session):
    """
    Récupère toutes les actualités triées par défaut (ordre d'insertion).
    """
    return db.execute(select(Actualite)).scalars().all()

def get_actualite(db: Session, id_actualites: uuid.UUID):
    """
    Récupère une seule actualité par son ID.
    Lève 404 si l'actualité est introuvable.
    """
    actualite = db.get(Actualite, id_actualites)
    if not actualite:
        raise HTTPException(status_code=404, detail="Actualité non trouvée")
    return actualite

def update_actualites(
    db: Session,
    id_actualites: uuid.UUID,
    actualite_update: ActualiteUpdate,
    image: UploadFile = None
):
    """
    Met à jour une actualité. Gère les sources et le remplacement d'images.
    """
    db_actualite = get_actualite(db, id_actualites)

    if actualite_update.titre:
        db_actualite.titre = actualite_update.titre
    if actualite_update.description:
        db_actualite.description = actualite_update.description
    if actualite_update.categorie:
        db_actualite.categorie = actualite_update.categorie

    if image:
        if db_actualite.image:
            delete_image_file(db_actualite.image)
        db_actualite.image = save_image(image)

    if actualite_update.sources is not None:
        db_actualite.sources = get_or_create_sources(db, actualite_update.sources)

    db.add(db_actualite)
    db.commit()
    db.refresh(db_actualite)
    return db_actualite

def delete_actualite(db: Session, id_actualites: uuid.UUID):
    """
    Supprime une actualité et nettoie le fichier image du serveur.
    """
    db_actualite = get_actualite(db, id_actualites)
    if db_actualite.image:
        delete_image_file(db_actualite.image)
    db.delete(db_actualite)
    db.commit()
    return {"message": f"Actualité '{db_actualite.titre}' supprimée"}

def delete_all_actualites(db: Session):
    """
    Supprime toutes les actualités et tous les fichiers images associés.
    """
    actualites = get_all_actualites(db)
    for actualite in actualites:
        if actualite.image:
            delete_image_file(actualite.image)
        db.delete(actualite)
    db.commit()
    return {"message": "Tous les articles ont été supprimés"}
