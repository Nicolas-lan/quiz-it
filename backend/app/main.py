import logging
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import schemas
from .core.db import get_db, engine, Base, SessionLocal
from .core.init_data import init_database
from .core.auth import get_current_active_user, get_optional_current_user
from .api.endpoints import auth, dashboard
from .models.database_models import User, Technology, Question, QuizSession

# Configuration du logging
def setup_simple_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"quiz_app_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

setup_simple_logging()
logger = logging.getLogger("quiz_app")

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quiz IT API",
    description="API pour quiz multi-technologies avec authentification",
    version="2.0.0"
)

# Middleware CORS - Configuration plus robuste
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://0.0.0.0:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """Initialisation au démarrage"""
    logger.info("🚀 Démarrage de Quiz IT API v2.0")
    
    try:
        db = SessionLocal()
        
        # Vérifier si la base est initialisée
        user_count = db.query(User).count()
        
        if user_count == 0:
            logger.info("🔧 Initialisation de la base de données...")
            init_database(db)
        else:
            tech_count = db.query(Technology).count()
            question_count = db.query(Question).count()
            logger.info(f"✅ Base de données déjà initialisée:")
            logger.info(f"   - {user_count} utilisateurs")
            logger.info(f"   - {tech_count} technologies")
            logger.info(f"   - {question_count} questions")
        
        db.close()
        logger.info("✅ Application démarrée avec succès")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation: {e}", exc_info=True)
        raise

# Inclusion des routes d'authentification
app.include_router(auth.router, prefix="/auth", tags=["authentification"])

# Inclusion des routes du dashboard
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

# Inclusion des routes de traduction
from .api.endpoints import translate
app.include_router(translate.router, prefix="/api/translate", tags=["traduction"])

