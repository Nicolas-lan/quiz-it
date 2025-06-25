#!/usr/bin/env python3
"""
Script corrigé pour générer toutes les traductions des questions automatiquement
"""

import json
import os
from pathlib import Path

# Chemin vers les fichiers de questions
SCRIPTS_DIR = Path("/workspace/backend/app/scripts")
OUTPUT_DIR = Path("/workspace/frontend/src/i18n/locales")

def load_questions_from_json(filename):
    """Charge les questions depuis un fichier JSON avec gestion de différents formats"""
    file_path = SCRIPTS_DIR / filename
    if not file_path.exists():
        print(f"⚠️  Fichier {filename} non trouvé")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Gestion de différents formats
            if isinstance(data, list):
                # Format: [question1, question2, ...]
                return data
            elif isinstance(data, dict) and 'questions' in data:
                # Format: {"questions": [question1, question2, ...]}
                return data['questions']
            else:
                print(f"⚠️  Format non reconnu pour {filename}")
                return []
                
    except Exception as e:
        print(f"❌ Erreur lors du chargement de {filename}: {e}")
        return []

def extract_all_texts(questions):
    """Extrait tous les textes des questions (questions et options)"""
    texts = set()
    
    for question in questions:
        # Ajouter le texte de la question
        if 'question_text' in question:
            texts.add(question['question_text'])
        
        # Ajouter toutes les options
        if 'options' in question:
            for option in question['options']:
                texts.add(option)
        
        # Ajouter la bonne réponse (si différente des options)
        if 'correct_answer' in question:
            texts.add(question['correct_answer'])
            
        # Ajouter l'explication si elle existe
        if 'explanation' in question:
            texts.add(question['explanation'])
    
    return texts

