import React from 'react';

// Service de traduction dynamique pour les questions
// Approche hybride : cache local + API de traduction

const CACHE_PREFIX = 'question_translation_';
const CACHE_DURATION = 7 * 24 * 60 * 60 * 1000; // 7 jours

// Cache local pour éviter les re-traductions
const TranslationCache = {
  // Générer une clé de cache unique
  getCacheKey: (questionId, language) => {
    return `${CACHE_PREFIX}${questionId}_${language}`;
  },

  // Récupérer une traduction depuis le cache
  get: (questionId, language) => {
    try {
      const key = TranslationCache.getCacheKey(questionId, language);
      const cached = localStorage.getItem(key);
      
      if (cached) {
        const { data, timestamp } = JSON.parse(cached);
        
        // Vérifier si le cache n'est pas expiré
        if (Date.now() - timestamp < CACHE_DURATION) {
          return data;
        } else {
          // Cache expiré, le supprimer
          localStorage.removeItem(key);
        }
      }
    } catch (error) {
      console.error('Erreur lecture cache traduction:', error);
    }
    return null;
  },

  // Sauvegarder une traduction dans le cache
  set: (questionId, language, translatedQuestion) => {
    try {
      const key = TranslationCache.getCacheKey(questionId, language);
      const cacheData = {
        data: translatedQuestion,
        timestamp: Date.now()
      };
      localStorage.setItem(key, JSON.stringify(cacheData));
    } catch (error) {
      console.error('Erreur sauvegarde cache traduction:', error);
    }
  },

  // Nettoyer le cache (appel optionnel)
  clear: () => {
    try {
      const keys = Object.keys(localStorage);
      keys.forEach(key => {
        if (key.startsWith(CACHE_PREFIX)) {
          localStorage.removeItem(key);
        }
      });
    } catch (error) {
      console.error('Erreur nettoyage cache:', error);
    }
  }
};

// Service de traduction via API
const TranslationAPI = {
  // Traduire du texte via l'API backend
  translateText: async (text, targetLanguage, sourceLanguage = 'fr') => {
    try {
      const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/api/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text,
          target: targetLanguage,
          source: sourceLanguage
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur traduction: ${response.status}`);
      }

      const result = await response.json();
      return result.translatedText || text;
    } catch (error) {
      console.error('Erreur API traduction:', error);
      return text; // Fallback sur le texte original
    }
  },

  // Traduire une question complète
  translateQuestion: async (question, targetLanguage) => {
    if (targetLanguage === 'fr') {
      return question; // Pas de traduction nécessaire
    }

    try {
      // Traduire en parallèle tous les textes
      const [
        translatedQuestionText,
        translatedExplanation,
        ...translatedOptions
      ] = await Promise.all([
        TranslationAPI.translateText(question.question_text, targetLanguage),
        question.explanation ? 
          TranslationAPI.translateText(question.explanation, targetLanguage) : 
          Promise.resolve(question.explanation),
        ...question.options.map(option => 
          TranslationAPI.translateText(option, targetLanguage)
        )
      ]);

      // Trouver l'index de la bonne réponse pour la traduire aussi
      const correctAnswerIndex = question.options.indexOf(question.correct_answer);
      const translatedCorrectAnswer = correctAnswerIndex !== -1 ? 
        translatedOptions[correctAnswerIndex] : 
        await TranslationAPI.translateText(question.correct_answer, targetLanguage);

      return {
        ...question,
        question_text: translatedQuestionText,
        options: translatedOptions,
        correct_answer: translatedCorrectAnswer,
        explanation: translatedExplanation,
        originalLanguage: 'fr',
        translatedTo: targetLanguage
      };
    } catch (error) {
      console.error('Erreur traduction question:', error);
      return question; // Fallback sur la question originale
    }
  }
};

// Service principal de traduction des questions
export const QuestionTranslationService = {
  // Obtenir une question traduite (avec cache)
  getTranslatedQuestion: async (question, targetLanguage) => {
    // Si c'est déjà en français, pas besoin de traduction
    if (targetLanguage === 'fr') {
      return question;
    }

    // Vérifier le cache d'abord
    const cached = TranslationCache.get(question.id, targetLanguage);
    if (cached) {
      return cached;
    }

    // Traduire et mettre en cache
    try {
      const translated = await TranslationAPI.translateQuestion(question, targetLanguage);
      TranslationCache.set(question.id, targetLanguage, translated);
      return translated;
    } catch (error) {
      console.error('Erreur service traduction:', error);
      return question; // Fallback
    }
  },

  // Précharger des traductions (pour optimiser l'UX)
  preloadTranslations: async (questions, targetLanguage) => {
    if (targetLanguage === 'fr') return;

    const promises = questions.map(async (question) => {
      // Vérifier si déjà en cache
      if (!TranslationCache.get(question.id, targetLanguage)) {
        // Traduire en arrière-plan
        try {
          const translated = await TranslationAPI.translateQuestion(question, targetLanguage);
          TranslationCache.set(question.id, targetLanguage, translated);
        } catch (error) {
          // Ignorer les erreurs en préchargement
          console.warn('Erreur préchargement traduction:', error);
        }
      }
    });

    // Exécuter en parallèle sans bloquer
    Promise.all(promises);
  },

  // Nettoyer le cache (utilitaire)
  clearCache: TranslationCache.clear,

  // Statistiques du cache (debug)
  getCacheStats: () => {
    try {
      const keys = Object.keys(localStorage);
      const translationKeys = keys.filter(key => key.startsWith(CACHE_PREFIX));
      
      return {
        totalCached: translationKeys.length,
        cacheSize: translationKeys.reduce((size, key) => {
          return size + localStorage.getItem(key).length;
        }, 0),
        languages: [...new Set(translationKeys.map(key => key.split('_').pop()))]
      };
    } catch (error) {
      return { totalCached: 0, cacheSize: 0, languages: [] };
    }
  }
};

// Hook React pour utiliser la traduction des questions
export const useQuestionTranslation = (question, language) => {
  const [translatedQuestion, setTranslatedQuestion] = React.useState(question);
  const [isTranslating, setIsTranslating] = React.useState(false);

  React.useEffect(() => {
    if (!question) return;

    const translateQuestion = async () => {
      setIsTranslating(true);
      try {
        const translated = await QuestionTranslationService.getTranslatedQuestion(question, language);
        setTranslatedQuestion(translated);
      } catch (error) {
        console.error('Erreur traduction question:', error);
        setTranslatedQuestion(question);
      } finally {
        setIsTranslating(false);
      }
    };

    translateQuestion();
  }, [question, language]);

  return {
    question: translatedQuestion,
    isTranslating,
    originalQuestion: question
  };
};