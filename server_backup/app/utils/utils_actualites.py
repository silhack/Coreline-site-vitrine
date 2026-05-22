import os
import uuid
from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIR = Path("app/static/actualites/images")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Mo


def save_image(image: UploadFile) -> str:
    if not image.filename:
        raise ValueError("Le fichier uploadé n'a pas de nom.")

    file_ext = Path(image.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Extension non autorisée : {file_ext}")

    # Lire le contenu pour vérifier la taille
    content = image.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise ValueError("La taille du fichier dépasse la limite autorisée (5 Mo).")

    # Réinitialiser le curseur
    image.file.seek(0)

    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    return f"/static/actualites/images/{filename}"


def delete_image_file(image_url: str):
    if not image_url.startswith("/static/"):
        print("URL d'image invalide :", image_url)
        return

    absolute_path = Path(os.getcwd()) / "app" / image_url.lstrip("/")
    print(absolute_path)
    
    # Vérification de l'existence du fichier
    if absolute_path.exists() and absolute_path.is_file():
        try:
            absolute_path.unlink()  # Suppression du fichier
            print(f"[Succès] Le fichier {absolute_path} a été supprimé.")
            return True
        except Exception as e:
            print(f"[Erreur] Impossible de supprimer le fichier {absolute_path}: {e}")
            return False
    else:
        print(f"[Erreur] Le fichier {absolute_path} n'existe pas.")
        return False