# Quiz IT - Plateforme d'apprentissage

Une application de quiz interactive pour tester vos connaissances en technologies (Spark, Git, Docker).

## Technologies utilisées

### Backend
- Python 3.9
- FastAPI
- SQLAlchemy
- SQLite

### Frontend
- React
- Tailwind CSS
- Axios

### Infrastructure
- Docker
- Docker Compose

## Fonctionnalités

- Quiz sur différentes technologies (Spark, Git, Docker)
- Interface utilisateur moderne et responsive
- Système de score
- Filtrage par technologie et niveau de difficulté
- Explications détaillées pour chaque question

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