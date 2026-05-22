import uuid
import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.contacts import create_contact, get_all_contacts, get_contact, update_contact, delete_contact, delete_all_contacts, send_mail
from app.database import get_db
from app.schemas.contacts import ContactCreate, ContactPublic, ContactUpdate, ContactMailRequest
from app.dependencies import get_current_admin
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

# Configuration mail légère (sans BDD)
_mail_conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME', ''),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD', ''),
    MAIL_FROM=os.getenv('MAIL_FROM', os.getenv('MAIL_USERNAME', '')),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_SERVER=os.getenv('MAIL_SERVER', ''),
    MAIL_STARTTLS=os.getenv('MAIL_STARTTLS', 'True').lower() == 'true',
    MAIL_SSL_TLS=os.getenv('MAIL_SSL_TLS', 'False').lower() == 'true',
    USE_CREDENTIALS=True if os.getenv('MAIL_PASSWORD') else False,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).resolve().parent.parent / "templates"
)

# Router pour la gestion des demandes de contact
router = APIRouter(
  tags=["contacts"],
  prefix="/contacts"
)

# POST - Public (Formulaire de contact)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ContactPublic)
def route_create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle demande de contact dans la base de données.
    """
    return create_contact(db, contact)

@router.post("/mail", status_code=status.HTTP_200_OK, response_model=dict)
async def route_send_mail(contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Enregistre la demande et envoie un e-mail de notification.
    """
    return await send_mail(db, contact)

# POST - Public (Envoi email SANS base de données)
@router.post("/send", status_code=status.HTTP_200_OK)
async def route_send_contact_email(contact: ContactMailRequest):
    """
    Reçoit le formulaire de contact et envoie un e-mail de notification.
    Ne nécessite PAS de base de données.
    """
    try:
        template_body = {
            "title": contact.subject or "Nouveau message de contact",
            "name": contact.name,
            "email": contact.email,
            "message": contact.message
        }

        message = MessageSchema(
            subject=f"Contact Coreline Alliance - {contact.subject or 'Nouveau message'}",
            recipients=[os.getenv('MAIL_USERNAME', '')],
            reply_to=[contact.email],
            template_body={"body": template_body},
            subtype=MessageType.html
        )

        fm = FastMail(_mail_conf)
        await fm.send_message(message, template_name="email.html")

        return {"message": "Votre message a été envoyé avec succès."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'envoi de l'email: {str(e)}"
        )

# GET - Protégé (Admin uniquement)
@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ContactPublic])
def route_get_contacts(
    db: Session = Depends(get_db), 
    current_admin=Depends(get_current_admin)
):
    """
    Récupère la liste de tous les messages de contact (Admin uniquement).
    """
    return get_all_contacts(db)

@router.get("/{id_contact}", status_code=status.HTTP_200_OK, response_model=ContactPublic)
def route_get_contact(
    id_contact: uuid.UUID, 
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Récupère un message de contact spécifique par son ID (Admin uniquement).
    """
    return get_contact(db, id_contact)

@router.patch("/{id_contact}", status_code=status.HTTP_202_ACCEPTED, response_model=ContactPublic)
def route_update_contact(
    contact: ContactUpdate, 
    id_contact: uuid.UUID, 
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Met à jour un message de contact (Admin uniquement).
    """
    return update_contact(db, id_contact, contact)

@router.delete("/{id_contact}", status_code=status.HTTP_200_OK)
def route_delete_contact(
    id_contact: uuid.UUID, 
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Supprime un message de contact (Admin uniquement).
    """
    return delete_contact(db, id_contact)

@router.delete("/", status_code=status.HTTP_200_OK)
def route_delete_contacts(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """
    Supprime TOUS les messages de contact (Admin uniquement).
    """
    return delete_all_contacts(db)
