from sqlalchemy.orm import Session
from ..models.database_models import User, Technology, Category, Question
from ..core.auth import get_password_hash
from ..core.logging import get_logger

logger = get_logger("init_data")

def create_admin_user(db: Session):
    """Créer un utilisateur administrateur par défaut"""
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@quiz.local",
            full_name="Administrator",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        logger.info("✅ Utilisateur admin créé (admin/admin123)")
    else:
        logger.info("👤 Utilisateur admin existe déjà")

def create_technologies(db: Session):
    """Créer les technologies par défaut"""
    technologies_data = [
        {
            "name": "spark",
            "display_name": "Apache Spark",
            "description": "Big Data & Traitement distribué",
            "icon": "🔥",
            "color": "bg-orange-100"
        },
        {
            "name": "git",
            "display_name": "Git",
            "description": "Gestion de version",
            "icon": "🌱",
            "color": "bg-red-100"
        },
        {
            "name": "docker",
            "display_name": "Docker",
            "description": "Conteneurisation & DevOps",
            "icon": "🐳",
            "color": "bg-blue-100"
        }
    ]
    
    for tech_data in technologies_data:
        tech = db.query(Technology).filter(Technology.name == tech_data["name"]).first()
        if not tech:
            tech = Technology(**tech_data)
            db.add(tech)
            logger.info(f"✅ Technologie créée: {tech_data['display_name']}")
    
    db.commit()

def create_categories(db: Session):
    """Créer les catégories par défaut"""
    categories_data = [
        # Spark
        {"name": "RDD", "description": "Resilient Distributed Datasets", "technology": "spark"},
        {"name": "DataFrame", "description": "DataFrames et Datasets", "technology": "spark"},
        {"name": "Spark SQL", "description": "SQL et requêtes", "technology": "spark"},
        {"name": "Spark Core", "description": "Concepts de base", "technology": "spark"},
        
        # Git
        {"name": "Basics", "description": "Commandes de base", "technology": "git"},
        {"name": "Branching", "description": "Branches et merge", "technology": "git"},
        {"name": "Advanced", "description": "Fonctionnalités avancées", "technology": "git"},
        
        # Docker
        {"name": "Basics", "description": "Concepts de base", "technology": "docker"},
        {"name": "Concepts", "description": "Images et conteneurs", "technology": "docker"},
        {"name": "Compose", "description": "Docker Compose", "technology": "docker"},
    ]
    
    for cat_data in categories_data:
        tech = db.query(Technology).filter(Technology.name == cat_data["technology"]).first()
        if tech:
            cat = db.query(Category).filter(
                Category.name == cat_data["name"],
                Category.technology_id == tech.id
            ).first()
            if not cat:
                cat = Category(
                    name=cat_data["name"],
                    description=cat_data["description"],
                    technology_id=tech.id
                )
                db.add(cat)
                logger.info(f"✅ Catégorie créée: {cat_data['name']} ({cat_data['technology']})")
    
    db.commit()

