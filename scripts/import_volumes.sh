#!/bin/bash
# Script pour importer les volumes Docker

echo "📥 Import des volumes Docker..."

# Vérifier que les fichiers existent
if [ ! -f "data/dumps/postgres_dump.sql" ]; then
    echo "❌ Fichier postgres_dump.sql non trouvé"
    exit 1
fi

# 1. Import du dump PostgreSQL
echo "📊 Import de la base PostgreSQL..."
docker-compose exec -T postgres psql -U quiz_user -d quiz_db < data/dumps/postgres_dump.sql
echo "✅ Base PostgreSQL restaurée"

# 2. Import du volume PostgreSQL complet (si besoin de restaurer complètement)
# echo "💾 Restauration du volume PostgreSQL..."
# docker run --rm \
#   -v quiz-postgres-data:/volume \
#   -v $(pwd)/data/dumps:/backup \
#   alpine sh -c "cd /volume && tar xzf /backup/postgres_volume.tar.gz"

# 3. Import du volume Redis (si nécessaire)
# echo "🔴 Restauration du volume Redis..."
# docker run --rm \
#   -v quiz-redis-data:/volume \
#   -v $(pwd)/data/dumps:/backup \
#   alpine sh -c "cd /volume && tar xzf /backup/redis_volume.tar.gz"

echo "🎉 Import terminé !"