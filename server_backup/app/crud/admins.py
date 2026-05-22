from datetime import datetime, timezone
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.security import hash_password

def get_admin_by_name(db: Session, nom: str):
    """
    Récupère un administrateur par son nom d'utilisateur.
    """
    return db.execute(select(Admin).where(Admin.nom == nom)).scalar_one_or_none()

def get_admin_by_email(db: Session, email: str):
    """
    Récupère un administrateur par son adresse e-mail.
    """
    return db.execute(select(Admin).where(Admin.email == email)).scalar_one_or_none()

def get_admin_by_id(db: Session, admin_id: uuid.UUID):
    """
    Récupère un administrateur par son ID unique (UUID).
    """
    return db.get(Admin, admin_id)

def create_admin(db: Session, admin_data: AdminCreate):
    """
    Crée un nouvel administrateur avec un mot de passe haché.
    """
    hashed = hash_password(admin_data.password)
    db_admin = Admin(
        nom=admin_data.nom, 
        email=admin_data.email, # Ajout de l'email
        password=hashed
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin 

def get_all_admins(db: Session): 
    """
    Récupère la liste de tous les administrateurs.
    """
    return db.execute(select(Admin)).scalars().all()

def update_admin(admin_id: uuid.UUID, admin_update: AdminUpdate, db: Session):
    """
    Met à jour les informations d'un administrateur (nom, email et/ou mot de passe).
    """
    db_admin = get_admin_by_id(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin inexistant")

    if admin_update.nom:
        db_admin.nom = admin_update.nom
    if admin_update.email:
        db_admin.email = admin_update.email
    if admin_update.password:
        db_admin.password = hash_password(admin_update.password)

    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def delete_admin(db: Session, admin_id: uuid.UUID):
    """
    Supprime un administrateur de la base de données.
    """
    db_admin = get_admin_by_id(db, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin inexistant")
    db.delete(db_admin)
    db.commit()
    return {"Message": f"Admin {db_admin.nom} supprimé avec succès"}

def delete_all_admins(db: Session):
    """
    Supprime TOUS les administrateurs (Action dangereuse).
    """
    db.execute(delete(Admin))
    db.commit()
    return {"message": "Tous les admins ont été supprimés"}