// Point d'entrée principal pour l'internationalisation
export { LanguageProvider, useLanguage, SUPPORTED_LANGUAGES } from './LanguageContext';
export { useTranslation } from './useTranslation';
export { QuestionTranslationService, useQuestionTranslation } from './questionTranslationService';

// Configuration par défaut
export const I18N_CONFIG = {
  defaultLanguage: 'fr',
  fallbackLanguage: 'fr',
  supportedLanguages: ['fr', 'en', 'es'],
  cacheExpiration: 7 * 24 * 60 * 60 * 1000, // 7 jours
};

// Utilitaires
export const getLanguageFromUrl = () => {
  const path = window.location.pathname;
  const langMatch = path.match(/^\/([a-z]{2})\//);
  return langMatch ? langMatch[1] : null;
};

export const setLanguageInUrl = (language) => {
  const currentPath = window.location.pathname;
  const newPath = currentPath.replace(/^\/[a-z]{2}\//, '/').replace(/^\//, '');
  window.history.pushState({}, '', `/${language}/${newPath}`);
};