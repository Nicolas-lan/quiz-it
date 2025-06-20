#!/usr/bin/env python3
"""
Script pour importer les nouvelles technologies JavaScript et Python
"""
import json
import sys
import os
from pathlib import Path

# Ajouter le chemin parent pour les imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy.orm import Session
from app.core.db import SessionLocal, engine
from app.models.database_models import Technology, Category, Question, Base

def create_tables():
    """Créer les tables si elles n'existent pas"""
    Base.metadata.create_all(bind=engine)

def import_technology_data(tech_name: str, file_path: str, db: Session):
    """Importe les données d'une technologie depuis un fichier JSON"""
    
    print(f"📂 Importation de {tech_name}...")
    
    # Lire le fichier JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Créer ou récupérer la technologie
    tech = db.query(Technology).filter(Technology.name == tech_name).first()
    if not tech:
        tech = Technology(
            name=tech_name,
            display_name=data.get("technology", tech_name),
            description=f"Questions about {tech_name}",
            icon="💻",
            color="#007bff",
            is_active=True
        )
        db.add(tech)
        db.commit()
        db.refresh(tech)
        print(f"✅ Technologie {tech_name} créée")
    else:
        print(f"ℹ️  Technologie {tech_name} existe déjà")
    
    # Importer les questions
    categories_created = set()
    questions_imported = 0
    
    for question_data in data["questions"]:
        # Créer ou récupérer la catégorie
        category_name = question_data["category"]
        category = db.query(Category).filter(
            Category.name == category_name,
            Category.technology_id == tech.id
        ).first()
        
        if not category:
            category = Category(
                name=category_name,
                technology_id=tech.id
            )
            db.add(category)
            db.commit()
            db.refresh(category)
            categories_created.add(category_name)
        
        # Vérifier si la question existe déjà
        existing_question = db.query(Question).filter(
            Question.question_text == question_data["question_text"],
            Question.technology_id == tech.id
        ).first()
        
        if existing_question:
            print(f"⚠️  Question déjà existante: {question_data['question_text'][:50]}...")
            continue
        
        # Créer la question
        question = Question(
            technology_id=tech.id,
            category_id=category.id,
            question_text=question_data["question_text"],
            options=json.dumps(question_data["options"], ensure_ascii=False),
            correct_answer=question_data["correct_answer"],
            explanation=question_data.get("explanation"),
            difficulty=question_data.get("difficulty", 1),
            tags=json.dumps(question_data.get("tags", []), ensure_ascii=False),
            is_active=True
        )
        
        db.add(question)
        questions_imported += 1
    
    db.commit()
    
    print(f"✅ {tech_name} importé avec succès:")
    print(f"   - {len(categories_created)} nouvelles catégories: {', '.join(categories_created)}")
    print(f"   - {questions_imported} questions importées")
    print()

def main():
    """Fonction principale"""
    print("🚀 Import des nouvelles technologies JavaScript et Python\n")
    
    # Créer les tables
    create_tables()
    
    # Créer une session de base de données
    db = SessionLocal()
    
    try:
        # Chemins des fichiers JSON
        script_dir = Path(__file__).parent
        js_file = script_dir / "javascript_questions.json"
        python_file = script_dir / "python_questions.json"
        
        # Vérifier que les fichiers existent
        if not js_file.exists():
            print(f"❌ Fichier non trouvé: {js_file}")
            return
        
        if not python_file.exists():
            print(f"❌ Fichier non trouvé: {python_file}")
            return
        
        # Importer JavaScript
        import_technology_data("JavaScript", js_file, db)
        
        # Importer Python
        import_technology_data("Python", python_file, db)
        
        # Statistiques finales
        print("📊 Statistiques finales:")
        total_tech = db.query(Technology).filter(Technology.is_active == True).count()
        total_questions = db.query(Question).filter(Question.is_active == True).count()
        
        print(f"   - Technologies actives: {total_tech}")
        print(f"   - Questions totales: {total_questions}")
        
        # Questions par technologie
        print("\n📈 Répartition par technologie:")
        technologies = db.query(Technology).filter(Technology.is_active == True).all()
        for tech in technologies:
            question_count = db.query(Question).filter(
                Question.technology_id == tech.id,
                Question.is_active == True
            ).count()
            print(f"   - {tech.display_name}: {question_count} questions")
        
        print("\n🎉 Import terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()

if __name__ == "__main__":
    main()