def create_initial_questions(db: Session):
    """Créer les questions initiales"""
    
    # Récupérer les technologies et catégories
    spark_tech = db.query(Technology).filter(Technology.name == "spark").first()
    git_tech = db.query(Technology).filter(Technology.name == "git").first()
    docker_tech = db.query(Technology).filter(Technology.name == "docker").first()
    
    # Questions Spark
    if spark_tech:
        rdd_cat = db.query(Category).filter(
            Category.name == "RDD", 
            Category.technology_id == spark_tech.id
        ).first()
        
        core_cat = db.query(Category).filter(
            Category.name == "Spark Core", 
            Category.technology_id == spark_tech.id
        ).first()
        
        if rdd_cat:
            spark_questions = [
                {
                    "technology_id": spark_tech.id,
                    "category_id": rdd_cat.id,
                    "question_text": "What is the primary data structure in Spark?",
                    "options": [
                        "RDD (Resilient Distributed Dataset)",
                        "DataFrame",
                        "Dataset",
                        "Array"
                    ],
                    "correct_answer": "RDD (Resilient Distributed Dataset)",
                    "explanation": "RDD is the fundamental data structure in Spark that represents an immutable, distributed collection of objects.",
                    "difficulty": 1,
                    "tags": ["basics", "rdd", "data-structure"]
                }
            ]
            
            if core_cat:
                spark_questions.append({
                    "technology_id": spark_tech.id,
                    "category_id": core_cat.id,
                    "question_text": "Which of the following is NOT a Spark component?",
                    "options": [
                        "Spark Core",
                        "Spark SQL",
                        "Spark ML",
                        "Spark Database"
                    ],
                    "correct_answer": "Spark Database",
                    "explanation": "Spark Database is not a component of Apache Spark. The main components are Spark Core, Spark SQL, Spark Streaming, MLlib, and GraphX.",
                    "difficulty": 1,
                    "tags": ["components", "basics"]
                })
            
            for q_data in spark_questions:
                existing = db.query(Question).filter(
                    Question.question_text == q_data["question_text"]
                ).first()
                if not existing:
                    question = Question(**q_data)
                    db.add(question)
    
    # Questions Git
    if git_tech:
        basics_cat = db.query(Category).filter(
            Category.name == "Basics", 
            Category.technology_id == git_tech.id
        ).first()
        
        if basics_cat:
            git_questions = [
                {
                    "technology_id": git_tech.id,
                    "category_id": basics_cat.id,
                    "question_text": "Quelle commande Git permet d'initialiser un nouveau dépôt ?",
                    "options": [
                        "git init",
                        "git start",
                        "git create",
                        "git new"
                    ],
                    "correct_answer": "git init",
                    "explanation": "La commande git init crée un nouveau dépôt Git vide dans le répertoire courant en initialisant un dossier .git avec toutes les métadonnées nécessaires.",
                    "difficulty": 1,
                    "tags": ["git", "basics", "initialization"]
                },
                {
                    "technology_id": git_tech.id,
                    "category_id": basics_cat.id,
                    "question_text": "Comment ajouter des fichiers à la zone de staging ?",
                    "options": [
                        "git add <fichier>",
                        "git stage <fichier>",
                        "git commit <fichier>",
                        "git push <fichier>"
                    ],
                    "correct_answer": "git add <fichier>",
                    "explanation": "git add permet d'ajouter des fichiers à la zone de staging. Utilisez git add . pour ajouter tous les fichiers modifiés.",
                    "difficulty": 1,
                    "tags": ["git", "basics", "staging"]
                }
            ]
            
            for q_data in git_questions:
                existing = db.query(Question).filter(
                    Question.question_text == q_data["question_text"]
                ).first()
                if not existing:
                    question = Question(**q_data)
                    db.add(question)
    
    # Questions Docker
    if docker_tech:
        basics_cat = db.query(Category).filter(
            Category.name == "Basics", 
            Category.technology_id == docker_tech.id
        ).first()
        
        concepts_cat = db.query(Category).filter(
            Category.name == "Concepts", 
            Category.technology_id == docker_tech.id
        ).first()
        
        if basics_cat and concepts_cat:
            docker_questions = [
                {
                    "technology_id": docker_tech.id,
                    "category_id": basics_cat.id,
                    "question_text": "Qu'est-ce qu'un Dockerfile ?",
                    "options": [
                        "Un fichier texte contenant les instructions pour construire une image Docker",
                        "Un fichier de configuration pour Docker Compose",
                        "Un fichier de logs Docker",
                        "Un fichier binaire contenant une image Docker"
                    ],
                    "correct_answer": "Un fichier texte contenant les instructions pour construire une image Docker",
                    "explanation": "Un Dockerfile est un fichier texte qui contient toutes les commandes nécessaires pour assembler une image Docker. Il définit l'environnement et les dépendances requises.",
                    "difficulty": 2,
                    "tags": ["docker", "basics", "dockerfile"]
                },
                {
                    "technology_id": docker_tech.id,
                    "category_id": concepts_cat.id,
                    "question_text": "Quelle est la différence entre une image et un conteneur Docker ?",
                    "options": [
                        "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image",
                        "Une image est un conteneur en cours d'exécution",
                        "Il n'y a pas de différence",
                        "Un conteneur est un template, une image est son instance"
                    ],
                    "correct_answer": "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image",
                    "explanation": "Une image Docker est un template en lecture seule qui contient les instructions pour créer un conteneur. Un conteneur est une instance exécutable de cette image, comparable à la différence entre une classe et un objet en programmation.",
                    "difficulty": 2,
                    "tags": ["docker", "concepts", "containers", "images"]
                }
            ]
            
            for q_data in docker_questions:
                existing = db.query(Question).filter(
                    Question.question_text == q_data["question_text"]
                ).first()
                if not existing:
                    question = Question(**q_data)
                    db.add(question)
    
    db.commit()
    logger.info("✅ Questions initiales créées")

def init_database(db: Session):
    """Initialiser complètement la base de données"""
    logger.info("🚀 Initialisation de la base de données PostgreSQL")
    
    create_admin_user(db)
    create_technologies(db)
    create_categories(db)
    create_initial_questions(db)
    
    # Statistiques
    user_count = db.query(User).count()
    tech_count = db.query(Technology).count()
    question_count = db.query(Question).count()
    
    logger.info(f"📊 Base de données initialisée:")
    logger.info(f"   - {user_count} utilisateurs")
    logger.info(f"   - {tech_count} technologies") 
    logger.info(f"   - {question_count} questions")
    logger.info("✅ Initialisation terminée avec succès")