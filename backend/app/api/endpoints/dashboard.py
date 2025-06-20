from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from ...core.db import get_db
from ...core.auth import get_current_active_user
from ...models.database_models import User, QuizSession, Technology, Question
from ...schemas import (
    UserDashboard,
    UserStatistics,
    ProgressData,
    QuizSessionSummary
)

router = APIRouter()

@router.get("/me")
def get_user_dashboard(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtenir le dashboard complet de l'utilisateur connecté"""
    
    # Récupérer les statistiques générales
    statistics = get_user_statistics(current_user.id, db)
    
    # Récupérer les données de progression
    progress_data = get_progress_data(current_user.id, db)
    
    # Récupérer l'historique complet des quiz
    quiz_history = get_quiz_history(current_user.id, db, limit=50)
    
    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_active": current_user.is_active,
            "is_admin": current_user.is_admin,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None
        },
        "statistics": statistics.dict(),
        "progress_data": progress_data.dict(),
        "quiz_history": [q.dict() for q in quiz_history]
    }

@router.get("/stats", response_model=UserStatistics)
def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtenir les statistiques de l'utilisateur"""
    return get_user_statistics(current_user.id, db)

@router.get("/history", response_model=List[QuizSessionSummary])
def get_user_quiz_history(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtenir l'historique des quiz de l'utilisateur"""
    return get_quiz_history(current_user.id, db, limit)

@router.get("/progress", response_model=ProgressData)
def get_user_progress(
    days: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtenir les données de progression sur les X derniers jours"""
    return get_progress_data(current_user.id, db, days)

# Fonctions utilitaires

def get_user_statistics(user_id: int, db: Session) -> UserStatistics:
    """Calculer les statistiques d'un utilisateur"""
    
    # Sessions terminées avec technologie
    completed_sessions = db.query(QuizSession).join(Technology).filter(
        QuizSession.user_id == user_id,
        QuizSession.completed_at.isnot(None)
    ).all()
    
    if not completed_sessions:
        return UserStatistics(
            total_quizzes=0,
            average_score=0.0,
            best_score=0,
            total_time_spent=0,
            quizzes_by_technology={},
            scores_by_technology={},
            recent_activity=[]
        )
    
    # Statistiques de base
    total_quizzes = len(completed_sessions)
    scores = [session.score_percentage for session in completed_sessions]
    average_score = sum(scores) / len(scores)
    best_score = max(scores)
    total_time_spent = sum(session.time_spent_seconds or 0 for session in completed_sessions)
    
    # Statistiques par technologie
    tech_stats = {}
    tech_scores = {}
    
    for session in completed_sessions:
        tech_name = session.technology.name
        if tech_name not in tech_stats:
            tech_stats[tech_name] = 0
            tech_scores[tech_name] = []
        tech_stats[tech_name] += 1
        tech_scores[tech_name].append(session.score_percentage)
    
    # Moyenne des scores par technologie
    scores_by_technology = {
        tech: sum(scores) / len(scores) 
        for tech, scores in tech_scores.items()
    }
    
    # Activité récente (5 derniers quiz)
    recent_sessions = sorted(completed_sessions, key=lambda x: x.completed_at, reverse=True)[:5]
    recent_activity = [
        QuizSessionSummary(
            id=session.id,
            technology_name=session.technology.name,
            score_percentage=session.score_percentage,
            total_questions=session.total_questions,
            correct_answers=session.correct_answers,
            started_at=session.started_at,
            completed_at=session.completed_at,
            time_spent_seconds=session.time_spent_seconds or 0
        )
        for session in recent_sessions
    ]
    
    return UserStatistics(
        total_quizzes=total_quizzes,
        average_score=round(average_score, 1),
        best_score=best_score,
        total_time_spent=total_time_spent,
        quizzes_by_technology=tech_stats,
        scores_by_technology={k: round(v, 1) for k, v in scores_by_technology.items()},
        recent_activity=recent_activity
    )

def get_progress_data(user_id: int, db: Session, days: int = 30) -> ProgressData:
    """Obtenir les données de progression sur les X derniers jours"""
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Sessions dans la période
    sessions = db.query(QuizSession).filter(
        QuizSession.user_id == user_id,
        QuizSession.completed_at >= start_date,
        QuizSession.completed_at.isnot(None)
    ).order_by(QuizSession.completed_at).all()
    
    # Grouper par date
    daily_data = {}
    current_date = start_date.date()
    
    # Initialiser toutes les dates avec des valeurs vides
    while current_date <= end_date.date():
        daily_data[current_date.strftime('%Y-%m-%d')] = {
            'scores': [],
            'count': 0
        }
        current_date += timedelta(days=1)
    
    # Remplir avec les vraies données
    for session in sessions:
        date_str = session.completed_at.date().strftime('%Y-%m-%d')
        if date_str in daily_data:
            daily_data[date_str]['scores'].append(session.score_percentage)
            daily_data[date_str]['count'] += 1
    
    # Préparer les listes pour le graphique
    dates = sorted(daily_data.keys())
    scores = []
    quiz_counts = []
    
    for date in dates:
        data = daily_data[date]
        if data['scores']:
            avg_score = sum(data['scores']) / len(data['scores'])
        else:
            avg_score = 0.0
        
        scores.append(round(avg_score, 1))
        quiz_counts.append(data['count'])
    
    return ProgressData(
        dates=dates,
        scores=scores,
        quiz_counts=quiz_counts
    )

def get_quiz_history(user_id: int, db: Session, limit: int = 20) -> List[QuizSessionSummary]:
    """Obtenir l'historique des quiz avec détails"""
    
    sessions = db.query(QuizSession).join(Technology).filter(
        QuizSession.user_id == user_id,
        QuizSession.completed_at.isnot(None)
    ).order_by(desc(QuizSession.completed_at)).limit(limit).all()
    
    return [
        QuizSessionSummary(
            id=session.id,
            technology_name=session.technology.name,
            score_percentage=session.score_percentage,
            total_questions=session.total_questions,
            correct_answers=session.correct_answers,
            started_at=session.started_at,
            completed_at=session.completed_at,
            time_spent_seconds=session.time_spent_seconds or 0
        )
        for session in sessions
    ]