# 🚀 Guide de démarrage - Quiz IT

Guide étape par étape pour installer et démarrer le projet Quiz IT sur votre machine.

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

### ✅ Obligatoire
- **Git** : [Télécharger Git](https://git-scm.com/downloads)
- **Docker Desktop** : [Télécharger Docker](https://www.docker.com/products/docker-desktop/)
  - Windows : Docker Desktop pour Windows
  - macOS : Docker Desktop pour Mac  
  - Linux : Docker Engine + Docker Compose

### 🔍 Vérification des prérequis
Ouvrez un terminal et vérifiez que tout est installé :

```bash
# Vérifier Git
git --version
# Résultat attendu : git version 2.x.x

# Vérifier Docker
docker --version
# Résultat attendu : Docker version 20.x.x

# Vérifier Docker Compose
docker-compose --version
# Résultat attendu : docker-compose version 1.x.x ou 2.x.x
```

## 📥 Installation du projet

### 1. Cloner le repository

```bash
# Cloner le projet
git clone [URL_DU_REPO]
cd quiz-it

# Vérifier que vous êtes sur la bonne branche
git branch
# Vous devriez voir : * develop
```

### 2. Configuration de l'environnement

```bash
# Copier les fichiers de configuration
cp .env.example .env
cp backend/.env.example backend/.env

# 📝 Optionnel : Modifier les mots de passe (pour production seulement)
# Les valeurs par défaut fonctionnent parfaitement pour le développement
```

### 3. Démarrer l'application

```bash
# Construire et démarrer tous les services
docker-compose up -d

# Vérifier que tous les services démarrent correctement
docker-compose ps
```

**Résultat attendu :**
```
     Name                   Command               State                    Ports                  
--------------------------------------------------------------------------------------------------
quiz-backend    uvicorn app.main:app --ho ...   Up      0.0.0.0:8000->8000/tcp                 
quiz-frontend   docker-entrypoint.sh npm s ...   Up      0.0.0.0:3000->3000/tcp                 
quiz-postgres   docker-entrypoint.sh postgres   Up      0.0.0.0:5432->5432/tcp                 
quiz-redis      docker-entrypoint.sh redis ...   Up      0.0.0.0:6379->6379/tcp
```

### 4. Importer les données initiales

```bash
# Attendre que PostgreSQL soit prêt (30-60 secondes)
docker-compose logs postgres

# Importer les données (questions, utilisateurs, etc.)
./scripts/import_volumes.sh
```

### 5. Vérifier l'installation

Ouvrez votre navigateur et testez ces URLs :

- ✅ **Application principale** : http://localhost:3000
- ✅ **API Backend** : http://localhost:8000
- ✅ **Documentation API** : http://localhost:8000/docs

## 🔑 Se connecter

### Identifiants par défaut
- **Username** : `admin`
- **Password** : `admin`

### Test de l'application
1. Allez sur http://localhost:3000
2. Cliquez sur "Se connecter" (icône utilisateur en haut à droite)
3. Saisissez admin/admin
4. Testez le mode sombre (icône lune/soleil)
5. Lancez un quiz sur une technologie

## 🛠️ Commandes utiles

### Gestion Docker
```bash
# Voir les logs en temps réel
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f backend

# Redémarrer un service
docker-compose restart backend

# Arrêter tout
docker-compose down

# Rebuild complet (après modifications)
docker-compose down
docker-compose up -d --build
```

### Données et volumes
```bash
# Exporter vos données (après ajout de questions)
./scripts/export_volumes.sh

# Réimporter les données (reset complet)
./scripts/import_volumes.sh
```

### Développement
```bash
# Mode développement avec logs
docker-compose up

# Accéder au shell du backend
docker-compose exec backend bash

# Accéder à PostgreSQL
docker-compose exec postgres psql -U quiz_user -d quiz_db
```

## 🐛 Résolution de problèmes

### Problème : Port déjà utilisé
```bash
# Erreur : "bind: address already in use"
# Solution : Arrêter le service qui utilise le port

# Vérifier quel processus utilise le port 3000
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows

# Changer le port dans docker-compose.yml si nécessaire
ports:
  - "3001:3000"  # Port 3001 au lieu de 3000
```

### Problème : Docker non démarré
```bash
# Erreur : "Cannot connect to the Docker daemon"
# Solution : Démarrer Docker Desktop
# Attendre que Docker soit complètement démarré (icône en vert)
```

### Problème : Base de données vide
```bash
# Vérifier que l'import s'est bien passé
docker-compose exec postgres psql -U quiz_user -d quiz_db -c "SELECT COUNT(*) FROM users;"

# Si 0 résultat, relancer l'import
./scripts/import_volumes.sh
```

### Problème : Erreur de build
```bash
# Nettoyer et rebuild
docker-compose down
docker system prune -f
docker-compose up -d --build
```

## 📱 Fonctionnalités disponibles

### ✅ Actuellement
- 🎯 **3 technologies** : Apache Spark, Docker, Git
- 📝 **36 questions** réparties
- 🌙 **Mode sombre** complet
- 🔐 **Authentification** sécurisée
- ⚡ **Interface** optimisée et responsive
- 📊 **Scoring** en temps réel

### 🚧 En développement (voir ROADMAP.md)
- 👤 Profils utilisateur personnalisés
- 🏆 Leaderboard et classements
- 📊 Statistiques détaillées
- 🧪 Nouvelles technologies (JavaScript, Python)

## 🆘 Besoin d'aide ?

### Contacts
- **Créateur du projet** : [VOTRE_NOM]
- **Email** : [VOTRE_EMAIL]
- **Slack/Teams** : [VOTRE_CANAL]

### Ressources
- 📚 **Documentation complète** : README.md
- 🗺️ **Roadmap** : ROADMAP.md
- 🔧 **API Docs** : http://localhost:8000/docs (après démarrage)

### Signaler un problème
1. Vérifier les logs : `docker-compose logs`
2. Consulter ce guide de résolution
3. Créer une issue sur le repository Git
4. Contacter l'équipe

---

**🎉 Bon développement !**

*Dernière mise à jour : 20 juin 2025*