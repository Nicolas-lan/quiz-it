import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .logging import get_api_logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware pour logger toutes les requêtes HTTP"""
    
    def __init__(self, app):
        super().__init__(app)
        self.logger = get_api_logger()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Générer un ID unique pour la requête
        request_id = str(uuid.uuid4())[:8]
        
        # Informations de début de requête
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Log de début de requête
        self.logger.info(
            f"Début requête {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "query_params": str(request.query_params),
                "client_ip": client_ip,
                "user_agent": user_agent
            }
        )
        
        # Ajouter request_id au contexte de la requête
        request.state.request_id = request_id
        
        try:
            # Traiter la requête
            response = await call_next(request)
            
            # Calculer le temps de traitement
            duration = (time.time() - start_time) * 1000  # en ms
            
            # Log de fin de requête
            self.logger.info(
                f"Fin requête {request.method} {request.url.path} - {response.status_code}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration": round(duration, 2),
                    "response_size": response.headers.get("content-length", "unknown")
                }
            )
            
            # Ajouter l'ID de requête dans les headers de réponse
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Log des erreurs
            duration = (time.time() - start_time) * 1000
            
            self.logger.error(
                f"Erreur requête {request.method} {request.url.path}",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration": round(duration, 2),
                    "error": str(e),
                    "error_type": type(e).__name__
                },
                exc_info=True
            )
            
            # Re-lancer l'exception
            raise

class DatabaseLoggingMiddleware:
    """Middleware pour logger les opérations base de données"""
    
    def __init__(self):
        self.logger = get_api_logger()
    
    def log_query_start(self, query: str, params: dict = None):
        """Log le début d'une requête SQL"""
        self.logger.debug(
            "Exécution requête SQL",
            extra={
                "query": query[:200] + "..." if len(query) > 200 else query,
                "params": params
            }
        )
    
    def log_query_end(self, duration: float, rows_affected: int = None):
        """Log la fin d'une requête SQL"""
        self.logger.debug(
            "Requête SQL terminée",
            extra={
                "duration": round(duration * 1000, 2),  # en ms
                "rows_affected": rows_affected
            }
        )