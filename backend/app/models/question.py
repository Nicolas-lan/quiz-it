from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    correct_answer = Column(String)
    explanation = Column(String)
    certification = Column(String, index=True)
    category = Column(String, index=True)
    difficulty = Column(Integer)  # 1-5 