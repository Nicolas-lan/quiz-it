from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class SparkQuestion(Base):
    __tablename__ = "spark_questions"

    id = Column(Integer, primary_key=True, index=True)
    technology = Column(String, index=True)  # Ajouté pour filtrer par techno
    question_text = Column(String, index=True)
    options = Column(JSON)  # Liste des options de réponse
    correct_answer = Column(String)
    explanation = Column(String)
    category = Column(String, index=True)  # Par exemple: "RDD", "DataFrame", "Spark SQL", etc.
    difficulty = Column(Integer)  # 1-5
    tags = Column(JSON)  # Tags pour faciliter la recherche 