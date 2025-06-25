import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

// Langues supportées
export const SUPPORTED_LANGUAGES = {
  fr: { code: 'fr', name: 'Français', flag: '🇫🇷' },
  en: { code: 'en', name: 'English', flag: '🇬🇧' },
  es: { code: 'es', name: 'Español', flag: '🇪🇸' }
};

// Détection de la langue du navigateur
const detectBrowserLanguage = () => {
  const browserLang = navigator.language.split('-')[0];
  return SUPPORTED_LANGUAGES[browserLang] ? browserLang : 'fr';
};

// Stockage sécurisé de la langue
const getStoredLanguage = () => {
  try {
    return localStorage.getItem('app_language') || detectBrowserLanguage();
  } catch (error) {
    console.error('Erreur lecture langue:', error);
    return 'fr';
  }
};

const setStoredLanguage = (language) => {
  try {
    localStorage.setItem('app_language', language);
  } catch (error) {
    console.error('Erreur stockage langue:', error);
  }
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguageState] = useState(getStoredLanguage());
  const [translations, setTranslations] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  // Chargement des traductions
  const loadTranslations = async (lang) => {
    try {
      setIsLoading(true);
      const translationModule = await import(`./locales/${lang}.json`);
      setTranslations(translationModule.default);
    } catch (error) {
      console.error(`Erreur chargement traductions ${lang}:`, error);
      // Fallback sur français
      if (lang !== 'fr') {
        const fallbackModule = await import('./locales/fr.json');
        setTranslations(fallbackModule.default);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Changement de langue
  const setLanguage = (newLanguage) => {
    if (SUPPORTED_LANGUAGES[newLanguage]) {
      setLanguageState(newLanguage);
      setStoredLanguage(newLanguage);
      loadTranslations(newLanguage);
    }
  };

  // Chargement initial
  useEffect(() => {
    loadTranslations(language);
  }, [language]);

  const value = {
    language,
    setLanguage,
    translations,
    isLoading,
    supportedLanguages: SUPPORTED_LANGUAGES,
    currentLanguageInfo: SUPPORTED_LANGUAGES[language]
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};