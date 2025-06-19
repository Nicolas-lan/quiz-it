# Utiliser Python 3.11 pour éviter les problèmes de compatibilité
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Variables d'environnement pour optimiser Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements.txt et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Créer les dossiers pour les données et logs
RUN mkdir -p /app/data /app/logs

# Copier le code de l'application
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Point de santé pour Docker
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Commande par défaut
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]