@app.get("/")
def read_root():
    """Page d'accueil de l'API"""
    logger.info("Accès à la page d'accueil de l'API")
    return {
        "message": "Quiz IT API v2.0",
        "version": "2.0.0",
        "features": [
            "Authentification JWT",
            "Base PostgreSQL",
            "Quiz multi-technologies",
            "Gestion des utilisateurs"
        ],
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    """Vérification de l'état de l'application"""
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/test")
def test_endpoint():
    """Endpoint de test simple"""
    return {"message": "Test endpoint working", "status": "ok"}

@app.get("/technologies-debug")
def get_technologies_debug(db: Session = Depends(get_db)):
    """Debug des technologies sans schéma Pydantic"""
    try:
        from .models.database_models import Technology
        technologies = db.query(Technology).filter(Technology.is_active == True).all()
        
        result = []
        for tech in technologies:
            result.append({
                "id": tech.id,
                "name": tech.name,
                "display_name": tech.display_name,
                "description": tech.description,
                "icon": tech.icon,
                "color": tech.color,
                "is_active": tech.is_active,
                "created_at": str(tech.created_at)
            })
        
        return {"technologies": result, "count": len(result)}
    except Exception as e:
        return {"error": str(e), "type": str(type(e))}

# === ROUTES TECHNOLOGIES ===

@app.get("/technologies")
def get_technologies(db: Session = Depends(get_db)):
    """Récupérer toutes les technologies"""
    logger.info("Récupération des technologies")
    
    try:
        from .models.database_models import Technology
        technologies = db.query(Technology).filter(Technology.is_active == True).all()
        
        # Sérialisation manuelle pour éviter les problèmes Pydantic
        result = []
        for tech in technologies:
            result.append({
                "id": tech.id,
                "name": tech.name,
                "display_name": tech.display_name,
                "description": tech.description,
                "icon": tech.icon,
                "color": tech.color,
                "is_active": tech.is_active
            })
        
        logger.info(f"✅ {len(result)} technologies récupérées")
        return result
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des technologies: {e}", exc_info=True)
        return {"error": str(e)}

@app.get("/technologies/{tech_name}/categories", response_model=List[schemas.Category])
def get_technology_categories(tech_name: str, db: Session = Depends(get_db)):
    """Récupérer les catégories d'une technologie"""
    logger.info(f"Récupération des catégories pour: {tech_name}")
    
    from .models.database_models import Technology, Category
    
    tech = db.query(Technology).filter(Technology.name == tech_name).first()
    if not tech:
        raise HTTPException(status_code=404, detail="Technologie non trouvée")
    
    categories = db.query(Category).filter(Category.technology_id == tech.id).all()
    return categories

# === ROUTES QUESTIONS ===

@app.get("/questions")
def get_questions(
    technology: str = None,
    category: str = None,
    difficulty: int = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Récupérer les questions (sans les bonnes réponses)"""
    logger.info(f"Récupération des questions - tech: {technology}, cat: {category}, diff: {difficulty}")
    
    from .models.database_models import Question, Technology, Category
    
    try:
        query = db.query(Question).filter(Question.is_active == True)
        
        if technology:
            tech = db.query(Technology).filter(Technology.name == technology).first()
            if tech:
                query = query.filter(Question.technology_id == tech.id)
        
        if category:
            cat = db.query(Category).filter(Category.name == category).first()
            if cat:
                query = query.filter(Question.category_id == cat.id)
        
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)
        
        questions = query.limit(limit).all()
        
        # Sérialisation manuelle pour éviter les problèmes Pydantic
        result = []
        for q in questions:
            import json
            result.append({
                "id": q.id,
                "technology_id": q.technology_id,
                "category_id": q.category_id,
                "question_text": q.question_text,
                "options": json.loads(q.options) if isinstance(q.options, str) else q.options,
                "difficulty": q.difficulty,
                "images": q.images,
                "tags": json.loads(q.tags) if isinstance(q.tags, str) else q.tags,
                "technology": q.technology.name if q.technology else None,
                "category": q.category.name if q.category else None
            })
        
        logger.info(f"✅ {len(result)} questions récupérées")
        return result
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération des questions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")

@app.get("/questions/random")
def get_random_question(
    technology: str = None,
    category: str = None,
    difficulty: int = None,
    db: Session = Depends(get_db)
):
    """Récupérer une question aléatoire"""
    logger.info(f"Récupération question aléatoire - tech: {technology}")
    
    from .models.database_models import Question, Technology, Category
    
    try:
        query = db.query(Question).filter(Question.is_active == True)
        
        if technology:
            tech = db.query(Technology).filter(Technology.name == technology).first()
            if tech:
                query = query.filter(Question.technology_id == tech.id)
        
        if category:
            cat = db.query(Category).filter(Category.name == category).first()
            if cat:
                query = query.filter(Question.category_id == cat.id)
        
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)
        
        question = query.order_by(func.random()).first()
        
        if question is None:
            logger.warning("❌ Aucune question aléatoire trouvée")
            raise HTTPException(status_code=404, detail="Aucune question trouvée")
        
        logger.info(f"✅ Question aléatoire récupérée: ID {question.id}")
        
        # Sérialisation manuelle pour éviter les problèmes Pydantic
        import json
        return {
            "id": question.id,
            "technology_id": question.technology_id,
            "category_id": question.category_id,
            "question_text": question.question_text,
            "options": json.loads(question.options) if isinstance(question.options, str) else question.options,
            "difficulty": question.difficulty,
            "images": question.images,
            "tags": json.loads(question.tags) if isinstance(question.tags, str) else question.tags,
            "technology": question.technology.name if question.technology else None,
            "category": question.category.name if question.category else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors de la récupération d'une question aléatoire: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")

# === ROUTES QUIZ SESSIONS (authentification requise) ===

@app.post("/quiz/start", response_model=schemas.QuizSession)
def start_quiz(
    quiz_data: schemas.QuizSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Démarrer une nouvelle session de quiz"""
    logger.info(f"Début de quiz pour {current_user.username}")
    
    # Vérifier que la technologie existe
    tech = db.query(Technology).filter(Technology.id == quiz_data.technology_id).first()
    if not tech:
        raise HTTPException(status_code=404, detail="Technologie non trouvée")
    
    # Créer la session
    session = QuizSession(
        user_id=current_user.id,
        technology_id=quiz_data.technology_id,
        status="in_progress"
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    logger.info(f"✅ Session de quiz créée: {session.id}")
    return session

@app.get("/quiz/sessions", response_model=List[schemas.QuizSession])
def get_user_quiz_sessions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer les sessions de quiz de l'utilisateur"""
    sessions = db.query(models.database_models.QuizSession).filter(
        models.database_models.QuizSession.user_id == current_user.id
    ).order_by(models.database_models.QuizSession.started_at.desc()).all()
    
    return sessions

# === ROUTES STATISTIQUES ===

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Statistiques générales de l'application"""
    logger.info("Récupération des statistiques")
    
    try:
        from .models.database_models import User, Technology, Question, QuizSession
        
        total_users = db.query(User).count()
        total_technologies = db.query(Technology).filter(Technology.is_active == True).count()
        total_questions = db.query(Question).filter(Question.is_active == True).count()
        total_sessions = db.query(QuizSession).count()
        
        # Questions par technologie
        tech_stats = db.query(
            Technology.name,
            Technology.display_name,
            func.count(Question.id).label('question_count')
        ).join(Question).filter(
            Technology.is_active == True,
            Question.is_active == True
        ).group_by(Technology.id, Technology.name, Technology.display_name).all()
        
        stats = {
            "total_users": total_users,
            "total_technologies": total_technologies,
            "total_questions": total_questions,
            "total_quiz_sessions": total_sessions,
            "questions_by_technology": [
                {
                    "technology": tech.name,
                    "display_name": tech.display_name,
                    "question_count": tech.question_count
                }
                for tech in tech_stats
            ]
        }
        
        logger.info(f"✅ Statistiques calculées")
        return stats
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du calcul des statistiques: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur")