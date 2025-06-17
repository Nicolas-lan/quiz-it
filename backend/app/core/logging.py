import logging
import sys
from datetime import datetime
from pathlib import Path
import json
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """Formatter JSON pour logs structurés"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Ajouter des infos contextuelles si disponibles
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'technology'):
            log_entry['technology'] = record.technology
        if hasattr(record, 'duration'):
            log_entry['duration_ms'] = record.duration
            
        # Ajouter exception si présente
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry, ensure_ascii=False)

def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """Configure le système de logging"""
    
    # Créer le dossier logs si nécessaire
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configuration du niveau de log
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Formatter pour console (plus lisible)
    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Formatter JSON pour fichier
    json_formatter = JSONFormatter()
    
    # Handler console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    
    # Handler fichier
    if not log_file:
        log_file = log_dir / f"quiz_app_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Tout dans le fichier
    file_handler.setFormatter(json_formatter)
    
    # Configuration root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Réduire le niveau des loggers tiers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    # Logger de démarrage
    logger = logging.getLogger("quiz_app.startup")
    logger.info("Logging configuré", extra={
        "log_level": log_level,
        "log_file": str(log_file),
        "console_level": level
    })

def get_logger(name: str) -> logging.Logger:
    """Récupère un logger avec le nom spécifié"""
    return logging.getLogger(f"quiz_app.{name}")

# Loggers spécialisés pour différents modules
def get_api_logger() -> logging.Logger:
    return get_logger("api")

def get_db_logger() -> logging.Logger:
    return get_logger("database")

def get_quiz_logger() -> logging.Logger:
    return get_logger("quiz")

def get_auth_logger() -> logging.Logger:
    return get_logger("auth")