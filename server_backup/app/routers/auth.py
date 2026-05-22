import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import security
from app.crud.admins import (
    delete_all_admins, 
    get_admin_by_id, 
    get_admin_by_name, 
    create_admin, 
    delete_admin, 
    get_all_admins, 
    update_admin
)
from app.schemas.admin import AdminCreate, AdminPublic, AdminUpdate, LoginRequest, Token
from app.dependencies import get_current_admin


router = APIRouter(
  tags=["admins"],
  prefix="/admins"
)

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Point d'entrée pour la connexion des administrateurs.
    Retourne un token JWT si les identifiants sont valides.
    """
    admin = get_admin_by_name(db, data.nom)
    if not admin or not security.verify_password(data.password, admin.password): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Nom d'utilisateur ou mot de passe invalide"
        )
    
    access_token = security.create_access_token(data={"sub": admin.nom})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AdminPublic)
def route_create_admin(
    admin_data: AdminCreate, 
    db: Session = Depends(get_db),
    current_admin: AdminPublic = Depends(get_current_admin)
):
    """
    Crée un nouvel administrateur (Nécessite d'être déjà connecté en tant qu'admin).
    """
    existing = get_admin_by_name(db, admin_data.nom)
    if existing:
        raise HTTPException(status_code=400, detail="Un admin avec ce nom existe déjà")
    return create_admin(db, admin_data)

@router.get("/me", response_model=AdminPublic)
def read_current_admin(current_admin: AdminPublic = Depends(get_current_admin)):
    """
    Récupère les informations de l'administrateur connecté.
    """
    return current_admin

@router.get("/{admin_id}", response_model=AdminPublic)
def route_get_admin(
    admin_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_admin: AdminPublic = Depends(get_current_admin)
):
    """
    Récupère un administrateur par son ID (Accès restreint).
    """
    admin = get_admin_by_id(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin non trouvé")
    return admin

@router.get("/", response_model=list[AdminPublic])
def route_get_admins(
    db: Session = Depends(get_db),
    current_admin: AdminPublic = Depends(get_current_admin)
):
    """
    Liste tous les administrateurs (Accès restreint).
    """
    return get_all_admins(db)

@router.patch("/{admin_id}", response_model=AdminPublic)
def route_update_admin(
    admin_id: uuid.UUID, 
    update_data: AdminUpdate, 
    db: Session = Depends(get_db),
    current_admin: AdminPublic = Depends(get_current_admin)
):
    """
    Met à jour les informations d'un administrateur (Accès restreint).
    """
    return update_admin(admin_id, update_data, db)

@router.delete("/{admin_id}")
def route_delete_admin(
    admin_id: uuid.UUID, 
    db: Session = Depends(get_db),
    current_admin: AdminPublic = Depends(get_current_admin)
):
    """
    Supprime un administrateur (Accès restreint).
    """
    return delete_admin(db, admin_id)