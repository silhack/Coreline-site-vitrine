import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from pydantic import BaseModel, EmailStr, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_ip_addr
from slowapi.errors import RateLimitExceeded
import bleach

# Configurer les logs internes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mail_api")

# Charger les variables d'environnement
load_dotenv()

# Configurer le Rate Limiter
def get_real_client_ip(request: Request) -> str:
    # Cherche d'abord si Nginx a transmis la vraie IP
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Prend la première IP de la liste (l'IP d'origine du client)
        return forwarded_for.split(",")[0].strip()
    return get_ip_addr(request) # Fallback local standard

limiter = Limiter(key_func=get_real_client_ip)

app = FastAPI(
    title="Coreline Alliance Mail API",
    description="API de messagerie souveraine et ultra-légère",
    version="1.0.0",
    docs_url=None if os.getenv("ENV") == "production" else "/docs",
    redoc_url=None if os.getenv("ENV") == "production" else "/redoc"
)

# Enregistrer le limiter et son gestionnaire d'erreur dans FastAPI
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configuration CORS
allowed_origins = os.getenv("ALLOWED_ORIGIN", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration de fastapi-mail
MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
MAIL_FROM = os.getenv('MAIL_FROM', MAIL_USERNAME)
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_SERVER = os.getenv('MAIL_SERVER', '')
MAIL_STARTTLS = os.getenv('MAIL_STARTTLS', 'True').lower() == 'true'
MAIL_SSL_TLS = os.getenv('MAIL_SSL_TLS', 'False').lower() == 'true'

mail_config = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM or MAIL_USERNAME,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=MAIL_STARTTLS,
    MAIL_SSL_TLS=MAIL_SSL_TLS,
    USE_CREDENTIALS=True if MAIL_PASSWORD else False,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).resolve().parent / "templates"
)

# Schéma de données durci contre les attaques par déni de service de payload
class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    subject: str | None = Field(None, max_length=150)
    message: str = Field(..., min_length=10, max_length=5000)
    website: str | None = Field(None, max_length=100) # Honeypot caché pour les bots

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Coreline Alliance Mail API",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/contact", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def send_contact_email(request: Request, contact: ContactRequest):
    """
    Reçoit les informations de contact et envoie un e-mail de notification
    aux administrateurs de la boîte professionnelle.
    """
    client_ip = request.client.host if request.client else "unknown"

    # 1. Protection Anti-spam Honeypot Côté Serveur
    if contact.website:
        logger.warning(f"[SPAM DETECTED] Le bot a rempli le champ honeypot. IP: {client_ip}")
        # Retourne un faux succès (200 OK) pour tromper le robot sans consommer de SMTP
        return {
            "status": "success",
            "message": "Votre message a été envoyé avec succès."
        }

    # 2. Validation de sécurité anti-CRLF (Prévention d'Header Injection dans reply_to / subject)
    for field_name, value in [("name", contact.name), ("email", contact.email), ("subject", contact.subject)]:
        if value and any(c in value for c in ["\r", "\n"]):
            logger.error(f"[SECURITY ALERT] Tentative d'injection CRLF détectée dans '{field_name}' depuis l'IP: {client_ip}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Requête invalide."
            )

    # 3. Vérification que les configurations minimales sont présentes
    if not MAIL_USERNAME or not MAIL_SERVER:
        # En développement ou si non configuré, on logue dans la console
        logger.info(f"[SIMULATION MAIL] Reçu depuis IP: {client_ip}")
        logger.info(f"De: {contact.email}")
        logger.info(f"Nom: {contact.name}")
        logger.info(f"Sujet: {contact.subject or 'Sans sujet'}")
        logger.info(f"Message: {contact.message}")
        return {
            "status": "success",
            "message": "Message simulé avec succès en console (SMTP non configuré)."
        }

    try:
        # 4. Préparation du template
        clean_message = bleach.clean(contact.message, tags=[], strip=True)
        template_body = {
            "title": contact.subject or "Nouveau message de contact",
            "name": contact.name,
            "email": contact.email,
            "message": clean_message
        }

        # 5. Construction du message
        message = MessageSchema(
            subject=f"Contact Coreline Alliance - {contact.subject or 'Nouveau message'}",
            recipients=[os.getenv('MAIL_TO', MAIL_USERNAME)],
            reply_to=[contact.email],
            template_body={"body": template_body},
            subtype=MessageType.html
        )

        # 6. Envoi
        fm = FastMail(mail_config)
        await fm.send_message(message, template_name="email.html")

        logger.info(f"[EMAIL SENT] Notification expédiée avec succès pour {contact.email}. IP: {client_ip}")
        return {
            "status": "success",
            "message": "Votre message a été envoyé avec succès."
        }

    except Exception as e:
        # Log interne sécurisé avec niveau d'erreur approprié
        logger.error(f"[SMTP ERROR] Échec de l'envoi de l'email pour {contact.email} depuis IP {client_ip}. Raison : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Une erreur est survenue lors de l'envoi du message. Veuillez réessayer ultérieurement."
        )

if __name__ == "__main__":
    import uvicorn
    # Dev only — use gunicorn in production
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
