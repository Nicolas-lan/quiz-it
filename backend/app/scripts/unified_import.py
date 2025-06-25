#!/usr/bin/env python3
"""
Script unifié pour l'import de questions et technologies
Combine les fonctionnalités de add_questions.py, import_all_questions.py et import_new_technologies.py

Usage:
    # Import simple d'une technologie
    python unified_import.py --tech "JavaScript" --file javascript_questions.json
    
    # Import avec images
    python unified_import.py --tech "Spark" --file spark_questions.json --images-dir ./images/spark
    
    # Import batch de toutes les technologies du dossier
    python unified_import.py --batch-import
    
    # Créer une nouvelle technologie avec métadonnées
    python unified_import.py --create-tech "Kubernetes" --display-name "Kubernetes" --icon "⚓" --color "#326ce5"
"""

import json
import sys
import argparse
import shutil
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Tuple

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.db import SessionLocal, engine
from app.models.database_models import Technology, Category, Question, Base

# Configuration des dossiers d'images
IMAGES_BASE_DIR = Path("/app/static/images")
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

# Fichiers par défaut pour l'import batch
DEFAULT_BATCH_FILES = {
    'Apache Spark': 'spark_mixed_questions.json',
    'Git': 'git_mixed_questions.json', 
    'Docker': 'docker_mixed_questions.json',
    'JavaScript': 'javascript_questions.json',
    'Python': 'python_questions.json'
}

