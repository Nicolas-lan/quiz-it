#!/usr/bin/env python3
"""
Script pour ajouter massivement des questions au quiz avec support d'images
Usage: python add_questions.py --tech spark --file questions_spark.json --images-dir ./images
"""

import json
import sys
import argparse
import shutil
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from typing import List, Dict, Optional

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.db import SessionLocal
from app.models.database_models import Technology, Category, Question

# Configuration des dossiers d'images
IMAGES_BASE_DIR = Path("/app/static/images")
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

def setup_image_directories():
    """Créer les dossiers d'images nécessaires"""
    dirs_to_create = [
        IMAGES_BASE_DIR,
        IMAGES_BASE_DIR / "questions",
        IMAGES_BASE_DIR / "code_examples",
        IMAGES_BASE_DIR / "diagrams",
        IMAGES_BASE_DIR / "screenshots"
    ]
    
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Dossiers d'images configurés dans {IMAGES_BASE_DIR}")

def copy_image_to_static(source_path: str, category: str = "questions") -> Optional[str]:
    """
    Copier une image vers le dossier static et retourner l'URL relative
    
    Args:
        source_path: Chemin vers l'image source
        category: Catégorie d'image (questions, code_examples, diagrams, screenshots)
    
    Returns:
        URL relative de l'image ou None si erreur
    """
    source = Path(source_path)
    
    if not source.exists():
        print(f"⚠️  Image non trouvée: {source_path}")
        return None
    
    if source.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        print(f"⚠️  Extension non supportée: {source.suffix}")
        return None
    
    # Générer un nom unique pour éviter les conflits
    unique_name = f"{uuid.uuid4().hex}{source.suffix}"
    destination = IMAGES_BASE_DIR / category / unique_name
    
    try:
        shutil.copy2(source, destination)
        # Retourner l'URL relative pour l'application
        return f"/static/images/{category}/{unique_name}"
    except Exception as e:
        print(f"❌ Erreur lors de la copie d'image: {e}")
        return None

def process_question_images(question_data: Dict, images_base_path: str) -> Dict:
    """
    Traiter les images d'une question et mettre à jour les chemins
    
    Formats supportés dans le JSON:
    {
        "question_text": "Que fait ce code?",
        "question_image": "spark_rdd_example.png",
        "code_image": "code_with_blanks.png", 
        "diagram_image": "spark_architecture.png",
        "options": [...],
        "images": {
            "question": "path/to/question_image.png",
            "code": "path/to/code_example.png",
            "diagram": "path/to/diagram.png",
            "screenshot": "path/to/screenshot.png"
        }
    }
    """
    processed_question = question_data.copy()
    images_dir = Path(images_base_path) if images_base_path else None
    
    # Traiter les images individuelles (ancien format)
    image_fields = {
        'question_image': 'questions',
        'code_image': 'code_examples', 
        'diagram_image': 'diagrams',
        'screenshot_image': 'screenshots'
    }
    
    for field, category in image_fields.items():
        if field in question_data and question_data[field]:
            if images_dir:
                image_path = images_dir / question_data[field]
            else:
                image_path = Path(question_data[field])
            
            url = copy_image_to_static(str(image_path), category)
            if url:
                processed_question[field] = url
                print(f"📷 Image copiée: {question_data[field]} -> {url}")
            else:
                processed_question[field] = None
    
    # Traiter le nouveau format avec objet images
    if 'images' in question_data and isinstance(question_data['images'], dict):
        processed_images = {}
        
        for image_type, image_path in question_data['images'].items():
            if image_path:
                # Déterminer la catégorie basée sur le type
                category_map = {
                    'question': 'questions',
                    'code': 'code_examples',
                    'diagram': 'diagrams', 
                    'screenshot': 'screenshots',
                    'example': 'code_examples'
                }
                category = category_map.get(image_type, 'questions')
                
                if images_dir:
                    full_path = images_dir / image_path
                else:
                    full_path = Path(image_path)
                
                url = copy_image_to_static(str(full_path), category)
                if url:
                    processed_images[image_type] = url
                    print(f"📷 Image {image_type} copiée: {image_path} -> {url}")
        
        processed_question['images'] = processed_images
    
    return processed_question

