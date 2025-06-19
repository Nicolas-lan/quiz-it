#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, '/app')

from app.core.db import SessionLocal
from app.models.database_models import Technology, Category, Question

def import_questions(tech_name: str, json_file: str):
    """Import questions from JSON file"""
    db = SessionLocal()
    
    try:
        print(f"🚀 Importing {tech_name} questions...")
        
        # Get or create technology
        technology = db.query(Technology).filter(Technology.name == tech_name).first()
        if not technology:
            technology = Technology(
                name=tech_name, 
                display_name=tech_name,
                description=f"Questions about {tech_name}",
                icon="💻",
                color="#007bff"
            )
            db.add(technology)
            db.commit()
            db.refresh(technology)
            print(f"✅ Created technology: {tech_name}")
        
        # Load questions
        with open(json_file, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        imported_count = 0
        skipped_count = 0
        
        for q_data in questions_data:
            # Check if question exists
            existing = db.query(Question).filter(
                Question.question_text == q_data['question_text']
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
                # Try to find existing category with same name (due to unique constraint)
                existing_category = db.query(Category).filter(Category.name == category_name).first()
                if existing_category:
                    category = existing_category
                else:
                    try:
                        category = Category(
                            name=category_name,
                            technology_id=technology.id,
                            description=f"{category_name} questions for {tech_name}"
                        )
                        db.add(category)
                        db.commit()
                        db.refresh(category)
                    except Exception as e:
                        db.rollback()
                        # Use existing category if unique constraint fails
                        category = db.query(Category).filter(Category.name == category_name).first()
            
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
        
        db.commit()
        print(f"✅ {tech_name}: {imported_count} imported, {skipped_count} skipped")
        
        # Show total count
        total = db.query(Question).filter(Question.technology_id == technology.id).count()
        print(f"📊 Total {tech_name} questions: {total}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python quick_import.py <technology> <json_file>")
        sys.exit(1)
    
    tech_name = sys.argv[1]
    json_file = sys.argv[2]
    
    import_questions(tech_name, json_file)