FROM python:3.9-slim

WORKDIR /app

# Créer le répertoire data avec les bonnes permissions
RUN mkdir -p /app/data && chmod 777 /app/data

# Copier les fichiers de configuration
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY app/ ./app/

# Créer le fichier __init__.py s'il n'existe pas
RUN touch app/__init__.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 