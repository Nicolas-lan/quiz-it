# 🎯 Quiz IT - Plateforme d'apprentissage

Une application de quiz interactive moderne pour tester vos connaissances en technologies IT.

## 🚀 Technologies utilisées

### Backend
- **Python 3.9** avec FastAPI
- **PostgreSQL** pour la base de données
- **SQLAlchemy** ORM avec Alembic migrations
- **JWT** pour l'authentification
- **Pydantic** pour la validation des données

### Frontend
- **React 18** avec hooks modernes
- **Tailwind CSS** pour le styling
- **Axios** pour les appels API
- **React Router** pour la navigation

### Infrastructure
- **Docker & Docker Compose** pour la containerisation
- **Nginx** (ready for production)
- **PostgreSQL** en conteneur

## ✨ Fonctionnalités

### Actuellement disponible
- 🎯 **3 technologies** : Apache Spark, Docker, Git
- 📝 **36 questions** au total (10 Spark, 14 Docker, 12 Git)
- 🎨 **Interface moderne** et responsive
- ⚡ **Système de scoring** en temps réel
- 🔄 **Questions dynamiques** avec différents niveaux de difficulté
- 🔍 **Recherche** et filtrage par technologie

### En développement (voir ROADMAP.md)
- 🌙 Mode sombre
- 👤 Profils utilisateur et historique
- 🏆 Leaderboard et classements
- 📊 Statistiques détaillées
- 📱 Version mobile optimisée

## Installation

1. Cloner le repository :
```bash
git clone <votre-repo-url>
cd quiz-it
```

2. Lancer l'application avec Docker Compose :
```bash
docker-compose up -d
```

3. Accéder à l'application :
- Frontend : http://localhost:3000
- API Backend : http://localhost:8000
- Documentation API : http://localhost:8000/docs

## Structure du projet

```
.
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── database.py
│   │   ├── initial_data.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.js
│   │   └── index.js
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## Développement

Pour ajouter de nouvelles questions :
1. Modifier le fichier `backend/app/initial_data.py`
2. Redémarrer le conteneur backend : `docker-compose restart backend`

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence

MIT 