def get_manual_translations():
    """Retourne les traductions manuelles de qualité pour les termes techniques"""
    return {
        "en": {
            # Questions Spark
            "Qu'est-ce qu'un RDD dans Apache Spark?": "What is an RDD in Apache Spark?",
            "Quelle est la différence entre une transformation et une action?": "What is the difference between a transformation and an action?",
            "Comment optimiser les performances d'un job Spark?": "How to optimize Spark job performance?",
            "Quel est l'avantage principal des DataFrames par rapport aux RDDs?": "What is the main advantage of DataFrames over RDDs?",
            "Comment gérer la persistence en Spark?": "How to handle persistence in Spark?",
            
            # Réponses Spark
            "Resilient Distributed Dataset": "Resilient Distributed Dataset",
            "Les transformations sont lazy, les actions déclenchent l'exécution": "Transformations are lazy, actions trigger execution",
            "Les transformations sont lazy, les actions sont immédiates": "Transformations are lazy, actions are immediate",
            "Les transformations modifient les données, les actions les lisent": "Transformations modify data, actions read it",
            "Les transformations sont plus rapides que les actions": "Transformations are faster than actions",
            "Utiliser cache() et persist() pour éviter les recalculs": "Use cache() and persist() to avoid recomputations",
            "API plus haut niveau et optimisations Catalyst": "Higher-level API and Catalyst optimizations",
            
            # Questions Git
            "Quelle commande Git permet d'initialiser un nouveau dépôt ?": "Which Git command initializes a new repository?",
            "Comment ajouter des fichiers à la zone de staging ?": "How to add files to the staging area?",
            "Que fait la commande git merge ?": "What does the git merge command do?",
            "Comment annuler le dernier commit ?": "How to undo the last commit?",
            "Quelle est la différence entre git pull et git fetch ?": "What is the difference between git pull and git fetch?",
            
            # Réponses Git
            "git add <fichier>": "git add <file>",
            "git stage <fichier>": "git stage <file>",
            "git commit <fichier>": "git commit <file>",
            "git push <fichier>": "git push <file>",
            "Fusionne deux branches": "Merges two branches",
            "git pull = git fetch + git merge": "git pull = git fetch + git merge",
            
            # Questions Docker
            "Qu'est-ce qu'un Dockerfile ?": "What is a Dockerfile?",
            "Quelle est la différence entre une image et un conteneur Docker ?": "What is the difference between a Docker image and container?",
            "Comment exposer un port dans Docker ?": "How to expose a port in Docker?",
            "Que fait la commande docker run ?": "What does the docker run command do?",
            "Comment optimiser la taille d'une image Docker ?": "How to optimize Docker image size?",
            
            # Réponses Docker
            "Un fichier texte contenant les instructions pour construire une image Docker": "A text file containing instructions to build a Docker image",
            "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image": "An image is a read-only template, a container is an executable instance of the image",
            "Utiliser EXPOSE dans le Dockerfile": "Use EXPOSE in the Dockerfile",
            "Crée et démarre un nouveau conteneur": "Creates and starts a new container",
            "Utiliser des images de base minimales et multi-stage builds": "Use minimal base images and multi-stage builds",
            
            # Questions JavaScript
            "Quel est le résultat de: console.log(typeof null);": "What is the result of: console.log(typeof null);",
            "Quelle est la différence principale entre 'let' et 'var'?": "What is the main difference between 'let' and 'var'?",
            "Que fait cette fonction? const double = x => x * 2;": "What does this function do? const double = x => x * 2;",
            "Comment empêcher le comportement par défaut d'un événement?": "How to prevent the default behavior of an event?",
            "Quel est le résultat de: '5' + 3 + 2;": "What is the result of: '5' + 3 + 2;",
            
            # Réponses JavaScript
            "\"object\"": "\"object\"",
            "let a une portée de bloc, var a une portée de fonction": "let has block scope, var has function scope",
            "Multiplie x par 2 et retourne le résultat": "Multiplies x by 2 and returns the result",
            "event.preventDefault()": "event.preventDefault()",
            "\"532\"": "\"532\"",
            
            # Questions Python
            "Quel est le résultat de: print(type([]))": "What is the result of: print(type([]))",
            "Quelle est la différence entre une liste et un tuple?": "What is the difference between a list and a tuple?",
            "Que fait cette fonction? lambda x: x**2": "What does this function do? lambda x: x**2",
            "Pourquoi utiliser 'with open()' au lieu de 'open()'?": "Why use 'with open()' instead of 'open()'?",
            "À quoi sert un décorateur en Python?": "What is a decorator used for in Python?",
            
            # Réponses Python
            "<class 'list'>": "<class 'list'>",
            "Les listes sont mutables, les tuples sont immutables": "Lists are mutable, tuples are immutable",
            "Calcule le carré de x": "Calculates the square of x",
            "Ferme automatiquement le fichier": "Automatically closes the file",
            "Modifier le comportement d'une fonction": "Modify the behavior of a function",
        },
        
        "es": {
            # Questions Spark
            "Qu'est-ce qu'un RDD dans Apache Spark?": "¿Qué es un RDD en Apache Spark?",
            "Quelle est la différence entre une transformation et une action?": "¿Cuál es la diferencia entre una transformación y una acción?",
            "Comment optimiser les performances d'un job Spark?": "¿Cómo optimizar el rendimiento de un trabajo Spark?",
            "Quel est l'avantage principal des DataFrames par rapport aux RDDs?": "¿Cuál es la ventaja principal de los DataFrames sobre los RDDs?",
            "Comment gérer la persistence en Spark?": "¿Cómo manejar la persistencia en Spark?",
            
            # Réponses Spark
            "Resilient Distributed Dataset": "Conjunto de Datos Distribuido Resiliente",
            "Les transformations sont lazy, les actions déclenchent l'exécution": "Las transformaciones son lazy, las acciones activan la ejecución",
            "Les transformations sont lazy, les actions sont immédiates": "Las transformaciones son lazy, las acciones son inmediatas",
            "Les transformations modifient les données, les actions les lisent": "Las transformaciones modifican los datos, las acciones los leen",
            "Les transformations sont plus rapides que les actions": "Las transformaciones son más rápidas que las acciones",
            "Utiliser cache() et persist() pour éviter les recalculs": "Usar cache() y persist() para evitar recálculos",
            "API plus haut niveau et optimisations Catalyst": "API de nivel superior y optimizaciones Catalyst",
            
            # Questions Git
            "Quelle commande Git permet d'initialiser un nouveau dépôt ?": "¿Qué comando de Git permite inicializar un nuevo repositorio?",
            "Comment ajouter des fichiers à la zone de staging ?": "¿Cómo agregar archivos al área de staging?",
            "Que fait la commande git merge ?": "¿Qué hace el comando git merge?",
            "Comment annuler le dernier commit ?": "¿Cómo deshacer el último commit?",
            "Quelle est la différence entre git pull et git fetch ?": "¿Cuál es la diferencia entre git pull y git fetch?",
            
            # Réponses Git
            "git add <fichier>": "git add <archivo>",
            "git stage <fichier>": "git stage <archivo>",
            "git commit <fichier>": "git commit <archivo>",
            "git push <fichier>": "git push <archivo>",
            "Fusionne deux branches": "Fusiona dos ramas",
            "git pull = git fetch + git merge": "git pull = git fetch + git merge",
            
            # Questions Docker
            "Qu'est-ce qu'un Dockerfile ?": "¿Qué es un Dockerfile?",
            "Quelle est la différence entre une image et un conteneur Docker ?": "¿Cuál es la diferencia entre una imagen y un contenedor Docker?",
            "Comment exposer un port dans Docker ?": "¿Cómo exponer un puerto en Docker?",
            "Que fait la commande docker run ?": "¿Qué hace el comando docker run?",
            "Comment optimiser la taille d'une image Docker ?": "¿Cómo optimizar el tamaño de una imagen Docker?",
            
            # Réponses Docker
            "Un fichier texte contenant les instructions pour construire une image Docker": "Un archivo de texto que contiene las instrucciones para construir una imagen Docker",
            "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image": "Una imagen es una plantilla de solo lectura, un contenedor es una instancia ejecutable de la imagen",
            "Utiliser EXPOSE dans le Dockerfile": "Usar EXPOSE en el Dockerfile",
            "Crée et démarre un nouveau conteneur": "Crea e inicia un nuevo contenedor",
            "Utiliser des images de base minimales et multi-stage builds": "Usar imágenes base mínimas y multi-stage builds",
            
            # Questions JavaScript
            "Quel est le résultat de: console.log(typeof null);": "¿Cuál es el resultado de: console.log(typeof null);",
            "Quelle est la différence principale entre 'let' et 'var'?": "¿Cuál es la diferencia principal entre 'let' y 'var'?",
            "Que fait cette fonction? const double = x => x * 2;": "¿Qué hace esta función? const double = x => x * 2;",
            "Comment empêcher le comportement par défaut d'un événement?": "¿Cómo prevenir el comportamiento predeterminado de un evento?",
            "Quel est le résultat de: '5' + 3 + 2;": "¿Cuál es el resultado de: '5' + 3 + 2;",
            
            # Réponses JavaScript
            "\"object\"": "\"object\"",
            "let a une portée de bloc, var a une portée de fonction": "let tiene alcance de bloque, var tiene alcance de función",
            "Multiplie x par 2 et retourne le résultat": "Multiplica x por 2 y devuelve el resultado",
            "event.preventDefault()": "event.preventDefault()",
            "\"532\"": "\"532\"",
            
            # Questions Python
            "Quel est le résultat de: print(type([]))": "¿Cuál es el resultado de: print(type([]))",
            "Quelle est la différence entre une liste et un tuple?": "¿Cuál es la diferencia entre una lista y una tupla?",
            "Que fait cette fonction? lambda x: x**2": "¿Qué hace esta función? lambda x: x**2",
            "Pourquoi utiliser 'with open()' au lieu de 'open()'?": "¿Por qué usar 'with open()' en lugar de 'open()'?",
            "À quoi sert un décorateur en Python?": "¿Para qué sirve un decorador en Python?",
            
            # Réponses Python
            "<class 'list'>": "<class 'list'>",
            "Les listes sont mutables, les tuples sont immutables": "Las listas son mutables, las tuplas son inmutables",
            "Calcule le carré de x": "Calcula el cuadrado de x",
            "Ferme automatiquement le fichier": "Cierra automáticamente el archivo",
            "Modifier le comportement d'une fonction": "Modificar el comportamiento de una función",
        }
    }

