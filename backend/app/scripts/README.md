# Script d'Import de Questions avec Images

## 🚀 Utilisation

### Import basique
```bash
# Dans le container backend
docker exec -it quiz-backend python scripts/add_questions.py --tech spark --file questions_spark.json
```

### Import avec images
```bash
# Avec dossier d'images local
docker exec -it quiz-backend python scripts/add_questions.py \
  --tech spark \
  --file questions_spark.json \
  --images-dir /app/data/images/spark
```

## 📁 Structure des Fichiers

### Structure recommandée
```
project/
├── questions/
│   ├── spark_questions.json
│   ├── git_questions.json
│   └── docker_questions.json
└── images/
    ├── spark/
    │   ├── code_examples/
    │   ├── diagrams/
    │   └── screenshots/
    ├── git/
    │   ├── workflows/
    │   ├── commands/
    │   └── examples/
    └── docker/
        ├── dockerfiles/
        ├── compose/
        └── architecture/
```

## 📝 Format des Questions JSON

### Question simple
```json
{
  "question_text": "Qu'est-ce qu'un RDD?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_answer": "Option A",
  "explanation": "Explication détaillée",
  "difficulty": 2,
  "category": "RDD",
  "tags": ["rdd", "basic"]
}
```

### Question avec image simple
```json
{
  "question_text": "Que fait ce code?",
  "question_image": "code_example.png",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_answer": "Option A",
  "explanation": "Explication avec image",
  "difficulty": 3,
  "category": "Code Examples",
  "tags": ["code", "example"]
}
```

### Question avec code à trous
```json
{
  "question_text": "Complétez le code manquant:",
  "code_image": "code_with_blanks.png",
  "options": [".groupBy()", ".filter()", ".map()", ".reduce()"],
  "correct_answer": ".groupBy()",
  "explanation": "La fonction groupBy est nécessaire ici",
  "difficulty": 4,
  "category": "Code Examples",
  "tags": ["code_completion", "advanced"]
}
```

### Question avec multiple images (format avancé)
```json
{
  "question_text": "Analysez ce workflow:",
  "images": {
    "diagram": "workflow_diagram.png",
    "code": "example_code.png",
    "screenshot": "ui_screenshot.png"
  },
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_answer": "Option A",
  "explanation": "Explication avec références aux images",
  "difficulty": 4,
  "category": "Visual",
  "tags": ["workflow", "visual", "advanced"]
}
```

## 🖼️ Types d'Images Supportés

### Catégories automatiques
- **question_image** → `/static/images/questions/`
- **code_image** → `/static/images/code_examples/`
- **diagram_image** → `/static/images/diagrams/`
- **screenshot_image** → `/static/images/screenshots/`

### Format avancé (objet images)
```json
"images": {
  "question": "image_principale.png",
  "code": "exemple_code.png", 
  "diagram": "diagramme.png",
  "screenshot": "capture_ecran.png",
  "example": "exemple_supplementaire.png"
}
```

## ✨ Fonctionnalités

### ✅ Ce que le script fait automatiquement
- **Copie les images** vers les bons dossiers
- **Génère des noms uniques** pour éviter les conflits
- **Créé les catégories** manquantes selon la technologie
- **Détecte les doublons** et les ignore
- **Valide les formats** d'images supportés
- **Ajoute des tags automatiques** pour les questions avec images
- **Organise par catégories** selon le type d'image

### 🔧 Extensions supportées
- `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg`

### 📊 Catégories par technologie

#### Apache Spark
- RDD, DataFrame, Spark SQL, Streaming, MLlib
- Architecture, Performance, Deployment
- **Code Examples**, **Visual**

#### Git  
- Basics, Branching, Merging, Remote, Advanced
- Workflow, Hooks, Troubleshooting
- **Visual Workflow**, **Command Examples**

#### Docker
- Basics, Images, Containers, Dockerfile, Compose
- Networking, Volumes, Production  
- **Code Examples**, **Architecture**

## 🎯 Cas d'Usage

### 1. Questions de code avec trous
Parfait pour tester la compréhension syntaxique
```json
{
  "question_text": "Complétez cette transformation Spark:",
  "code_image": "spark_transform_blank.png",
  "category": "Code Examples"
}
```

### 2. Questions visuelles d'architecture
Pour tester la compréhension des concepts
```json
{
  "question_text": "Identifiez les composants:",
  "images": {
    "diagram": "spark_cluster_architecture.png"
  },
  "category": "Architecture"
}
```

### 3. Analyse d'interface utilisateur
Pour les outils avec interface graphique
```json
{
  "question_text": "Que montre cette Spark UI?",
  "images": {
    "screenshot": "spark_ui_stages.png"
  },
  "category": "Performance"
}
```

## 🚀 Exemple Complet

```bash
# 1. Préparer les fichiers
mkdir -p /tmp/quiz_data/images/spark
cp mes_images/*.png /tmp/quiz_data/images/spark/

# 2. Copier dans le container
docker cp /tmp/quiz_data quiz-backend:/app/data/

# 3. Lancer l'import
docker exec -it quiz-backend python scripts/add_questions.py \
  --tech spark \
  --file /app/data/spark_questions.json \
  --images-dir /app/data/images/spark

# 4. Vérifier le résultat
curl http://localhost:8000/technologies/1/questions | jq '.[0]'
```

## 🐛 Troubleshooting

### Images non trouvées
- Vérifiez les chemins relatifs dans le JSON
- Assurez-vous que `--images-dir` pointe vers le bon dossier

### Questions dupliquées  
- Le script ignore automatiquement les questions avec le même texte
- Modifiez légèrement le texte si nécessaire

### Erreurs de catégorie
- Les catégories sont créées automatiquement
- Utilisez les noms standards ou "General" par défaut