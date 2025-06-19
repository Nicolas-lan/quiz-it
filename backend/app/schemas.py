from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# ============================================================================
# User Schemas
# ============================================================================

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=100)

class User(UserBase):
    id: int
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ============================================================================
# Authentication Schemas
# ============================================================================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# ============================================================================
# Technology Schemas
# ============================================================================

class TechnologyBase(BaseModel):
    name: str = Field(..., max_length=50)
    display_name: str = Field(..., max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=10)
    color: Optional[str] = Field(None, max_length=20)

class TechnologyCreate(TechnologyBase):
    pass

class TechnologyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    display_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=10)
    color: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None

class Technology(TechnologyBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================================================
# Category Schemas
# ============================================================================

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    technology_id: int

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    technology_id: Optional[int] = None

class Category(CategoryBase):
    id: int
    created_at: datetime
    technology: Optional[Technology] = None

    class Config:
        from_attributes = True

# ============================================================================
# Question Schemas
# ============================================================================

class QuestionBase(BaseModel):
    technology_id: int
    category_id: int
    question_text: str
    options: List[str] = Field(..., min_items=2, max_items=6)
    correct_answer: str = Field(..., max_length=500)
    explanation: Optional[str] = None
    difficulty: int = Field(default=1, ge=1, le=5)
    images: Optional[dict] = None
    tags: Optional[List[str]] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    technology_id: Optional[int] = None
    category_id: Optional[int] = None
    question_text: Optional[str] = None
    options: Optional[List[str]] = Field(None, min_items=2, max_items=6)
    correct_answer: Optional[str] = Field(None, max_length=500)
    explanation: Optional[str] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    images: Optional[dict] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None

class Question(QuestionBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    technology: Optional[Technology] = None
    category: Optional[Category] = None

    class Config:
        from_attributes = True

# ============================================================================
# Quiz Session Schemas
# ============================================================================

class QuizSessionBase(BaseModel):
    technology_id: int

class QuizSessionCreate(QuizSessionBase):
    pass

class QuizSessionUpdate(BaseModel):
    status: Optional[str] = Field(None, regex="^(in_progress|completed|abandoned)$")
    total_questions: Optional[int] = Field(None, ge=0)
    correct_answers: Optional[int] = Field(None, ge=0)
    score_percentage: Optional[int] = Field(None, ge=0, le=100)
    time_spent_seconds: Optional[int] = Field(None, ge=0)

class QuizSession(QuizSessionBase):
    id: int
    user_id: int
    status: str = "in_progress"
    total_questions: int = 0
    correct_answers: int = 0
    score_percentage: int = 0
    time_spent_seconds: int = 0
    started_at: datetime
    completed_at: Optional[datetime] = None
    technology: Optional[Technology] = None

    class Config:
        from_attributes = True

# ============================================================================
# Quiz Answer Schemas
# ============================================================================

class QuizAnswerBase(BaseModel):
    quiz_session_id: int
    question_id: int
    user_answer: str = Field(..., max_length=500)
    time_spent_seconds: int = Field(default=0, ge=0)

class QuizAnswerCreate(QuizAnswerBase):
    pass

class QuizAnswer(QuizAnswerBase):
    id: int
    is_correct: bool
    answered_at: datetime
    question: Optional[Question] = None

    class Config:
        from_attributes = True

# ============================================================================
# Response Schemas
# ============================================================================

class QuestionForQuiz(BaseModel):
    """Schema pour les questions dans un quiz (sans la réponse correcte)"""
    id: int
    question_text: str
    options: List[str]
    difficulty: int
    images: Optional[dict] = None
    tags: Optional[List[str]] = None

    class Config:
        from_attributes = True

class QuizResult(BaseModel):
    """Schema pour les résultats d'un quiz"""
    quiz_session_id: int
    total_questions: int
    correct_answers: int
    score_percentage: int
    time_spent_seconds: int
    answers: List[QuizAnswer]

class QuestionPublic(BaseModel):
    """Schema pour les questions publiques (sans la réponse correcte)"""
    id: int
    technology_id: int
    category_id: int
    question_text: str
    options: List[str]
    explanation: Optional[str] = None
    difficulty: int
    images: Optional[dict] = None
    tags: Optional[List[str]] = None
    technology: Optional[Technology] = None
    category: Optional[Category] = None

    class Config:
        from_attributes = True

# ============================================================================
# Dashboard Schemas
# ============================================================================

class QuizSessionSummary(BaseModel):
    """Résumé d'une session de quiz pour l'historique"""
    id: int
    technology_name: str
    score_percentage: int
    total_questions: int
    correct_answers: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    time_spent_seconds: int
    
    class Config:
        from_attributes = True

class UserStatistics(BaseModel):
    """Statistiques détaillées d'un utilisateur"""
    total_quizzes: int
    average_score: float
    best_score: int
    total_time_spent: int  # en secondes
    quizzes_by_technology: dict  # {"technology_name": count}
    scores_by_technology: dict   # {"technology_name": average_score}
    recent_activity: List[QuizSessionSummary]
    
class ProgressData(BaseModel):
    """Données pour les graphiques de progression"""
    dates: List[str]  # dates au format YYYY-MM-DD
    scores: List[float]  # scores moyens par date
    quiz_counts: List[int]  # nombre de quiz par date
    
class UserDashboard(BaseModel):
    """Dashboard complet de l'utilisateur"""
    user: User
    statistics: UserStatistics
    progress_data: ProgressData
    quiz_history: List[QuizSessionSummary]
    
    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    """Schema pour les statistiques du dashboard admin"""
    total_users: int
    total_questions: int
    total_quiz_sessions: int
    average_score: float
    technologies: List[Technology]