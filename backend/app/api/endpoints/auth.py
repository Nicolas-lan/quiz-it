from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.db import get_db
from ...core.auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ...models.database_models import User
from ...schemas import (
    Token, 
    User as UserSchema, 
    UserCreate, 
    UserUpdate,
    LoginRequest
)
import logging

router = APIRouter()
logger = logging.getLogger("quiz_app.auth")

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Créer un nouveau compte utilisateur"""
    
    logger.info(f"Tentative de création de compte pour: {user.username}")
    
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        if existing_user.username == user.username:
            logger.warning(f"Tentative de création avec username existant: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce nom d'utilisateur est déjà pris"
            )
        if existing_user.email == user.email:
            logger.warning(f"Tentative de création avec email existant: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cette adresse email est déjà utilisée"
            )
    
    # Créer le nouvel utilisateur
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"✅ Compte créé avec succès pour: {user.username} (ID: {db_user.id})")
    return db_user

@router.post("/login", response_model=Token)
def login_user(user_credentials: LoginRequest, db: Session = Depends(get_db)):
    """Connexion utilisateur avec username/email et mot de passe"""
    
    logger.info(f"Tentative de connexion pour: {user_credentials.username}")
    
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        logger.warning(f"❌ Échec de connexion pour: {user_credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur/email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    logger.info(f"✅ Connexion réussie pour: {user.username} (ID: {user.id})")
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.post("/login/form", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Connexion OAuth2 standard (pour la documentation FastAPI)"""
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserSchema)
def read_current_user(current_user: User = Depends(get_current_active_user)):
    """Obtenir les informations de l'utilisateur connecté"""
    logger.info(f"Récupération du profil pour: {current_user.username}")
    return current_user

@router.put("/me", response_model=UserSchema)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour le profil de l'utilisateur connecté"""
    
    logger.info(f"Mise à jour du profil pour: {current_user.username}")
    
    # Vérifier si l'email est déjà utilisé par un autre utilisateur
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cette adresse email est déjà utilisée"
            )
    
    # Mettre à jour les champs
    update_data = user_update.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    logger.info(f"✅ Profil mis à jour pour: {current_user.username}")
    return current_user

@router.post("/logout")
def logout_user(current_user: User = Depends(get_current_active_user)):
    """Déconnexion utilisateur (côté client seulement)"""
    logger.info(f"Déconnexion pour: {current_user.username}")
    return {"message": "Déconnexion réussie"}

@router.get("/validate-token")
def validate_token(current_user: User = Depends(get_current_active_user)):
    """Valider un token JWT"""
    return {
        "valid": True,
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    }