def generate_complete_translations():
    """Génère les traductions complètes pour toutes les questions"""
    
    print("🔍 Extraction des questions depuis les fichiers JSON...")
    
    # Fichiers à traiter
    question_files = [
        'spark_mixed_questions.json',
        'git_mixed_questions.json', 
        'docker_mixed_questions.json',
        'javascript_questions.json',
        'python_questions.json',
        'example_questions_with_images.json'
    ]
    
    # Collecter tous les textes
    all_texts = set()
    for filename in question_files:
        questions = load_questions_from_json(filename)
        texts = extract_all_texts(questions)
        all_texts.update(texts)
        print(f"✅ {filename}: {len(questions)} questions, {len(texts)} textes extraits")
    
    print(f"\n📊 Total: {len(all_texts)} textes uniques à traduire")
    
    # Charger les traductions manuelles
    manual_translations = get_manual_translations()
    
    # Charger les traductions existantes
    def load_existing_translations(lang):
        file_path = OUTPUT_DIR / f"{lang}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('questions', {})
        return {}
    
    # Générer les traductions pour chaque langue
    for lang in ['fr', 'en', 'es']:
        print(f"\n🌍 Génération des traductions {lang.upper()}...")
        
        # Charger les traductions existantes  
        existing = load_existing_translations(lang)
        
        # Ajouter les nouvelles traductions
        questions_translations = existing.copy()
        
        for text in sorted(all_texts):
            if text not in questions_translations:
                if lang == 'fr':
                    # Pour le français, garder le texte original
                    questions_translations[text] = text
                else:
                    # Pour les autres langues, utiliser les traductions manuelles ou garder l'original
                    questions_translations[text] = manual_translations.get(lang, {}).get(text, text)
        
        # Charger le fichier complet et mettre à jour la section questions
        file_path = OUTPUT_DIR / f"{lang}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                full_data = json.load(f)
        else:
            full_data = {}
        
        # Mettre à jour la section questions
        full_data['questions'] = questions_translations
        
        # Sauvegarder
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(questions_translations)} traductions sauvées dans {lang}.json")
    
    print(f"\n🎉 Toutes les traductions ont été générées avec succès!")
    print(f"📝 Fichiers mis à jour:")
    for lang in ['fr', 'en', 'es']:
        print(f"   - {OUTPUT_DIR}/{lang}.json")

if __name__ == "__main__":
    generate_complete_translations()