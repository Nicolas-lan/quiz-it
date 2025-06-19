#!/usr/bin/env python3
import json
import sys
import os
sys.path.insert(0, '/app')

from app.core.db import SessionLocal
from app.models.database_models import Technology, Category, Question

def force_import():
    """Force import of technologies and questions"""
    db = SessionLocal()
    
    try:
        print("🚀 Force importing technologies and questions...")
        
        # Create technologies first
        technologies_to_create = [
            {"name": "Apache Spark", "display_name": "Apache Spark", "description": "Questions about Apache Spark", "icon": "💻", "color": "#E25A1C"},
            {"name": "Docker", "display_name": "Docker", "description": "Questions about Docker", "icon": "🐳", "color": "#2496ED"},
            {"name": "Git", "display_name": "Git", "description": "Questions about Git", "icon": "📂", "color": "#F05032"}
        ]
        
        for tech_data in technologies_to_create:
            existing = db.query(Technology).filter(Technology.name == tech_data["name"]).first()
            if not existing:
                tech = Technology(**tech_data)
                db.add(tech)
                db.commit()
                db.refresh(tech)
                print(f"✅ Created technology: {tech_data['name']}")
            else:
                print(f"ℹ️  Technology already exists: {tech_data['name']}")
        
        # Now import questions for each technology
        tech_files = [
            ("Apache Spark", "/app/scripts/spark_mixed_questions.json"),
            ("Docker", "/app/scripts/docker_mixed_questions.json"),
            ("Git", "/app/scripts/git_mixed_questions.json")
        ]
        
        for tech_name, file_path in tech_files:
            if os.path.exists(file_path):
                import_questions_for_tech(db, tech_name, file_path)
            else:
                print(f"⚠️  File not found: {file_path}")
        
        # Show final stats
        print("\n📊 Final Statistics:")
        technologies = db.query(Technology).all()
        for tech in technologies:
            count = db.query(Question).filter(Question.technology_id == tech.id).count()
            print(f"  - {tech.display_name}: {count} questions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

def import_questions_for_tech(db, tech_name, file_path):
    """Import questions for a specific technology"""
    print(f"\n🔄 Importing questions for {tech_name}...")
    
    # Get technology
    technology = db.query(Technology).filter(Technology.name == tech_name).first()
    if not technology:
        print(f"❌ Technology not found: {tech_name}")
        return
    
    # Load questions
    with open(file_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    imported_count = 0
    skipped_count = 0
    
    for q_data in questions_data:
        # Check if question exists
        existing = db.query(Question).filter(
            Question.question_text == q_data['question_text'],
            Question.technology_id == technology.id
        ).first()
        
        if existing:
            skipped_count += 1
            continue
        
        # Get or create category
        category_name = q_data.get('category', 'General')
        category = db.query(Category).filter(
            Category.name == category_name,
            Category.technology_id == technology.id
        ).first()
        
        if not category:
            # Create unique category name
            unique_cat_name = f"{category_name}_{tech_name}_{technology.id}"
            existing_cat = db.query(Category).filter(Category.name == unique_cat_name).first()
            
            if not existing_cat:
                category = Category(
                    name=unique_cat_name,
                    technology_id=technology.id,
                    description=f"{category_name} questions for {tech_name}"
                )
                db.add(category)
                db.commit()
                db.refresh(category)
            else:
                category = existing_cat
        
        # Handle images
        images_json = None
        if 'code_image' in q_data:
            images_json = json.dumps({"code": q_data['code_image']})
        elif 'diagram_image' in q_data:
            images_json = json.dumps({"diagram": q_data['diagram_image']})
        elif 'screenshot_image' in q_data:
            images_json = json.dumps({"screenshot": q_data['screenshot_image']})
        elif 'question_image' in q_data:
            images_json = json.dumps({"question": q_data['question_image']})
        elif 'images' in q_data:
            images_json = json.dumps(q_data['images'])
        
        # Create question
        try:
            question = Question(
                question_text=q_data['question_text'],
                options=json.dumps(q_data['options']),
                correct_answer=q_data['correct_answer'],
                explanation=q_data.get('explanation', ''),
                difficulty=q_data.get('difficulty', 1),
                images=images_json,
                tags=json.dumps(q_data.get('tags', [])),
                technology_id=technology.id,
                category_id=category.id
            )
            
            db.add(question)
            imported_count += 1
            
        except Exception as e:
            print(f"❌ Error creating question: {e}")
            db.rollback()
            continue
    
    try:
        db.commit()
        print(f"✅ {tech_name}: {imported_count} imported, {skipped_count} skipped")
    except Exception as e:
        print(f"❌ Error committing questions for {tech_name}: {e}")
        db.rollback()

if __name__ == '__main__':
    force_import()