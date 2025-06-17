from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class SparkQuestionBase(BaseModel):
    technology: str
    question_text: str
    options: List[str]
    correct_answer: str
    explanation: str
    category: str
    difficulty: int
    tags: List[str]

class SparkQuestionCreate(SparkQuestionBase):
    pass

class SparkQuestion(SparkQuestionBase):
    id: int
    
    # Configuration pour Pydantic v2
    model_config = ConfigDict(from_attributes=True)