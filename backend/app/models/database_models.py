from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    quiz_sessions = relationship("QuizSession", back_populates="user")

class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)  # spark, git, docker
    display_name = Column(String(100), nullable=False)  # Apache Spark, Git, Docker
    description = Column(Text)
    icon = Column(String(10))  # emoji ou classe CSS
    color = Column(String(20))  # classe CSS couleur
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    questions = relationship("Question", back_populates="technology")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    technology_id = Column(Integer, ForeignKey("technologies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    technology = relationship("Technology")
    questions = relationship("Question", back_populates="category")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    technology_id = Column(Integer, ForeignKey("technologies.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # Liste des options
    correct_answer = Column(String(500), nullable=False)
    explanation = Column(Text)
    difficulty = Column(Integer, default=1)  # 1-5
    images = Column(JSON)  # Stockage des images
    tags = Column(JSON)  # Liste des tags
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relations
    technology = relationship("Technology", back_populates="questions")
    category = relationship("Category", back_populates="questions")
    quiz_answers = relationship("QuizAnswer", back_populates="question")

class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    technology_id = Column(Integer, ForeignKey("technologies.id"), nullable=False)
    status = Column(String(20), default="in_progress")  # in_progress, completed, abandoned
    total_questions = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    score_percentage = Column(Integer, default=0)
    time_spent_seconds = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    # Relations
    user = relationship("User", back_populates="quiz_sessions")
    technology = relationship("Technology")
    quiz_answers = relationship("QuizAnswer", back_populates="quiz_session")

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    quiz_session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(String(500), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_spent_seconds = Column(Integer, default=0)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    quiz_session = relationship("QuizSession", back_populates="quiz_answers")
    question = relationship("Question", back_populates="quiz_answers")