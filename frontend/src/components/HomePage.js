import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import AuthModal from './AuthModal';

// Icônes simples
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
  )
};

const HomePage = ({ onSelectTech, onShowDashboard }) => {
  const [technologies, setTechnologies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  
  const { user, logout, isAuthenticated } = useAuth();

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

  // Filtrer les technologies selon le terme de recherche
  const filteredTechnologies = technologies.filter(tech => 
    tech.displayName.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto p-4">
      {/* Header avec authentification */}
      <div className="flex justify-between items-center mb-8">
        <div className="text-center flex-1">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Quiz IT</h1>
          <p className="text-lg text-gray-600">
            Testez vos connaissances sur différentes technologies IT
          </p>
        </div>
        
        {/* Boutons d'authentification */}
        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-gray-700">
                <Icons.User />
                <span className="font-medium">{user?.username}</span>
              </div>
              <button
                onClick={onShowDashboard}
                className="flex items-center space-x-2 px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
              >
                <Icons.Dashboard />
                <span>Dashboard</span>
              </button>
              <button
                onClick={logout}
                className="flex items-center space-x-2 px-4 py-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
              >
                <Icons.Logout />
                <span>Déconnexion</span>
              </button>
            </div>
          ) : (
            <div className="flex space-x-2">
              <button
                onClick={() => {
                  setAuthMode('login');
                  setShowAuthModal(true);
                }}
                className="px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-md transition-colors"
              >
                Connexion
              </button>
              <button
                onClick={() => {
                  setAuthMode('register');
                  setShowAuthModal(true);
                }}
                className="px-4 py-2 bg-blue-600 text-white hover:bg-blue-700 rounded-md transition-colors"
              >
                Inscription
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Barre de recherche */}
      <div className="relative mb-8">
        <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
          <Icons.Search />
        </div>
        <input
          type="search"
          placeholder="Rechercher une technologie..."
          className="w-full pl-12 pr-4 py-3 rounded-lg border bg-white shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Technologies disponibles */}
      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-2 text-gray-500">Chargement des technologies...</p>
        </div>
      ) : (
        <>
          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Technologies disponibles ({filteredTechnologies.length})
            </h2>
            <p className="text-gray-600">
              Cliquez sur une technologie pour commencer le quiz
            </p>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {filteredTechnologies.map(tech => (
              <button
                key={tech.id}
                onClick={() => onSelectTech(tech.originalName)}
                className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 border border-gray-200 hover:border-blue-300 group"
              >
                <div className="text-center">
                  <div className="text-4xl mb-4 group-hover:scale-110 transition-transform duration-300">
                    {tech.icon || '💻'}
                  </div>
                  <h3 className="font-semibold text-lg text-gray-800 mb-2">
                    {tech.displayName}
                  </h3>
                  <p className="text-sm text-gray-600 mb-4">
                    {tech.description}
                  </p>
                  <div className="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                    Quiz disponible
                  </div>
                </div>
              </button>
            ))}
          </div>
        </>
      )}

      {/* Message si aucun résultat */}
      {!loading && filteredTechnologies.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          {searchTerm ? 
            `Aucune technologie trouvée pour "${searchTerm}"` : 
            'Aucune technologie disponible'
          }
        </div>
      )}

      {/* Modal d'authentification */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        mode={authMode}
      />
    </div>
  );
};

export default HomePage;