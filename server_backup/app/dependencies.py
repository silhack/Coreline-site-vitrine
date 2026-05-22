from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import SECRET_KEY, ALGORITHM
from app.models.admin import Admin
from app.schemas.admin import TokenData
from sqlalchemy import select

# Schéma d'authentification OAuth2 (le token est envoyé dans le header Authorization)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admins/login")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dépendance pour récupérer l'administrateur actuel à partir du token JWT.
    Lève une exception 401 si le token est invalide ou expiré.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Pourrait ne pas valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Décodage du token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nom: str = payload.get("sub")
        if nom is None:
            raise credentials_exception
        token_data = TokenData(nom=nom)
    except JWTError:
        raise credentials_exception
    
    # Recherche de l'admin dans la base de données
    admin = db.execute(select(Admin).where(Admin.nom == token_data.nom)).scalar_one_or_none()
    if admin is None:
        raise credentials_exception
    
    return admin
