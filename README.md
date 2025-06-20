# 🎯 Quiz IT - Plateforme d'apprentissage

Une application de quiz interactive moderne pour tester vos connaissances en technologies IT. Interface élégante avec mode sombre, authentification sécurisée et optimisations React avancées.

## 🚀 Technologies utilisées

### Backend
- **Python 3.11** avec FastAPI 0.100.1
- **PostgreSQL 15** pour la base de données
- **SQLAlchemy** ORM avec Alembic migrations
- **JWT** pour l'authentification sécurisée
- **Pydantic** pour la validation des données
- **Passlib + bcrypt** pour le hashage des mots de passe

### Frontend
- **React 18** avec hooks modernes (memo, useMemo, useCallback)
- **Tailwind CSS 3.4** avec mode sombre complet
- **Context API** pour l'état global (Auth + Theme)
- **Fetch API** avec AbortController pour les requêtes
- **SessionStorage** pour la sécurité des tokens

### Infrastructure
- **Docker & Docker Compose** pour la containerisation
- **PostgreSQL** en conteneur avec optimisations
- **Redis** pour le cache (prêt pour les futures fonctionnalités)
- **Nginx** (ready for production)

## ✨ Fonctionnalités

### ✅ Actuellement disponible
- 🎯 **3 technologies** : Apache Spark, Docker, Git
- 📝 **36 questions** au total (10 Spark, 14 Docker, 12 Git)
- 🎨 **Interface moderne** et responsive
- 🌙 **Mode sombre complet** avec toggle et persistance
- 🔐 **Authentification sécurisée** (admin/admin par défaut)
- ⚡ **Optimisations React** (memo, useMemo, useCallback)
- 🔄 **Questions dynamiques** avec différents niveaux de difficulté
- 🔍 **Recherche** et filtrage par technologie
- 📊 **Système de scoring** en temps réel
- 🛡️ **Sécurité renforcée** (CORS, validation, tokens)

### 🚧 En développement (voir ROADMAP.md)
- 👤 Profils utilisateur et historique
- 🏆 Leaderboard et classements
- 📊 Statistiques détaillées et graphiques
- 📱 Version mobile optimisée
- 🧪 Tests automatisés

## 🚀 Installation rapide

> 📚 **Pour vos collègues :** Guide détaillé dans [SETUP.md](SETUP.md)  
> 📧 **Pour partager :** Instructions dans [PARTAGE.md](PARTAGE.md)

### Prérequis
- **Docker Desktop** installé et démarré
- **Git** installé

### Étapes

1. **Cloner le repository :**
```bash
git clone <votre-repo-url>
cd quiz-it
```

2. **Configurer l'environnement :**
```bash
# Copier les fichiers d'environnement
cp .env.example .env
cp backend/.env.example backend/.env

# Modifier les mots de passe si nécessaire (optionnel pour le développement)
```

3. **Lancer l'application :**
```bash
docker-compose up -d
```

4. **Accéder à l'application :**
- 🌐 **Frontend** : http://localhost:3000
- 🔌 **API Backend** : http://localhost:8000
- 📚 **Documentation API** : http://localhost:8000/docs
- 🐘 **PostgreSQL** : localhost:5432
- 🔴 **Redis** : localhost:6379

### 🔑 Connexion par défaut
- **Username** : `admin`
- **Password** : `admin`

### 🛠️ Commandes utiles
```bash
# Voir les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart backend

# Arrêter tout
docker-compose down

# Rebuild après modifications
docker-compose up -d --build

# Exporter les données (pour partage)
./scripts/export_volumes.sh

# Importer les données (nouveau dev)
./scripts/import_volumes.sh
```

## 📁 Structure du projet