class UnifiedImporter:
    """Classe principale pour l'import unifié"""
    
    def __init__(self, db: Session):
        self.db = db
        self.setup_image_directories()
    
    def setup_image_directories(self):
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
    
    def copy_image_to_static(self, source_path: str, category: str = "questions") -> Optional[str]:
        """Copier une image vers le dossier static et retourner l'URL relative"""
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
            return f"/static/images/{category}/{unique_name}"
        except Exception as e:
            print(f"❌ Erreur lors de la copie d'image: {e}")
            return None
    
    def process_question_images(self, question_data: Dict, images_base_path: Optional[str] = None) -> Dict:
        """Traiter les images d'une question et mettre à jour les chemins"""
        processed_question = question_data.copy()
        images_dir = Path(images_base_path) if images_base_path else None
        
        # Traiter les images individuelles (ancien format)
        image_fields = {
            'question_image': 'questions',
            'code_image': 'code_examples',
            'diagram_image': 'diagrams', 
            'screenshot_image': 'screenshots'
        }
        
        updated_images = {}
        
        for field, category in image_fields.items():
            if field in processed_question:
                image_path = processed_question[field]
                if images_dir:
                    full_path = images_dir / image_path
                    new_url = self.copy_image_to_static(str(full_path), category)
                    if new_url:
                        updated_images[field.replace('_image', '')] = new_url
                        del processed_question[field]
                else:
                    # Conserver le chemin original si pas de dossier source
                    updated_images[field.replace('_image', '')] = image_path
                    del processed_question[field]
        
        # Traiter le format avancé (objet images)
        if 'images' in processed_question:
            images_obj = processed_question['images']
            if isinstance(images_obj, dict):
                for key, image_path in images_obj.items():
                    category = {
                        'question': 'questions',
                        'code': 'code_examples',
                        'diagram': 'diagrams',
                        'screenshot': 'screenshots'
                    }.get(key, 'questions')
                    
                    if images_dir:
                        full_path = images_dir / image_path
                        new_url = self.copy_image_to_static(str(full_path), category)
                        if new_url:
                            updated_images[key] = new_url
                    else:
                        updated_images[key] = image_path
        
        # Mettre à jour le champ images si des images ont été trouvées
        if updated_images:
            processed_question['images'] = json.dumps(updated_images)
        elif 'images' in processed_question:
            # Conserver l'objet images original s'il existe
            processed_question['images'] = json.dumps(processed_question['images'])
        
        return processed_question
    
    def get_or_create_technology(self, tech_name: str, display_name: str = None, 
                                icon: str = "💻", color: str = "#007bff") -> Technology:
        """Récupérer ou créer une technologie"""
        tech = self.db.query(Technology).filter(Technology.name == tech_name).first()
        
        if not tech:
            tech = Technology(
                name=tech_name,
                display_name=display_name or tech_name,
                description=f"Questions about {tech_name}",
                icon=icon,
                color=color,
                is_active=True
            )
            self.db.add(tech)
            self.db.commit()
            self.db.refresh(tech)
            print(f"✅ Technologie créée: {tech_name}")
        else:
            # Mettre à jour les métadonnées si fournies
            if display_name:
                tech.display_name = display_name
            if icon != "💻":
                tech.icon = icon
            if color != "#007bff":
                tech.color = color
            self.db.commit()
            print(f"ℹ️  Technologie {tech_name} existe déjà")
        
        return tech
    
    def get_or_create_category(self, tech: Technology, category_name: str) -> Category:
        """Récupérer ou créer une catégorie"""
        category = self.db.query(Category).filter(
            Category.name == category_name,
            Category.technology_id == tech.id
        ).first()
        
        if not category:
            category = Category(
                name=category_name,
                technology_id=tech.id,
                description=f"{category_name} questions for {tech.name}"
            )
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)
        
        return category
    
    def import_questions_from_data(self, tech: Technology, questions_data: List[Dict], 
                                  images_base_path: Optional[str] = None) -> Tuple[int, int]:
        """Importer les questions depuis des données"""
        imported_count = 0
        skipped_count = 0
        
        for q_data in questions_data:
            # Vérifier si la question existe déjà
            existing = self.db.query(Question).filter(
                Question.question_text == q_data['question_text'],
                Question.technology_id == tech.id
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            # Traiter les images
            processed_question = self.process_question_images(q_data, images_base_path)
            
            # Récupérer ou créer la catégorie
            category_name = processed_question.get('category', 'General')
            category = self.get_or_create_category(tech, category_name)
            
            # Créer la question
            question = Question(
                technology_id=tech.id,
                category_id=category.id,
                question_text=processed_question['question_text'],
                options=json.dumps(processed_question['options'], ensure_ascii=False),
                correct_answer=processed_question['correct_answer'],
                explanation=processed_question.get('explanation', ''),
                difficulty=processed_question.get('difficulty', 1),
                images=processed_question.get('images'),
                tags=json.dumps(processed_question.get('tags', []), ensure_ascii=False),
                is_active=True
            )
            
            self.db.add(question)
            imported_count += 1
        
        self.db.commit()
        return imported_count, skipped_count
    
    def import_from_file(self, tech_name: str, file_path: str, images_dir: Optional[str] = None,
                        display_name: str = None, icon: str = "💻", color: str = "#007bff") -> Dict:
        """Importer depuis un fichier JSON"""
        print(f"\n🚀 Import de {tech_name} depuis {file_path}")
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Fichier non trouvé: {file_path}")
        
        # Charger les données JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Support de différents formats
        if isinstance(data, list):
            questions_data = data
        elif isinstance(data, dict) and 'questions' in data:
            questions_data = data['questions']
            # Extraire les métadonnées du fichier si disponibles
            if not display_name and 'technology' in data:
                display_name = data['technology']
        else:
            raise ValueError(f"Format JSON non reconnu dans {file_path}")
        
        # Créer/récupérer la technologie
        tech = self.get_or_create_technology(tech_name, display_name, icon, color)
        
        # Importer les questions
        imported, skipped = self.import_questions_from_data(tech, questions_data, images_dir)
        
        result = {
            'technology': tech_name,
            'imported': imported,
            'skipped': skipped,
            'total': len(questions_data)
        }
        
        print(f"✅ {tech_name}: {imported} questions importées, {skipped} ignorées")
        return result
    
    def batch_import(self, custom_files: Dict[str, str] = None) -> Dict:
        """Import batch de toutes les technologies"""
        print("🚀 Import batch de toutes les technologies\n")
        
        files_to_import = custom_files or DEFAULT_BATCH_FILES
        script_dir = Path(__file__).parent
        results = {}
        total_imported = 0
        
        for tech_name, filename in files_to_import.items():
            file_path = script_dir / filename
            
            if file_path.exists():
                try:
                    result = self.import_from_file(tech_name, str(file_path))
                    results[tech_name] = result
                    total_imported += result['imported']
                except Exception as e:
                    print(f"❌ Erreur pour {tech_name}: {e}")
                    results[tech_name] = {'error': str(e)}
            else:
                print(f"⚠️  Fichier ignoré (non trouvé): {filename}")
                results[tech_name] = {'error': 'Fichier non trouvé'}
        
        print(f"\n🎉 Import batch terminé: {total_imported} questions importées au total")
        return results
    
    def show_statistics(self):
        """Afficher les statistiques de la base"""
        print("\n📊 Statistiques de la base de données:")
        
        total_tech = self.db.query(Technology).filter(Technology.is_active == True).count()
        total_questions = self.db.query(Question).filter(Question.is_active == True).count()
        
        print(f"   - Technologies actives: {total_tech}")
        print(f"   - Questions totales: {total_questions}")
        
        print("\n📈 Répartition par technologie:")
        technologies = self.db.query(Technology).filter(Technology.is_active == True).all()
        for tech in technologies:
            question_count = self.db.query(Question).filter(
                Question.technology_id == tech.id,
                Question.is_active == True
            ).count()
            print(f"   - {tech.display_name}: {question_count} questions")

def main():
    """Fonction principale avec gestion des arguments"""
    parser = argparse.ArgumentParser(description='Script unifié d\'import de questions')
    
    # Arguments principaux
    parser.add_argument('--tech', help='Nom de la technologie')
    parser.add_argument('--file', help='Fichier JSON à importer')
    parser.add_argument('--images-dir', help='Dossier contenant les images')
    
    # Métadonnées de technologie
    parser.add_argument('--display-name', help='Nom d\'affichage de la technologie')
    parser.add_argument('--icon', default='💻', help='Icône de la technologie')
    parser.add_argument('--color', default='#007bff', help='Couleur de la technologie')
    
    # Import batch
    parser.add_argument('--batch-import', action='store_true', help='Import de tous les fichiers par défaut')
    
    # Création de technologie
    parser.add_argument('--create-tech', help='Créer une nouvelle technologie vide')
    
    # Utilitaires
    parser.add_argument('--stats', action='store_true', help='Afficher les statistiques')
    
    args = parser.parse_args()
    
    # Créer les tables si nécessaires
    Base.metadata.create_all(bind=engine)
    
    # Créer une session de base de données
    db = SessionLocal()
    importer = UnifiedImporter(db)
    
    try:
        if args.stats:
            importer.show_statistics()
            
        elif args.create_tech:
            tech = importer.get_or_create_technology(
                args.create_tech, 
                args.display_name or args.create_tech,
                args.icon,
                args.color
            )
            print(f"✅ Technologie '{tech.display_name}' créée/mise à jour")
            
        elif args.batch_import:
            results = importer.batch_import()
            
        elif args.tech and args.file:
            result = importer.import_from_file(
                args.tech, 
                args.file, 
                args.images_dir,
                args.display_name,
                args.icon,
                args.color
            )
            
        else:
            parser.print_help()
            print("\nExemples d'utilisation:")
            print("  python unified_import.py --tech 'JavaScript' --file javascript_questions.json")
            print("  python unified_import.py --batch-import")
            print("  python unified_import.py --stats")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == '__main__':
    main()