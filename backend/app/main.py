import logging
import os
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import get_db, engine, SessionLocal
from .initial_data import init_db
from sqlalchemy.sql import func

# Configuration simple du logging
def setup_simple_logging():
    """Configuration basique du logging"""
    # Créer le dossier logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Nom du fichier de log avec date
    log_file = log_dir / f"quiz_app_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Console
        ]
    )
    
    # Réduire les logs des librairies tierces
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Initialiser le logging
setup_simple_logging()
logger = logging.getLogger("quiz_app")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spark Quiz API")

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (en dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """Initialisation au démarrage avec logging"""
    logger.info("🚀 Démarrage de l'application Spark Quiz API")
    
    try:
        db = SessionLocal()
        question_count = db.query(models.SparkQuestion).count()
        
        if question_count == 0:
            logger.info("Initialisation de la base de données avec les questions par défaut")
            init_db(db)
            new_count = db.query(models.SparkQuestion).count()
            logger.info(f"✅ {new_count} questions ajoutées à la base de données")
        else:
            logger.info(f"✅ Base de données déjà initialisée avec {question_count} questions")
        
        db.close()
        logger.info("✅ Application démarrée avec succès")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation: {e}", exc_info=True)
        raise

@app.get("/questions/", response_model=List[schemas.SparkQuestion])
def get_questions(
    technology: str = None,
    category: str = None,
    difficulty: int = None,
    db: Session = Depends(get_db)
):
    """Récupère les questions avec logging"""
    logger.info(f"Récupération des questions - tech: {technology}, cat: {category}, diff: {difficulty}")
    
    try:
        query = db.query(models.SparkQuestion)
        if technology:
            query = query.filter(models.SparkQuestion.technology == technology)
        if category:
            query = query.filter(models.SparkQuestion.category == category)
        if difficulty:
            query = query.filter(models.SparkQuestion.difficulty == difficulty)
        
        questions = query.all()
        logger.info(f"✅ {len(questions)} questions récupérées")
        return questions
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des questions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/questions/{question_id}", response_model=schemas.SparkQuestion)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Récupère une question spécifique avec logging"""
    logger.info(f"Récupération de la question {question_id}")
    
    try:
        question = db.query(models.SparkQuestion).filter(models.SparkQuestion.id == question_id).first()
        if question is None:
            logger.warning(f"❌ Question {question_id} non trouvée")
            raise HTTPException(status_code=404, detail="Question not found")
        
        logger.info(f"✅ Question {question_id} récupérée ({question.technology})")
        return question
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération de la question {question_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.post("/questions/", response_model=schemas.SparkQuestion)
def create_question(question: schemas.SparkQuestionCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle question avec logging"""
    logger.info(f"Création d'une nouvelle question - tech: {question.technology}")
    
    try:
        # Correction pour compatibilité Pydantic v2
        question_data = question.model_dump() if hasattr(question, 'model_dump') else question.dict()
        db_question = models.SparkQuestion(**question_data)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        logger.info(f"✅ Question créée avec l'ID {db_question.id}")
        return db_question
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la création de la question: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la création")

# Route pour obtenir une question aléatoire
@app.get("/questions/random/", response_model=schemas.SparkQuestion)
def get_random_question(
    technology: str = None,
    category: str = None,
    difficulty: int = None,
    db: Session = Depends(get_db)
):
    """Récupère une question aléatoire avec logging"""
    logger.info(f"Récupération question aléatoire - tech: {technology}, cat: {category}, diff: {difficulty}")
    
    try:
        query = db.query(models.SparkQuestion)
        if technology:
            query = query.filter(models.SparkQuestion.technology == technology)
        if category:
            query = query.filter(models.SparkQuestion.category == category)
        if difficulty:
            query = query.filter(models.SparkQuestion.difficulty == difficulty)
        
        question = query.order_by(func.random()).first()
        
        if question is None:
            logger.warning("❌ Aucune question aléatoire trouvée avec ces critères")
            raise HTTPException(status_code=404, detail="Aucune question trouvée")
        
        logger.info(f"✅ Question aléatoire récupérée: ID {question.id} ({question.technology})")
        return question
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération d'une question aléatoire: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")

# Routes supplémentaires avec logging
@app.get("/")
def read_root():
    """Page d'accueil de l'API"""
    logger.info("Accès à la page d'accueil de l'API")
    return {
        "message": "Spark Quiz API", 
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Vérification de l'état de l'application"""
    logger.debug("Health check demandé")
    return {"status": "healthy"}

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Statistiques de l'application"""
    logger.info("Récupération des statistiques")
    
    try:
        total_questions = db.query(models.SparkQuestion).count()
        technologies = db.query(models.SparkQuestion.technology).distinct().all()
        tech_count = {tech[0]: db.query(models.SparkQuestion).filter(models.SparkQuestion.technology == tech[0]).count() 
                     for tech in technologies}
        
        stats = {
            "total_questions": total_questions,
            "technologies": list(tech_count.keys()),
            "questions_by_technology": tech_count
        }
        
        logger.info(f"✅ Statistiques calculées: {total_questions} questions total")
        return stats
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du calcul des statistiques: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")

# Routes utiles pour le développement et la production
@app.get("/technologies")
def get_technologies(db: Session = Depends(get_db)):
    """Récupère la liste des technologies disponibles"""
    logger.info("Récupération de la liste des technologies")
    
    try:
        technologies = db.query(models.SparkQuestion.technology).distinct().all()
        tech_list = [tech[0] for tech in technologies]
        
        logger.info(f"✅ {len(tech_list)} technologies trouvées: {tech_list}")
        return {"technologies": tech_list}
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des technologies: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/categories")
def get_categories(
    technology: str = None,
    db: Session = Depends(get_db)
):
    """Récupère la liste des catégories disponibles"""
    logger.info(f"Récupération des catégories pour la technologie: {technology}")
    
    try:
        query = db.query(models.SparkQuestion.category).distinct()
        if technology:
            query = query.filter(models.SparkQuestion.technology == technology)
        
        categories = query.all()
        cat_list = [cat[0] for cat in categories]
        
        logger.info(f"✅ {len(cat_list)} catégories trouvées")
        return {"categories": cat_list}
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des catégories: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")