def load_questions_from_json(file_path: str) -> List[Dict]:
    """Charger les questions depuis un fichier JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_categories_for_tech(db: Session, tech_id: int, tech_name: str) -> Dict[str, int]:
    """Créer les catégories pour une technologie"""
    categories_map = {
        "spark": [
            {"name": "RDD", "description": "Resilient Distributed Datasets"},
            {"name": "DataFrame", "description": "DataFrame et Dataset APIs"},
            {"name": "Spark SQL", "description": "Requêtes SQL et optimisation"},
            {"name": "Streaming", "description": "Traitement temps réel"},
            {"name": "MLlib", "description": "Machine Learning"},
            {"name": "Architecture", "description": "Architecture et concepts"},
            {"name": "Performance", "description": "Optimisation et tuning"},
            {"name": "Deployment", "description": "Déploiement et configuration"},
            {"name": "Code Examples", "description": "Exemples de code avec trous"},
            {"name": "Visual", "description": "Questions avec diagrammes"}
        ],
        "git": [
            {"name": "Basics", "description": "Commandes de base"},
            {"name": "Branching", "description": "Gestion des branches"},
            {"name": "Merging", "description": "Fusion et résolution de conflits"},
            {"name": "Remote", "description": "Dépôts distants"},
            {"name": "Advanced", "description": "Commandes avancées"},
            {"name": "Workflow", "description": "Flux de travail et bonnes pratiques"},
            {"name": "Hooks", "description": "Git hooks et automation"},
            {"name": "Troubleshooting", "description": "Résolution de problèmes"},
            {"name": "Visual Workflow", "description": "Workflows visuels"},
            {"name": "Command Examples", "description": "Exemples de commandes"}
        ],
        "docker": [
            {"name": "Basics", "description": "Concepts de base"},
            {"name": "Images", "description": "Gestion des images"},
            {"name": "Containers", "description": "Gestion des conteneurs"},
            {"name": "Dockerfile", "description": "Construction d'images"},
            {"name": "Compose", "description": "Docker Compose"},
            {"name": "Networking", "description": "Réseaux Docker"},
            {"name": "Volumes", "description": "Gestion des volumes"},
            {"name": "Production", "description": "Déploiement en production"},
            {"name": "Code Examples", "description": "Exemples de Dockerfile"},
            {"name": "Architecture", "description": "Diagrammes d'architecture"}
        ]
    }
    
    categories = categories_map.get(tech_name, [
        {"name": "General", "description": "Questions générales"},
        {"name": "Advanced", "description": "Questions avancées"},
        {"name": "Visual", "description": "Questions avec images"}
    ])
    
    category_ids = {}
    for cat_data in categories:
        existing_cat = db.query(Category).filter(
            Category.name == cat_data["name"],
            Category.technology_id == tech_id
        ).first()
        
        if not existing_cat:
            category = Category(
                name=cat_data["name"],
                description=cat_data["description"],
                technology_id=tech_id
            )
            db.add(category)
            db.commit()
            category_ids[cat_data["name"]] = category.id
            print(f"✅ Catégorie créée: {cat_data['name']}")
        else:
            category_ids[cat_data["name"]] = existing_cat.id
            print(f"👤 Catégorie existe: {cat_data['name']}")
    
    return category_ids

def add_questions_bulk(db: Session, tech_name: str, questions_data: List[Dict], images_dir: Optional[str]) -> int:
    """Ajouter les questions en masse avec support d'images"""
    tech = db.query(Technology).filter(Technology.name == tech_name).first()
    if not tech:
        print(f"❌ Technologie '{tech_name}' non trouvée")
        return 0
    
    category_ids = create_categories_for_tech(db, tech.id, tech_name)
    
    added_count = 0
    for i, q_data in enumerate(questions_data, 1):
        print(f"\n📝 Traitement question {i}/{len(questions_data)}")
        
        # Traiter les images si présentes
        processed_question = process_question_images(q_data, images_dir)
        
        # Vérifier si la question existe déjà
        existing = db.query(Question).filter(
            Question.question_text == processed_question["question_text"],
            Question.technology_id == tech.id
        ).first()
        
        if existing:
            print(f"⚠️  Question existe déjà: {processed_question['question_text'][:50]}...")
            continue
        
        # Déterminer la catégorie
        category_name = processed_question.get("category", "General")
        
        # Si la question a des images, utiliser une catégorie visuelle appropriée
        has_images = any([
            processed_question.get("question_image"),
            processed_question.get("code_image"),
            processed_question.get("diagram_image"),
            processed_question.get("images")
        ])
        
        if has_images and category_name == "General":
            if processed_question.get("code_image") or (processed_question.get("images", {}).get("code")):
                category_name = "Code Examples"
            elif processed_question.get("diagram_image") or (processed_question.get("images", {}).get("diagram")):
                category_name = "Visual" if "Visual" in category_ids else "Architecture"
            else:
                category_name = "Visual" if "Visual" in category_ids else category_name
        
        category_id = category_ids.get(category_name, list(category_ids.values())[0])
        
        # Préparer les métadonnées d'images pour stockage
        image_metadata = {}
        if processed_question.get("question_image"):
            image_metadata["question_image"] = processed_question["question_image"]
        if processed_question.get("code_image"):
            image_metadata["code_image"] = processed_question["code_image"]
        if processed_question.get("diagram_image"):
            image_metadata["diagram_image"] = processed_question["diagram_image"]
        if processed_question.get("images"):
            image_metadata["images"] = processed_question["images"]
        
        # Ajouter les métadonnées d'images aux tags
        tags = processed_question.get("tags", [])
        if image_metadata:
            tags.append("with_images")
            if image_metadata.get("code_image") or image_metadata.get("images", {}).get("code"):
                tags.append("code_example")
            if image_metadata.get("diagram_image") or image_metadata.get("images", {}).get("diagram"):
                tags.append("visual_diagram")
        
        question = Question(
            technology_id=tech.id,
            category_id=category_id,
            question_text=processed_question["question_text"],
            options=processed_question["options"],
            correct_answer=processed_question["correct_answer"],
            explanation=processed_question.get("explanation", ""),
            difficulty=processed_question.get("difficulty", 1),
            tags=tags,
            is_active=True
        )
        
        db.add(question)
        added_count += 1
        
        if added_count % 50 == 0:
            db.commit()
            print(f"📊 {added_count} questions ajoutées...")
    
    db.commit()
    print(f"✅ Total: {added_count} questions ajoutées pour {tech_name}")
    return added_count

