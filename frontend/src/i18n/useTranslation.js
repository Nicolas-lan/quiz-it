import { useLanguage } from './LanguageContext';

export const useTranslation = () => {
  const { language, translations, isLoading } = useLanguage();

  // Fonction de traduction avec navigation hiérarchique et interpolation
  const t = (key, params = {}) => {
    if (!translations || isLoading) {
      return key; // Fallback sur la clé si traductions pas encore chargées
    }

    // Navigation hiérarchique (ex: "auth.login" → translations.auth.login)
    const keys = key.split('.');
    let value = translations;

    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        // Clé non trouvée, retourner la clé originale
        console.warn(`Traduction manquante pour la clé: ${key} (langue: ${language})`);
        return key;
      }
    }

    // Si la valeur finale n'est pas une string, retourner la clé
    if (typeof value !== 'string') {
      console.warn(`Valeur de traduction invalide pour: ${key}`);
      return key;
    }

    // Interpolation des variables {{variable}}
    return interpolate(value, params);
  };

  // Fonction d'interpolation pour remplacer {{variable}} par sa valeur
  const interpolate = (template, params) => {
    return template.replace(/\{\{(\w+)\}\}/g, (match, key) => {
      return params[key] !== undefined ? params[key] : match;
    });
  };

  // Fonction pour obtenir une traduction avec fallback
  const tWithFallback = (key, fallback = '', params = {}) => {
    const translation = t(key, params);
    return translation === key ? fallback : translation;
  };

  // Fonction pour les traductions au pluriel (simple)
  const tPlural = (key, count, params = {}) => {
    const pluralKey = count === 1 ? `${key}.singular` : `${key}.plural`;
    return t(pluralKey, { count, ...params });
  };

  // Fonction pour formater les nombres selon la locale
  const formatNumber = (number) => {
    const locales = {
      fr: 'fr-FR',
      en: 'en-US',
      es: 'es-ES'
    };
    
    return new Intl.NumberFormat(locales[language] || 'fr-FR').format(number);
  };

  // Fonction pour formater les dates selon la locale
  const formatDate = (date, options = {}) => {
    const locales = {
      fr: 'fr-FR',
      en: 'en-US', 
      es: 'es-ES'
    };

    const defaultOptions = {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };

    return new Intl.DateTimeFormat(
      locales[language] || 'fr-FR', 
      { ...defaultOptions, ...options }
    ).format(new Date(date));
  };

  // Fonction pour formater les pourcentages
  const formatPercentage = (value) => {
    const locales = {
      fr: 'fr-FR',
      en: 'en-US',
      es: 'es-ES'
    };

    return new Intl.NumberFormat(locales[language] || 'fr-FR', {
      style: 'percent',
      minimumFractionDigits: 0,
      maximumFractionDigits: 1
    }).format(value / 100);
  };

  return {
    t,
    tWithFallback,
    tPlural,
    formatNumber,
    formatDate,
    formatPercentage,
    language,
    isLoading
  };
};