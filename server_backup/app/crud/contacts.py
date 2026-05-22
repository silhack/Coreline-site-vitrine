import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.contacts import Contact
from app.schemas.contacts import ContactCreate, ContactUpdate
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

class Envs: 
    """Chargement des configurations e-mail depuis l'environnement."""
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_STARTTLS = os.getenv('MAIL_STARTTLS', 'True').lower() == 'true'
    MAIL_SSL_TLS = os.getenv('MAIL_SSL_TLS', 'False').lower() == 'true'

# Configuration pour fastapi-mail
conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM or Envs.MAIL_USERNAME,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_STARTTLS=Envs.MAIL_STARTTLS,
    MAIL_SSL_TLS=Envs.MAIL_SSL_TLS,
    USE_CREDENTIALS=True if Envs.MAIL_PASSWORD else False,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).resolve().parent.parent / "templates"
)

def create_contact(db: Session, contact_data: ContactCreate): 
    """
    Enregistre une nouvelle demande de contact.
    """
    db_contact = Contact(
        nom=contact_data.nom,
        email=contact_data.email,
        telephone=contact_data.telephone,
        objet=contact_data.objet,
        message=contact_data.message
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_all_contacts(db: Session): 
    """
    Récupère tous les messages de contact.
    """
    return db.execute(select(Contact)).scalars().all()

def get_contact(db: Session, id_contact: uuid.UUID): 
    """
    Récupère un message de contact par ID.
    """
    contact = db.get(Contact, id_contact)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact inexistant")
    return contact

def update_contact(db: Session, id_contact: uuid.UUID, contact_update: ContactUpdate):
    """
    Met à jour un message de contact.
    """
    db_contact = get_contact(db, id_contact)
    
    if contact_update.nom:
        db_contact.nom = contact_update.nom
    if contact_update.email:
        db_contact.email = contact_update.email
    if contact_update.telephone:
        db_contact.telephone = contact_update.telephone
    if contact_update.objet:
        db_contact.objet = contact_update.objet
    if contact_update.message:
        db_contact.message = contact_update.message

    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, id_contact: uuid.UUID):
    """
    Supprime un message de contact.
    """
    db_contact = get_contact(db, id_contact)
    db.delete(db_contact)
    db.commit()
    return {"Message": f"Contact {db_contact.nom} supprimé avec succès"}

def delete_all_contacts(db: Session):
    """
    Vider toutes les demandes de contact.
    """
    db.execute(delete(Contact))
    db.commit()
    return {"message": "Tous les contacts ont été supprimés"}

async def send_mail(db: Session, contact: ContactCreate):
    """
    Enregistre le contact en base et envoie la notification par e-mail.
    """
    create_contact(db, contact)

    template_body = {
        "title": contact.objet,
        "name": contact.nom,
        "email": contact.email,
        "message": contact.message
    }

    message = MessageSchema(
        subject="Formulaire de contact - AkibaSolution",
        recipients=[Envs.MAIL_USERNAME],
        reply_to=[contact.email],
        template_body={"body": template_body},
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    # Envoi en utilisant le template HTML spécifié
    await fm.send_message(message, template_name="email.html")

    return {"message": "Votre message a été envoyé avec succès."}