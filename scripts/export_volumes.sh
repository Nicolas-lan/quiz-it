#!/bin/bash
# Script pour exporter les volumes Docker

echo "🚀 Export des volumes Docker..."

# Créer le dossier de destination
mkdir -p data/dumps

# 1. Dump PostgreSQL avec toutes les données
echo "📊 Export de la base PostgreSQL..."
docker-compose exec -T postgres pg_dump -U quiz_user -d quiz_db --clean --if-exists > data/dumps/postgres_dump.sql
echo "✅ PostgreSQL dump créé: data/dumps/postgres_dump.sql"

# 2. Export du volume PostgreSQL complet (backup)
echo "💾 Export du volume PostgreSQL..."
docker run --rm \
  -v quiz-postgres-data:/volume \
  -v $(pwd)/data/dumps:/backup \
  alpine tar czf /backup/postgres_volume.tar.gz -C /volume .
echo "✅ Volume PostgreSQL exporté: data/dumps/postgres_volume.tar.gz"

# 3. Export du volume Redis (si nécessaire)
echo "🔴 Export du volume Redis..."
docker run --rm \
  -v quiz-redis-data:/volume \
  -v $(pwd)/data/dumps:/backup \
  alpine tar czf /backup/redis_volume.tar.gz -C /volume .
echo "✅ Volume Redis exporté: data/dumps/redis_volume.tar.gz"

echo "🎉 Export terminé ! Fichiers créés :"
ls -lh data/dumps/