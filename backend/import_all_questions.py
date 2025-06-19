import json
import sys
import asyncio
from pathlib import Path
sys.path.append('/app')

from app.core.db import get_db
from app.models.database_models import Technology, Category, Question
from sqlalchemy.orm import Session

async def import_questions_from_file(db: Session, tech_name: str, file_path: str):
    print(f"\n🚀 Importing questions for {tech_name}...")
    
    # Get or create technology
    technology = db.query(Technology).filter(Technology.name == tech_name).first()
    if not technology:
        technology = Technology(name=tech_name, description=f"Questions about {tech_name}")
        db.add(technology)
        db.commit()
        db.refresh(technology)
        print(f"✅ Created technology: {tech_name}")
    
    # Load questions from JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    
    imported_count = 0
    skipped_count = 0
    
    for q_data in questions_data:
        # Check if question already exists
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
            category = Category(
                name=category_name,
                technology_id=technology.id,
                description=f"{category_name} questions for {tech_name}"
            )
            db.add(category)
            db.commit()
            db.refresh(category)
        
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
    print(f"✅ {tech_name}: {imported_count} questions imported, {skipped_count} skipped")
    return imported_count

def main():
    from app.core.db import SessionLocal
    db = SessionLocal()
    
    try:
        total_imported = 0
        
        # Import Spark questions
        spark_file = '/app/scripts/spark_mixed_questions.json'
        if Path(spark_file).exists():
            count = asyncio.run(import_questions_from_file(db, 'Apache Spark', spark_file))
            total_imported += count
        
        # Import Git questions  
        git_file = '/app/scripts/git_mixed_questions.json'
        if Path(git_file).exists():
            count = asyncio.run(import_questions_from_file(db, 'Git', git_file))
            total_imported += count
        
        # Import Docker questions
        docker_file = '/app/scripts/docker_mixed_questions.json'
        if Path(docker_file).exists():
            count = asyncio.run(import_questions_from_file(db, 'Docker', docker_file))
            total_imported += count
        
        print(f"\n🎉 Total imported: {total_imported} questions across all technologies!")
        
        # Show summary
        technologies = db.query(Technology).all()
        for tech in technologies:
            question_count = db.query(Question).filter(Question.technology_id == tech.id).count()
            print(f"📊 {tech.name}: {question_count} questions total")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    main()