```
quiz-it/
├── 📄 README.md                    # Documentation
├── 📄 ROADMAP.md                   # Feuille de route
├── 📄 docker-compose.yml           # Orchestration Docker
├── 📄 .env.example                 # Template configuration
├── 📁 data/                        # Données persistantes
│   ├── 📄 README.md                # Guide volumes et dumps
│   └── 📁 dumps/                   # Exports PostgreSQL/Redis
├── 📁 scripts/                     # Scripts utilitaires
│   ├── 📄 export_volumes.sh        # Export données
│   └── 📄 import_volumes.sh        # Import données
├── 📁 backend/                     # API FastAPI
│   ├── 📄 Dockerfile
│   ├── 📄 requirements.txt
│   ├── 📄 .env.example
│   ├── 📁 app/
│   │   ├── 📄 main.py              # Point d'entrée FastAPI
│   │   ├── 📄 schemas.py           # Modèles Pydantic
│   │   ├── 📁 api/endpoints/       # Endpoints API
│   │   │   ├── 📄 auth.py          # Authentification
│   │   │   └── 📄 dashboard.py     # Dashboard
│   │   ├── 📁 core/                # Configuration
│   │   │   ├── 📄 auth.py          # JWT & sécurité
│   │   │   ├── 📄 db.py            # Base de données
│   │   │   └── 📄 init_data.py     # Données initiales
│   │   ├── 📁 models/              # Modèles SQLAlchemy
│   │   │   └── 📄 database_models.py
│   │   └── 📁 scripts/             # Scripts utilitaires
│   └── 📁 alembic/                 # Migrations DB
├── 📁 frontend/                    # Application React
│   ├── 📄 Dockerfile
│   ├── 📄 package.json
│   ├── 📄 tailwind.config.js       # Config Tailwind + dark mode
│   └── 📁 src/
│       ├── 📄 App.js               # Composant principal
│       ├── 📁 components/          # Composants React
│       │   ├── 📄 HomePage.js      # Page d'accueil
│       │   ├── 📄 Quiz.js          # Interface quiz
│       │   ├── 📄 AuthModal.js     # Modal authentification
│       │   └── 📄 Dashboard.js     # Tableau de bord
│       └── 📁 context/             # Context React
│           ├── 📄 AuthContext.js   # État authentification
│           └── 📄 ThemeContext.js  # Mode sombre
└── 📁 logs/                        # Logs application
```

## 🛠️ Développement

### Ajouter de nouvelles questions
1. Utiliser les scripts dans `backend/app/scripts/`
2. Modifier `backend/app/core/init_data.py`
3. Redémarrer : `docker-compose restart backend`

### Ajouter de nouvelles technologies
1. Modifier `create_technologies()` dans `init_data.py`
2. Ajouter les questions correspondantes
3. Mettre à jour l'interface frontend si nécessaire

### Mode développement avec hot-reload
```bash
# Backend : modifications auto-reloadées
# Frontend : React hot-reload activé
docker-compose up -d
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le projet
2. **Créer** une branche : `git checkout -b feature/ma-fonctionnalite`
3. **Commiter** : `git commit -m 'feat: ajouter ma fonctionnalité'`
4. **Pousser** : `git push origin feature/ma-fonctionnalite`
5. **Pull Request** avec description détaillée

### 📋 Types de contributions recherchées
- 🧪 Nouvelles questions (JavaScript, Python, Kubernetes, etc.)
- 🎨 Améliorations UI/UX
- 🛡️ Corrections de sécurité
- 📱 Optimisations mobile
- 🧪 Tests automatisés
- 📚 Documentation

## 📊 État du projet

- ✅ **Version stable** : Prêt pour la production
- 🔐 **Sécurité** : Authentification JWT, validation des données
- ⚡ **Performance** : Optimisations React, requêtes optimisées
- 🌙 **Interface** : Mode sombre complet, responsive design
- 📱 **Compatibilité** : Tous navigateurs modernes

## 📝 Licence

MIT - Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

**Développé avec ❤️ pour la communauté IT**

*Dernière mise à jour : 20 juin 2025* 