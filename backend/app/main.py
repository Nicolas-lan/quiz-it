from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import get_db, engine, SessionLocal
from .initial_data import init_db
from sqlalchemy.sql import func

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Spark Quiz API")

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (en dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    if db.query(models.SparkQuestion).count() == 0:
        init_db(db)
    db.close()

@app.get("/questions/", response_model=List[schemas.SparkQuestion])
def get_questions(
    technology: str = None,
    category: str = None,
    difficulty: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.SparkQuestion)
    if technology:
        query = query.filter(models.SparkQuestion.technology == technology)
    if category:
        query = query.filter(models.SparkQuestion.category == category)
    if difficulty:
        query = query.filter(models.SparkQuestion.difficulty == difficulty)
    return query.all()

@app.get("/questions/{question_id}", response_model=schemas.SparkQuestion)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(models.SparkQuestion).filter(models.SparkQuestion.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.post("/questions/", response_model=schemas.SparkQuestion)
def create_question(question: schemas.SparkQuestionCreate, db: Session = Depends(get_db)):
    db_question = models.SparkQuestion(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Route pour obtenir une question aléatoire
@app.get("/questions/random/", response_model=schemas.SparkQuestion)
def get_random_question(
    technology: str = None,
    category: str = None,
    difficulty: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.SparkQuestion)
    if technology:
        query = query.filter(models.SparkQuestion.technology == technology)
    if category:
        query = query.filter(models.SparkQuestion.category == category)
    if difficulty:
        query = query.filter(models.SparkQuestion.difficulty == difficulty)
    return query.order_by(func.random()).first() 