import React, { useState, useRef, useEffect } from 'react';
import { useLanguage, SUPPORTED_LANGUAGES } from '../i18n/LanguageContext';
import { useTranslation } from '../i18n/useTranslation';

const LanguageSelector = () => {
  const { language, setLanguage, supportedLanguages, currentLanguageInfo } = useLanguage();
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  // Debug pour voir ce qu'il y a dans supportedLanguages
  console.log('supportedLanguages:', supportedLanguages);

  // Fermer le dropdown quand on clique à l'extérieur
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    setIsOpen(false);
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Bouton principal */}
      <button
        onClick={toggleDropdown}
        className="flex items-center space-x-2 px-3 py-2 rounded-lg 
                   bg-white dark:bg-gray-800 
                   border border-gray-300 dark:border-gray-600
                   hover:bg-gray-50 dark:hover:bg-gray-700
                   transition-colors duration-200
                   text-sm font-medium text-gray-700 dark:text-gray-200"
        title={t('language.change')}
      >
        <span className="text-lg">{currentLanguageInfo.flag}</span>
        <svg 
          className={`w-4 h-4 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 
                        bg-white dark:bg-gray-800 
                        border border-gray-300 dark:border-gray-600
                        rounded-lg shadow-lg z-50">
          <div className="py-1">
            <button
              onClick={() => handleLanguageChange('fr')}
              className={`w-full flex items-center px-4 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-150 ${language === 'fr' ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-200'}`}
            >
              <span className="text-lg mr-3">🇫🇷</span>
              <span className="font-medium">Français</span>
              {language === 'fr' && (
                <svg className="ml-auto w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </button>
            <button
              onClick={() => handleLanguageChange('en')}
              className={`w-full flex items-center px-4 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-150 ${language === 'en' ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-200'}`}
            >
              <span className="text-lg mr-3">🇬🇧</span>
              <span className="font-medium">English</span>
              {language === 'en' && (
                <svg className="ml-auto w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </button>
            <button
              onClick={() => handleLanguageChange('es')}
              className={`w-full flex items-center px-4 py-2 text-sm text-left hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-150 ${language === 'es' ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-200'}`}
            >
              <span className="text-lg mr-3">🇪🇸</span>
              <span className="font-medium">Español</span>
              {language === 'es' && (
                <svg className="ml-auto w-4 h-4 text-blue-600 dark:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          </div>
          
          {/* Séparateur */}
          <div className="border-t border-gray-200 dark:border-gray-600"></div>
          
          {/* Info traduction */}
          <div className="px-4 py-2 text-xs text-gray-500 dark:text-gray-400">
            {t('language.autoDetect')}
          </div>
        </div>
      )}
    </div>
  );
};

export default React.memo(LanguageSelector);