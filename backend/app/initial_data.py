from .models.spark_question import SparkQuestion

# Toutes les questions du quiz
initial_questions = [
    # Questions Spark
    {
        "technology": "spark",
        "question_text": "What is the primary data structure in Spark?",
        "options": [
            "RDD (Resilient Distributed Dataset)",
            "DataFrame",
            "Dataset",
            "Array"
        ],
        "correct_answer": "RDD (Resilient Distributed Dataset)",
        "explanation": "RDD is the fundamental data structure in Spark that represents an immutable, distributed collection of objects.",
        "category": "RDD",
        "difficulty": 1,
        "tags": ["basics", "rdd", "data-structure"]
    },
    {
        "technology": "spark",
        "question_text": "Which of the following is NOT a Spark component?",
        "options": [
            "Spark Core",
            "Spark SQL",
            "Spark ML",
            "Spark Database"
        ],
        "correct_answer": "Spark Database",
        "explanation": "Spark Database is not a component of Apache Spark. The main components are Spark Core, Spark SQL, Spark Streaming, MLlib, and GraphX.",
        "category": "Spark Core",
        "difficulty": 1,
        "tags": ["components", "basics"]
    },
    # Questions Git
    {
        "technology": "git",
        "question_text": "Quelle commande Git permet d'initialiser un nouveau dépôt ?",
        "options": [
            "git init",
            "git start",
            "git create",
            "git new"
        ],
        "correct_answer": "git init",
        "explanation": "La commande git init crée un nouveau dépôt Git vide dans le répertoire courant en initialisant un dossier .git avec toutes les métadonnées nécessaires.",
        "category": "Basics",
        "difficulty": 1,
        "tags": ["git", "basics", "initialization"]
    },
    {
        "technology": "git",
        "question_text": "Comment ajouter des fichiers à la zone de staging ?",
        "options": [
            "git add <fichier>",
            "git stage <fichier>",
            "git commit <fichier>",
            "git push <fichier>"
        ],
        "correct_answer": "git add <fichier>",
        "explanation": "git add permet d'ajouter des fichiers à la zone de staging. Utilisez git add . pour ajouter tous les fichiers modifiés.",
        "category": "Basics",
        "difficulty": 1,
        "tags": ["git", "basics", "staging"]
    },
    # Questions Docker
    {
        "technology": "docker",
        "question_text": "Qu'est-ce qu'un Dockerfile ?",
        "options": [
            "Un fichier texte contenant les instructions pour construire une image Docker",
            "Un fichier de configuration pour Docker Compose",
            "Un fichier de logs Docker",
            "Un fichier binaire contenant une image Docker"
        ],
        "correct_answer": "Un fichier texte contenant les instructions pour construire une image Docker",
        "explanation": "Un Dockerfile est un fichier texte qui contient toutes les commandes nécessaires pour assembler une image Docker. Il définit l'environnement et les dépendances requises.",
        "category": "Basics",
        "difficulty": 2,
        "tags": ["docker", "basics", "dockerfile"]
    },
    {
        "technology": "docker",
        "question_text": "Quelle est la différence entre une image et un conteneur Docker ?",
        "options": [
            "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image",
            "Une image est un conteneur en cours d'exécution",
            "Il n'y a pas de différence",
            "Un conteneur est un template, une image est son instance"
        ],
        "correct_answer": "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image",
        "explanation": "Une image Docker est un template en lecture seule qui contient les instructions pour créer un conteneur. Un conteneur est une instance exécutable de cette image, comparable à la différence entre une classe et un objet en programmation.",
        "category": "Concepts",
        "difficulty": 2,
        "tags": ["docker", "concepts", "containers", "images"]
    }
]

def init_db(db):
    # Supprimer toutes les questions existantes
    db.query(SparkQuestion).delete()
    
    # Ajouter les nouvelles questions
    for question_data in initial_questions:
        question = SparkQuestion(**question_data)
        db.add(question)
    db.commit() 