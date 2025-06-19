#!/usr/bin/env python3
import sys
sys.path.insert(0, '/app')

from app.core.db import SessionLocal
from app.models.database_models import Technology, Question

def cleanup_database():
    """Remove duplicate technologies without questions"""
    db = SessionLocal()
    
    try:
        print("🧹 Cleaning up duplicate technologies...")
        
        # Get technologies with 0 questions
        empty_techs = []
        all_techs = db.query(Technology).all()
        
        for tech in all_techs:
            question_count = db.query(Question).filter(Question.technology_id == tech.id).count()
            if question_count == 0:
                empty_techs.append(tech)
                print(f"📋 Found empty technology: ID {tech.id}, Name: '{tech.name}' (0 questions)")
        
        # Delete empty technologies
        for tech in empty_techs:
            print(f"🗑️  Deleting technology: ID {tech.id}, Name: '{tech.name}'")
            db.delete(tech)
        
        db.commit()
        print(f"✅ Deleted {len(empty_techs)} empty technologies")
        
        # Show final result
        print("\n📊 Final technologies:")
        remaining_techs = db.query(Technology).all()
        for tech in remaining_techs:
            question_count = db.query(Question).filter(Question.technology_id == tech.id).count()
            print(f"  - ID: {tech.id}, Name: '{tech.name}', Display: '{tech.display_name}', Questions: {question_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    cleanup_database()