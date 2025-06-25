import React from 'react';
import { useLanguage } from '../i18n/LanguageContext';
import { useTranslation } from '../i18n/useTranslation';

// Dictionnaire de traductions complet avec TOUS les textes des questions
const TRANSLATIONS = {
  fr: {},
  
  en: {
    // ==================== DOCKER QUESTIONS ====================
    "Qu'est-ce qu'un Dockerfile?": "What is a Dockerfile?",
    "Un fichier texte contenant les instructions pour construire une image Docker": "A text file containing instructions to build a Docker image",
    "Un conteneur Docker en cours d'exécution": "A running Docker container",
    "Une image Docker compressée": "A compressed Docker image",
    "Un script de démarrage automatique": "An automatic startup script",
    
    "Quelle est la différence entre une image Docker et un conteneur?": "What is the difference between a Docker image and a container?",
    "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image": "An image is a read-only template, a container is an executable instance of the image",
    "Il n'y a pas de différence": "There is no difference",
    "Un conteneur est plus rapide qu'une image": "A container is faster than an image",
    "Une image est temporaire, un conteneur est permanent": "An image is temporary, a container is permanent",
    
    "Quelle commande permet de lister toutes les images Docker locales?": "Which command lists all local Docker images?",
    "docker images": "docker images",
    "docker list": "docker list",
    "docker show": "docker show",
    "docker ps": "docker ps",
    
    "Que fait cette commande Docker?": "What does this Docker command do?",
    "docker run -d -p 8080:80 nginx": "docker run -d -p 8080:80 nginx",
    "Lance un conteneur nginx en arrière-plan et mappe le port 8080 vers le port 80": "Runs an nginx container in the background and maps port 8080 to port 80",
    "Télécharge l'image nginx": "Downloads the nginx image",
    "Arrête le conteneur nginx": "Stops the nginx container",
    "Supprime l'image nginx": "Removes the nginx image",
    
    "Quel est le rôle de l'instruction FROM dans un Dockerfile?": "What is the role of the FROM instruction in a Dockerfile?",
    "Définit l'image de base à partir de laquelle construire": "Defines the base image to build from",
    "Copie des fichiers depuis l'hôte": "Copies files from the host",
    "Expose un port": "Exposes a port",
    "Définit le répertoire de travail": "Sets the working directory",
    
    // ==================== GIT QUESTIONS ====================
    "Quelle commande Git permet d'initialiser un nouveau dépôt?": "Which Git command initializes a new repository?",
    "git init": "git init",
    "git start": "git start",
    "git create": "git create",
    "git new": "git new",
    
    "Que fait la commande 'git add .'?": "What does the 'git add .' command do?",
    "Ajoute tous les fichiers modifiés à la zone de staging": "Adds all modified files to the staging area",
    "Supprime tous les fichiers": "Deletes all files",
    "Créé un nouveau commit": "Creates a new commit",
    "Pousse les changements vers le serveur distant": "Pushes changes to the remote server",
    
    "Comment créer une nouvelle branche et basculer dessus en une seule commande?": "How to create a new branch and switch to it in one command?",
    "git checkout -b nom_branche": "git checkout -b branch_name",
    "git branch nom_branche": "git branch branch_name",
    "git switch nom_branche": "git switch branch_name",
    "git create nom_branche": "git create branch_name",
    
    "Quelle commande permet de voir l'historique des commits?": "Which command shows the commit history?",
    "git log": "git log",
    "git history": "git history",
    "git commits": "git commits",
    "git show": "git show",
    
    // ==================== JAVASCRIPT QUESTIONS ====================
    "Quel est le résultat de: console.log(typeof null);": "What is the result of: console.log(typeof null);",
    "\"object\"": "\"object\"",
    "\"null\"": "\"null\"",
    "\"undefined\"": "\"undefined\"",
    "\"boolean\"": "\"boolean\"",
    
    "Quelle est la différence principale entre 'let' et 'var'?": "What is the main difference between 'let' and 'var'?",
    "let a une portée de bloc, var a une portée de fonction": "let has block scope, var has function scope",
    "let est plus rapide que var": "let is faster than var",
    "Il n'y a pas de différence": "There is no difference",
    "var est plus récent que let": "var is newer than let",
    
    "Comment accéder à la propriété 'name' d'un objet user de manière sécurisée?": "How to safely access the 'name' property of a user object?",
    "user?.name": "user?.name",
    "user.name": "user.name",
    "user['name']": "user['name']",
    "user.getName()": "user.getName()",
    
    "Que fait cette fonction? lambda x: x**2": "What does this function do? lambda x: x**2",
    "Retourne le carré de x": "Returns the square of x",
    "Retourne x multiplié par 2": "Returns x multiplied by 2",
    "Retourne x puissance lambda": "Returns x to the power of lambda",
    "Génère une erreur": "Generates an error",
    
    // ==================== PYTHON QUESTIONS ====================
    "Quel est le résultat de: print(type([]))": "What is the result of: print(type([]))",
    "<class 'list'>": "<class 'list'>",
    "<class 'array'>": "<class 'array'>",
    "<class 'tuple'>": "<class 'tuple'>",
    "<class 'dict'>": "<class 'dict'>",
    
    "Quelle est la différence entre une liste et un tuple?": "What is the difference between a list and a tuple?",
    "Les listes sont mutables, les tuples sont immutables": "Lists are mutable, tuples are immutable",
    "Les tuples sont plus rapides": "Tuples are faster",
    "Il n'y a pas de différence": "There is no difference",
    "Les listes utilisent moins de mémoire": "Lists use less memory",
    
    "Comment créer un dictionnaire vide en Python?": "How to create an empty dictionary in Python?",
    "{}": "{}",
    "dict()": "dict()",
    "[]": "[]",
    "set()": "set()",
    
    "Quel est le résultat de: len('Hello')": "What is the result of: len('Hello')",
    "5": "5",
    "4": "4",
    "6": "6",
    "Hello": "Hello",
    
    // ==================== APACHE SPARK QUESTIONS ====================
    "Qu'est-ce qu'un RDD dans Apache Spark?": "What is an RDD in Apache Spark?",
    "Resilient Distributed Dataset": "Resilient Distributed Dataset",
    "Remote Data Driver": "Remote Data Driver",
    "Real-time Data Distributor": "Real-time Data Distributor",
    "Relational Database Driver": "Relational Database Driver",
    
    "Quelle est la différence entre une transformation et une action dans Spark?": "What is the difference between a transformation and an action in Spark?",
    "Les transformations sont lazy, les actions déclenchent l'exécution": "Transformations are lazy, actions trigger execution",
    "Les transformations sont lazy, les actions sont immédiates": "Transformations are lazy, actions are immediate",
    "Les transformations modifient les données, les actions les lisent": "Transformations modify data, actions read it",
    "Les transformations sont plus rapides que les actions": "Transformations are faster than actions",
    
    "Comment optimiser les performances d'un job Spark?": "How to optimize Spark job performance?",
    "Utiliser le cache pour les RDD réutilisés": "Use cache for reused RDDs",
    "Augmenter le nombre de partitions": "Increase number of partitions",
    "Diminuer le nombre de workers": "Decrease number of workers",
    "Utiliser des formats de stockage optimisés": "Use optimized storage formats",
    
    "Quelle opération Spark utilise-t-on pour filtrer des données?": "Which Spark operation is used to filter data?",
    "filter()": "filter()",
    "select()": "select()",
    "map()": "map()",
    "reduce()": "reduce()",
    
    // Questions avec opérations DataFrame
    "Filtre les lignes où age > 18": "Filter rows where age > 18",
    "df.filter(df.age > 18)": "df.filter(df.age > 18)",
    "df.where(col('age') > 18)": "df.where(col('age') > 18)",
    "df.select(df.age > 18)": "df.select(df.age > 18)",
    "df.filter('age > 18')": "df.filter('age > 18')",
    
    "Sélectionne la colonne age": "Select the age column",
    "df.select('age')": "df.select('age')",
    "df.filter('age')": "df.filter('age')",
    "df.get('age')": "df.get('age')",
    "df.column('age')": "df.column('age')",
    
    // Valeurs et types communs
    "null": "null",
    "undefined": "undefined",
    "boolean": "boolean",
    "object": "object",
    "string": "string",
    "number": "number",
    "true": "true",
    "false": "false"
  },
  
  es: {
    // ==================== DOCKER QUESTIONS ====================
    "Qu'est-ce qu'un Dockerfile?": "¿Qué es un Dockerfile?",
    "Un fichier texte contenant les instructions pour construire une image Docker": "Un archivo de texto que contiene las instrucciones para construir una imagen Docker",
    "Un conteneur Docker en cours d'exécution": "Un contenedor Docker en ejecución",
    "Une image Docker compressée": "Una imagen Docker comprimida",
    "Un script de démarrage automatique": "Un script de inicio automático",
    
    "Quelle est la différence entre une image Docker et un conteneur?": "¿Cuál es la diferencia entre una imagen Docker y un contenedor?",
    "Une image est un template en lecture seule, un conteneur est une instance exécutable de l'image": "Una imagen es una plantilla de solo lectura, un contenedor es una instancia ejecutable de la imagen",
    "Il n'y a pas de différence": "No hay diferencia",
    "Un conteneur est plus rapide qu'une image": "Un contenedor es más rápido que una imagen",
    "Une image est temporaire, un conteneur est permanent": "Una imagen es temporal, un contenedor es permanente",
    
    "Quelle commande permet de lister toutes les images Docker locales?": "¿Qué comando permite listar todas las imágenes Docker locales?",
    "docker images": "docker images",
    "docker list": "docker list",
    "docker show": "docker show",
    "docker ps": "docker ps",
    
    "Que fait cette commande Docker?": "¿Qué hace este comando Docker?",
    "docker run -d -p 8080:80 nginx": "docker run -d -p 8080:80 nginx",
    "Lance un conteneur nginx en arrière-plan et mappe le port 8080 vers le port 80": "Ejecuta un contenedor nginx en segundo plano y mapea el puerto 8080 al puerto 80",
    "Télécharge l'image nginx": "Descarga la imagen nginx",
    "Arrête le conteneur nginx": "Detiene el contenedor nginx",
    "Supprime l'image nginx": "Elimina la imagen nginx",
    
    "Quel est le rôle de l'instruction FROM dans un Dockerfile?": "¿Cuál es el papel de la instrucción FROM en un Dockerfile?",
    "Définit l'image de base à partir de laquelle construire": "Define la imagen base desde la cual construir",
    "Copie des fichiers depuis l'hôte": "Copia archivos desde el host",
    "Expose un port": "Expone un puerto",
    "Définit le répertoire de travail": "Define el directorio de trabajo",
    
    // ==================== GIT QUESTIONS ====================
    "Quelle commande Git permet d'initialiser un nouveau dépôt?": "¿Qué comando de Git permite inicializar un nuevo repositorio?",
    "git init": "git init",
    "git start": "git start",
    "git create": "git create",
    "git new": "git new",
    
    "Que fait la commande 'git add .'?": "¿Qué hace el comando 'git add .'?",
    "Ajoute tous les fichiers modifiés à la zone de staging": "Agrega todos los archivos modificados al área de staging",
    "Supprime tous les fichiers": "Elimina todos los archivos",
    "Créé un nouveau commit": "Crea un nuevo commit",
    "Pousse les changements vers le serveur distant": "Empuja los cambios al servidor remoto",
    
    "Comment créer une nouvelle branche et basculer dessus en une seule commande?": "¿Cómo crear una nueva rama y cambiar a ella en un solo comando?",
    "git checkout -b nom_branche": "git checkout -b nombre_rama",
    "git branch nom_branche": "git branch nombre_rama",
    "git switch nom_branche": "git switch nombre_rama",
    "git create nom_branche": "git create nombre_rama",
    
    "Quelle commande permet de voir l'historique des commits?": "¿Qué comando permite ver el historial de commits?",
    "git log": "git log",
    "git history": "git history",
    "git commits": "git commits",
    "git show": "git show",
    
    // ==================== JAVASCRIPT QUESTIONS ====================
    "Quel est le résultat de: console.log(typeof null);": "¿Cuál es el resultado de: console.log(typeof null);",
    "\"object\"": "\"object\"",
    "\"null\"": "\"null\"",
    "\"undefined\"": "\"undefined\"",
    "\"boolean\"": "\"boolean\"",
    
    "Quelle est la différence principale entre 'let' et 'var'?": "¿Cuál es la diferencia principal entre 'let' y 'var'?",
    "let a une portée de bloc, var a une portée de fonction": "let tiene alcance de bloque, var tiene alcance de función",
    "let est plus rapide que var": "let es más rápido que var",
    "Il n'y a pas de différence": "No hay diferencia",
    "var est plus récent que let": "var es más reciente que let",
    
    "Comment accéder à la propriété 'name' d'un objet user de manière sécurisée?": "¿Cómo acceder de forma segura a la propiedad 'name' de un objeto user?",
    "user?.name": "user?.name",
    "user.name": "user.name",
    "user['name']": "user['name']",
    "user.getName()": "user.getName()",
    
    "Que fait cette fonction? lambda x: x**2": "¿Qué hace esta función? lambda x: x**2",
    "Retourne le carré de x": "Devuelve el cuadrado de x",
    "Retourne x multiplié par 2": "Devuelve x multiplicado por 2",
    "Retourne x puissance lambda": "Devuelve x elevado a la potencia lambda",
    "Génère une erreur": "Genera un error",
    
    // ==================== PYTHON QUESTIONS ====================
    "Quel est le résultat de: print(type([]))": "¿Cuál es el resultado de: print(type([]))",
    "<class 'list'>": "<class 'list'>",
    "<class 'array'>": "<class 'array'>",
    "<class 'tuple'>": "<class 'tuple'>",
    "<class 'dict'>": "<class 'dict'>",
    
    "Quelle est la différence entre une liste et un tuple?": "¿Cuál es la diferencia entre una lista y una tupla?",
    "Les listes sont mutables, les tuples sont immutables": "Las listas son mutables, las tuplas son inmutables",
    "Les tuples sont plus rapides": "Las tuplas son más rápidas",
    "Il n'y a pas de différence": "No hay diferencia",
    "Les listes utilisent moins de mémoire": "Las listas usan menos memoria",
    
    "Comment créer un dictionnaire vide en Python?": "¿Cómo crear un diccionario vacío en Python?",
    "{}": "{}",
    "dict()": "dict()",
    "[]": "[]",
    "set()": "set()",
    
    "Quel est le résultat de: len('Hello')": "¿Cuál es el resultado de: len('Hello')",
    "5": "5",
    "4": "4",
    "6": "6",
    "Hello": "Hello",
    
    // ==================== APACHE SPARK QUESTIONS ====================
    "Qu'est-ce qu'un RDD dans Apache Spark?": "¿Qué es un RDD en Apache Spark?",
    "Resilient Distributed Dataset": "Conjunto de Datos Distribuido Resiliente",
    "Remote Data Driver": "Controlador de Datos Remotos",
    "Real-time Data Distributor": "Distribuidor de Datos en Tiempo Real",
    "Relational Database Driver": "Controlador de Base de Datos Relacional",
    
    "Quelle est la différence entre une transformation et une action dans Spark?": "¿Cuál es la diferencia entre una transformación y una acción en Spark?",
    "Les transformations sont lazy, les actions déclenchent l'exécution": "Las transformaciones son lazy, las acciones activan la ejecución",
    "Les transformations sont lazy, les actions sont immédiates": "Las transformaciones son lazy, las acciones son inmediatas",
    "Les transformations modifient les données, les actions les lisent": "Las transformaciones modifican los datos, las acciones los leen",
    "Les transformations sont plus rapides que les actions": "Las transformaciones son más rápidas que las acciones",
    
    "Comment optimiser les performances d'un job Spark?": "¿Cómo optimizar el rendimiento de un job Spark?",
    "Utiliser le cache pour les RDD réutilisés": "Usar caché para RDDs reutilizados",
    "Augmenter le nombre de partitions": "Aumentar el número de particiones",
    "Diminuer le nombre de workers": "Disminuir el número de workers",
    "Utiliser des formats de stockage optimisés": "Usar formatos de almacenamiento optimizados",
    
    "Quelle opération Spark utilise-t-on pour filtrer des données?": "¿Qué operación de Spark se usa para filtrar datos?",
    "filter()": "filter()",
    "select()": "select()",
    "map()": "map()",
    "reduce()": "reduce()",
    
    // Questions avec opérations DataFrame
    "Filtre les lignes où age > 18": "Filtrar filas donde age > 18",
    "df.filter(df.age > 18)": "df.filter(df.age > 18)",
    "df.where(col('age') > 18)": "df.where(col('age') > 18)",
    "df.select(df.age > 18)": "df.select(df.age > 18)",
    "df.filter('age > 18')": "df.filter('age > 18')",
    
    "Sélectionne la colonne age": "Seleccionar la columna age",
    "df.select('age')": "df.select('age')",
    "df.filter('age')": "df.filter('age')",
    "df.get('age')": "df.get('age')",
    "df.column('age')": "df.column('age')",
    
    // Valeurs et types communs
    "null": "null",
    "undefined": "undefined",
    "boolean": "boolean",
    "object": "object",
    "string": "string",
    "number": "number",
    "true": "true",
    "false": "false"
  }
};

