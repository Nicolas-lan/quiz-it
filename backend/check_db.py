#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, '/app')

from app.core.db import SessionLocal
from app.models.database_models import Technology, Category, Question

def check_database():
    """Check what's in the database"""
    db = SessionLocal()
    
    try:
        print("🔍 Checking database content...")
        
        # Check technologies
        technologies = db.query(Technology).all()
        print(f"\n📊 Technologies ({len(technologies)}):")
        for tech in technologies:
            print(f"  - ID: {tech.id}, Name: '{tech.name}', Display: '{tech.display_name}', Active: {tech.is_active}")
        
        # Check categories
        categories = db.query(Category).all()
        print(f"\n📂 Categories ({len(categories)}):")
        for cat in categories:
            print(f"  - ID: {cat.id}, Name: '{cat.name}', Tech ID: {cat.technology_id}")
        
        # Check questions
        questions = db.query(Question).all()
        print(f"\n❓ Questions ({len(questions)}):")
        for q in questions:
            print(f"  - ID: {q.id}, Tech ID: {q.technology_id}, Cat ID: {q.category_id}")
            print(f"    Text: '{q.question_text[:50]}...'")
        
        # Questions per technology
        print(f"\n📈 Questions per technology:")
        for tech in technologies:
            count = db.query(Question).filter(Question.technology_id == tech.id).count()
            print(f"  - {tech.display_name or tech.name}: {count} questions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    check_database()