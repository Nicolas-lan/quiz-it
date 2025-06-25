import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { useTranslation } from '../i18n/useTranslation';
import AuthModal from './AuthModal';
import LanguageSelector from './LanguageSelector';

// Icônes simples (déplacé hors du composant pour éviter la recréation)
const Icons = {
  Search: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
  ),
  User: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
  ),
  Logout: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
    </svg>
  ),
  Dashboard: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
    </svg>
  ),
  Moon: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
    </svg>
  ),
  Sun: () => (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  )
};

const HomePage = ({ onSelectTech, onShowDashboard }) => {
  const [technologies, setTechnologies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  
  const { user, logout, isAuthenticated } = useAuth();
  const { isDarkMode, toggleTheme } = useTheme();
  const { t } = useTranslation();

  // Mémoriser les callbacks pour éviter les re-renders inutiles
  const handleLoginClick = useCallback(() => {
    setAuthMode('login');
    setShowAuthModal(true);
  }, []);

  const handleRegisterClick = useCallback(() => {
    setAuthMode('register');
    setShowAuthModal(true);
  }, []);

  const handleCloseModal = useCallback(() => {
    setShowAuthModal(false);
  }, []);

  const handleSearchChange = useCallback((e) => {
    setSearchTerm(e.target.value);
  }, []);

  useEffect(() => {
    const fetchTechnologies = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/technologies`);
        if (response.ok) {
          const data = await response.json();
          // Mapper les données de l'API aux noms utilisés par le frontend
          const mappedTechnologies = data.map(tech => ({
            ...tech,
            originalName: tech.name, // Nom original pour l'API
            displayName: tech.display_name || tech.name // Nom affiché
          }));
          setTechnologies(mappedTechnologies);
        } else {
          console.error('Failed to fetch technologies');
        }
      } catch (error) {
        console.error('Error fetching technologies:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTechnologies();
  }, []);

  // Filtrer les technologies selon le terme de recherche (mémorisé)
  const filteredTechnologies = useMemo(() => 
    technologies.filter(tech => 
      tech.displayName.toLowerCase().includes(searchTerm.toLowerCase())
    ), [technologies, searchTerm]
  );

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
      <div className="max-w-6xl mx-auto p-4">
      {/* Header avec authentification */}
      <div className="flex justify-between items-center mb-8">
        <div className="text-center flex-1">
          <h1 className="text-4xl font-bold text-gray-800 dark:text-white mb-4">{t('quiz.title')}</h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            {t('quiz.selectTechnology')}
          </p>
        </div>
        
        {/* Boutons d'authentification */}
        <div className="flex items-center space-x-4">
          {/* Sélecteur de langue */}
          <LanguageSelector />
          
          {/* Toggle theme */}
          <button
            onClick={toggleTheme}
            className="p-2 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors"
            title={isDarkMode ? t('theme.light') : t('theme.dark')}
          >
            {isDarkMode ? <Icons.Sun /> : <Icons.Moon />}
          </button>
          {isAuthenticated ? (
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
                <Icons.User />
                <span className="font-medium">{user?.username}</span>
              </div>
              <button
                onClick={onShowDashboard}
                className="flex items-center space-x-2 px-4 py-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-md transition-colors"
              >
                <Icons.Dashboard />
                <span>{t('navigation.dashboard')}</span>
              </button>
              <button
                onClick={logout}
                className="flex items-center space-x-2 px-4 py-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors"
              >
                <Icons.Logout />
                <span>{t('navigation.logout')}</span>
              </button>
            </div>
          ) : (
            <div className="flex space-x-2">
              <button
                onClick={() => {
                  setAuthMode('login');
                  setShowAuthModal(true);
                }}
                className="px-4 py-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-md transition-colors"
              >
                {t('auth.login')}
              </button>
              <button
                onClick={() => {
                  setAuthMode('register');
                  setShowAuthModal(true);
                }}
                className="px-4 py-2 bg-blue-600 dark:bg-blue-700 text-white hover:bg-blue-700 dark:hover:bg-blue-600 rounded-md transition-colors"
              >
                {t('auth.register')}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Barre de recherche */}
      <div className="relative mb-8">
        <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500">
          <Icons.Search />
        </div>
        <input
          type="search"
          placeholder={t('common.search') + '...'}
          className="w-full pl-12 pr-4 py-3 rounded-lg border bg-white dark:bg-gray-800 dark:border-gray-700 dark:text-white shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400"
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>

        {/* Technologies disponibles */}
        {loading ? (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 dark:border-blue-400 mx-auto"></div>
            <p className="mt-2 text-gray-500 dark:text-gray-400">{t('common.loadingTechnologies')}</p>
          </div>
        ) : (
          <>
            <div className="mb-6">
              <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-4">
                {t('common.availableTechnologies')} ({filteredTechnologies.length})
              </h2>
            </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {filteredTechnologies.map(tech => (
              <button
                key={tech.id}
                onClick={() => onSelectTech(tech.originalName)}
                className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 group"
              >
                <div className="text-center">
                  <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">
                    {tech.icon || '💻'}
                  </div>
                  <h3 className="font-semibold text-lg text-gray-800 dark:text-white">
                    {tech.displayName}
                  </h3>
                </div>
              </button>
            ))}
          </div>
        </>
      )}

        {/* Message si aucun résultat */}
        {!loading && filteredTechnologies.length === 0 && (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            {searchTerm ? 
              `${t('common.noTechnologyFound')} "${searchTerm}"` : 
              t('common.noTechnologyAvailable')
            }
          </div>
        )}

        {/* Modal d'authentification */}
        <AuthModal
          isOpen={showAuthModal}
          onClose={handleCloseModal}
          mode={authMode}
        />
      </div>
    </div>
  );
};

export default HomePage;