import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from ..models.database_models import User

# Configuration JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24h par défaut

# Configuration bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# Security scheme pour FastAPI
security = HTTPBearer()

class AuthError(HTTPException):
    """Exception personnalisée pour les erreurs d'authentification"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hasher un mot de passe"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Créer un token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Vérifier et décoder un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthError("Token invalide")
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError("Token expiré")
    except jwt.JWTError:
        raise AuthError("Token invalide")

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authentifier un utilisateur"""
    user = db.query(User).filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    
    return user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Obtenir l'utilisateur actuel depuis le token"""
    token = credentials.credentials
    payload = verify_token(token)
    
    username: str = payload.get("sub")
    if username is None:
        raise AuthError("Token invalide")
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise AuthError("Utilisateur non trouvé")
    
    if not user.is_active:
        raise AuthError("Utilisateur inactif")
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtenir l'utilisateur actuel actif"""
    if not current_user.is_active:
        raise AuthError("Utilisateur inactif")
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtenir l'utilisateur actuel s'il est admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissions administrateur requises"
        )
    return current_user

# Dependency optionnel (utilisateur peut ne pas être connecté)
def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Obtenir l'utilisateur actuel si connecté, sinon None"""
    if not credentials:
        return None
    
    try:
        return get_current_user(credentials, db)
    except AuthError:
        return None