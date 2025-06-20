# 📊 Données et volumes persistants

Ce dossier contient les exports des volumes Docker pour permettre le partage des données.

## 📁 Structure

```
data/
├── README.md           # Ce fichier
└── dumps/             # Exports des volumes
    ├── postgres_dump.sql      # Dump SQL de la base PostgreSQL
    ├── postgres_volume.tar.gz # Archive complète du volume PostgreSQL
    └── redis_volume.tar.gz    # Archive du volume Redis
```

## 🚀 Utilisation

### Export des données (créateur du projet)
```bash
# Exporter tous les volumes
./scripts/export_volumes.sh
```

### Import des données (nouveau développeur)
```bash
# 1. Démarrer les conteneurs
docker-compose up -d

# 2. Attendre que PostgreSQL soit prêt
docker-compose logs postgres

# 3. Importer les données
./scripts/import_volumes.sh
```

## 📋 Contenu de la base

- **Utilisateurs** : admin/admin (administrateur)
- **Technologies** : Apache Spark, Docker, Git
- **Questions** : 36 questions réparties sur les 3 technologies
- **Catégories** : Organisées par difficulté et sujet

## 🔄 Mise à jour des dumps

Après avoir ajouté de nouvelles questions ou modifié la base :

```bash
# Re-exporter les données
./scripts/export_volumes.sh

# Commiter les nouveaux dumps
git add data/dumps/
git commit -m "update: nouveaux dumps avec questions XYZ"
```

## ⚠️ Important

- Les dumps contiennent toutes les données, y compris les mots de passe hashés
- Ne pas modifier manuellement les fichiers .sql
- Les volumes `.tar.gz` sont des backups complets (plus lourds)
- Pour le développement, `postgres_dump.sql` suffit généralement