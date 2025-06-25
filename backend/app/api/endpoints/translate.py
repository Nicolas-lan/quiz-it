from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging

# Pour l'instant, nous utilisons une simulation de traduction
# En production, vous pourriez utiliser Google Translate API, DeepL, etc.

router = APIRouter()
logger = logging.getLogger("quiz_app.translate")

class TranslationRequest(BaseModel):
    text: str
    target: str  # fr, en, es
    source: Optional[str] = "fr"

class TranslationResponse(BaseModel):
    translatedText: str
    originalText: str
    targetLanguage: str
    sourceLanguage: str

# Dictionnaire de traductions statiques pour les tests
# En production, remplacer par un vrai service de traduction
STATIC_TRANSLATIONS = {
    "en": {
        "Qu'est-ce qu'un RDD ?": "What is an RDD?",
        "Qu'est-ce qu'un RDD dans Apache Spark?": "What is an RDD in Apache Spark?",
        "Qu'est-ce qu'Apache Spark ?": "What is Apache Spark?",
        "Comment initialiser un RDD ?": "How to initialize an RDD?",
        "Quelle commande Git permet d'initialiser un nouveau dépôt ?": "Which Git command initializes a new repository?",
        "Comment ajouter des fichiers à la zone de staging ?": "How to add files to the staging area?",
        "Qu'est-ce qu'un Dockerfile ?": "What is a Dockerfile?",
        "Quelle est la différence entre une image et un conteneur Docker ?": "What is the difference between a Docker image and container?",
        "RDD (Resilient Distributed Dataset)": "RDD (Resilient Distributed Dataset)",
        "DataFrame": "DataFrame",
        "Dataset": "Dataset",
        "Array": "Array",
        "git init": "git init",
        "git start": "git start",
        "git create": "git create",
        "git new": "git new",
        "git add <fichier>": "git add <file>",
        "git stage <fichier>": "git stage <file>",
        "git commit <fichier>": "git commit <file>",
        "git push <fichier>": "git push <file>",
        "Un fichier texte contenant les instructions pour construire une image Docker": "A text file containing instructions to build a Docker image",
        "Un fichier de configuration pour Docker Compose": "A configuration file for Docker Compose",
        "Un fichier de logs Docker": "A Docker log file",
        "Un fichier binaire contenant une image Docker": "A binary file containing a Docker image",
        "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image": "An image is a read-only template, a container is an executable instance of the image",
        "Une image est un conteneur en cours d'exécution": "An image is a running container",
        "Il n'y a pas de différence": "There is no difference",
        "Un conteneur est un template, une image est son instance": "A container is a template, an image is its instance"
    },
    "es": {
        "Qu'est-ce qu'un RDD ?": "¿Qué es un RDD?",
        "Qu'est-ce qu'un RDD dans Apache Spark?": "¿Qué es un RDD en Apache Spark?",
        "Qu'est-ce qu'Apache Spark ?": "¿Qué es Apache Spark?",
        "Comment initialiser un RDD ?": "¿Cómo inicializar un RDD?",
        "Quelle commande Git permet d'initialiser un nouveau dépôt ?": "¿Qué comando de Git permite inicializar un nuevo repositorio?",
        "Comment ajouter des fichiers à la zone de staging ?": "¿Cómo agregar archivos al área de staging?",
        "Qu'est-ce qu'un Dockerfile ?": "¿Qué es un Dockerfile?",
        "Quelle est la différence entre une image et un conteneur Docker ?": "¿Cuál es la diferencia entre una imagen y un contenedor Docker?",
        "RDD (Resilient Distributed Dataset)": "RDD (Conjunto de Datos Distribuido Resiliente)",
        "DataFrame": "DataFrame",
        "Dataset": "Dataset", 
        "Array": "Array",
        "git init": "git init",
        "git start": "git start",
        "git create": "git create",
        "git new": "git new",
        "git add <fichier>": "git add <archivo>",
        "git stage <fichier>": "git stage <archivo>",
        "git commit <fichier>": "git commit <archivo>",
        "git push <fichier>": "git push <archivo>",
        "Un fichier texte contenant les instructions pour construire une image Docker": "Un archivo de texto que contiene las instrucciones para construir una imagen Docker",
        "Un fichier de configuration pour Docker Compose": "Un archivo de configuración para Docker Compose",
        "Un fichier de logs Docker": "Un archivo de logs de Docker",
        "Un fichier binaire contenant une image Docker": "Un archivo binario que contiene una imagen Docker",
        "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image": "Una imagen es una plantilla de solo lectura, un contenedor es una instancia ejecutable de la imagen",
        "Une image est un conteneur en cours d'exécution": "Una imagen es un contenedor en ejecución",
        "Il n'y a pas de différence": "No hay diferencia",
        "Un conteneur est un template, une image est son instance": "Un contenedor es una plantilla, una imagen es su instancia"
    }
}

@router.get("/languages")
async def get_supported_languages():
    """Obtenir la liste des langues supportées"""
    return {
        "languages": [
            {"code": "fr", "name": "Français", "flag": "🇫🇷"},
            {"code": "en", "name": "English", "flag": "🇬🇧"},
            {"code": "es", "name": "Español", "flag": "🇪🇸"}
        ]
    }

@router.get("/cache/stats")
async def get_translation_stats():
    """Statistiques des traductions (debug)"""
    # En production, retourner des stats du cache Redis
    return {
        "total_translations": len(STATIC_TRANSLATIONS["en"]) + len(STATIC_TRANSLATIONS["es"]),
        "supported_languages": ["fr", "en", "es"],
        "cache_status": "static_dictionary"
    }

@router.post("", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Traduire du texte d'une langue vers une autre
    En production, utiliser un vrai service de traduction
    """
    logger.info(f"Traduction demandée: '{request.text[:50]}...' ({request.source} → {request.target})")
    
    # Validation des langues supportées
    supported_languages = ["fr", "en", "es"]
    if request.target not in supported_languages:
        raise HTTPException(
            status_code=400, 
            detail=f"Langue cible non supportée: {request.target}. Langues disponibles: {supported_languages}"
        )
    
    if request.source not in supported_languages:
        raise HTTPException(
            status_code=400,
            detail=f"Langue source non supportée: {request.source}. Langues disponibles: {supported_languages}"
        )
    
    # Si même langue, retourner le texte original
    if request.source == request.target:
        return TranslationResponse(
            translatedText=request.text,
            originalText=request.text,
            targetLanguage=request.target,
            sourceLanguage=request.source
        )
    
    # Recherche dans les traductions statiques
    translated_text = request.text
    if request.target in STATIC_TRANSLATIONS:
        translated_text = STATIC_TRANSLATIONS[request.target].get(request.text, request.text)
    
    # Si pas de traduction trouvée et ce n'est pas déjà la langue cible
    if translated_text == request.text and request.source != request.target:
        logger.warning(f"Traduction non trouvée pour: '{request.text}' ({request.source} → {request.target})")
        # En production, appeler ici l'API de traduction externe
        # translated_text = await call_translation_api(request.text, request.target, request.source)
    
    logger.info(f"Traduction effectuée: '{translated_text[:50]}...'")
    
    return TranslationResponse(
        translatedText=translated_text,
        originalText=request.text,
        targetLanguage=request.target,
        sourceLanguage=request.source
    )