const SimpleTranslatedQuestion = ({ 
  question, 
  currentQuestion, 
  totalQuestions, 
  onAnswer,
  onNext,
  userAnswer,
  localScore 
}) => {
  const { t } = useTranslation();
  const { language } = useLanguage();

  // Fonction de traduction simple et directe
  const translateText = (text) => {
    if (!text) return text;
    
    // Si langue française, retour direct
    if (language === 'fr') return text;
    
    // Si traduction existe dans le dictionnaire, l'utiliser
    if (TRANSLATIONS[language] && TRANSLATIONS[language][text]) {
      return TRANSLATIONS[language][text];
    }
    
    // Sinon retourner le texte original (français)
    return text;
  };

  if (!question) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
        <p className="mt-2 text-gray-500">{t('common.loading')}</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header avec progression */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800 dark:text-white">
            {t('quiz.question', { number: currentQuestion + 1, total: totalQuestions })}
          </h2>
        </div>
        
        {/* Barre de progression */}
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentQuestion + 1) / totalQuestions) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* Question */}
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-md mb-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-6">
          {translateText(question.question_text)}
        </h3>

        {/* Options de réponse */}
        <div className="space-y-3">
          {question.options.map((option, index) => (
            <button
              key={index}
              onClick={() => onAnswer(option)} // Toujours envoyer l'option originale
              className={`
                w-full text-left p-4 rounded-lg border-2 transition-all duration-200
                ${userAnswer === option
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300'
                  : 'border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600'
                }
              `}
            >
              <div className="flex items-center">
                <span className="mr-3 text-sm font-medium text-gray-500 dark:text-gray-400">
                  {String.fromCharCode(65 + index)}
                </span>
                <span className="text-gray-900 dark:text-white">
                  {translateText(option)}
                </span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Debug info */}
      <div className="text-xs text-gray-400 mb-4 text-center">
        Langue: {language} | Traductions disponibles: {Object.keys(TRANSLATIONS[language] || {}).length}
      </div>

      {/* Boutons de navigation */}
      <div className="mt-6 flex justify-between items-center">
        <div className="text-sm text-gray-500 dark:text-gray-400">
          {localScore && (
            <>Score: {localScore.correct}/{localScore.total} ({localScore.percentage}%)</>
          )}
        </div>
        <button
          onClick={onNext}
          disabled={!userAnswer}
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {currentQuestion === totalQuestions - 1 ? t('quiz.finishQuiz') : t('quiz.nextQuestion')}
        </button>
      </div>
    </div>
  );
};

export default SimpleTranslatedQuestion;