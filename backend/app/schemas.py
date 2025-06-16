from pydantic import BaseModel
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

    class Config:
        orm_mode = True 