def main():
    parser = argparse.ArgumentParser(description='Ajouter des questions au quiz avec support d\'images')
    parser.add_argument('--tech', required=True, choices=['spark', 'git', 'docker'], 
                       help='Technologie cible')
    parser.add_argument('--file', required=True, help='Fichier JSON contenant les questions')
    parser.add_argument('--images-dir', help='Dossier contenant les images (optionnel)')
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"❌ Fichier non trouvé: {args.file}")
        return
    
    if args.images_dir and not Path(args.images_dir).exists():
        print(f"❌ Dossier d'images non trouvé: {args.images_dir}")
        return
    
    # Configurer les dossiers d'images
    setup_image_directories()
    
    print(f"🚀 Chargement des questions pour {args.tech} depuis {args.file}")
    if args.images_dir:
        print(f"📁 Dossier d'images: {args.images_dir}")
    
    questions_data = load_questions_from_json(args.file)
    print(f"📝 {len(questions_data)} questions trouvées")
    
    # Compter les questions avec images
    questions_with_images = sum(1 for q in questions_data if any([
        q.get("question_image"), q.get("code_image"), q.get("diagram_image"), q.get("images")
    ]))
    print(f"📷 {questions_with_images} questions avec images détectées")
    
    db = SessionLocal()
    try:
        added = add_questions_bulk(db, args.tech, questions_data, args.images_dir)
        print(f"🎉 Import terminé: {added} questions ajoutées")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()