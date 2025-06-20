import React, { useState, useCallback, useMemo } from 'react';
import { useAuth } from '../context/AuthContext';

const AuthModal = React.memo(({ isOpen, onClose, mode: initialMode = 'login' }) => {
  const [mode, setMode] = useState(initialMode);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    full_name: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login, register } = useAuth();

  // Mémoriser les callbacks pour éviter les re-renders
  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation des champs
    if (!formData.username.trim()) {
      setError('Le nom d\'utilisateur est requis');
      setLoading(false);
      return;
    }
    
    if (!formData.password.trim()) {
      setError('Le mot de passe est requis');
      setLoading(false);
      return;
    }

    if (mode === 'register') {
      if (!formData.email.trim()) {
        setError('L\'email est requis');
        setLoading(false);
        return;
      }
      if (!formData.full_name.trim()) {
        setError('Le nom complet est requis');
        setLoading(false);
        return;
      }
      if (formData.password.length < 6) {
        setError('Le mot de passe doit contenir au moins 6 caractères');
        setLoading(false);
        return;
      }
    }

    try {
      let result;
      if (mode === 'login') {
        result = await login(formData.username, formData.password);
      } else {
        result = await register(formData);
      }

      if (result && result.success === true) {
        onClose();
        setFormData({ username: '', password: '', email: '', full_name: '' });
      } else {
        setError(result?.error || 'Identifiants incorrects');
        // Ne pas fermer le modal en cas d'erreur
      }
    } catch (error) {
      console.error('💥 Erreur soumission form:', error);
      setError('Une erreur inattendue est survenue');
    } finally {
      setLoading(false);
    }
  }, [mode, formData, login, register, onClose]);

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }, []);

  // Mémoriser les valeurs dérivées
  const isRegisterMode = useMemo(() => mode === 'register', [mode]);
  const buttonText = useMemo(() => {
    if (loading) return 'Chargement...';
    return mode === 'login' ? 'Se connecter' : 'S\'inscrire';
  }, [loading, mode]);

  const switchModeText = useMemo(() => {
    return mode === 'login' 
      ? 'Pas de compte ? S\'inscrire' 
      : 'Déjà un compte ? Se connecter';
  }, [mode]);

  const handleModeSwitch = useCallback(() => {
    setMode(mode === 'login' ? 'register' : 'login');
    setError('');
    setFormData({ username: '', password: '', email: '', full_name: '' });
  }, [mode]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-8 max-w-md w-full mx-4">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
            {mode === 'login' ? 'Connexion' : 'Inscription'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {isRegisterMode && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Nom complet
              </label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                required={isRegisterMode}
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Nom d'utilisateur
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              required
            />
          </div>

          {isRegisterMode && (
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Email
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                required={isRegisterMode}
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Mot de passe
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              required
            />
          </div>

          {error && (
            <div className="text-red-500 text-sm text-center">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 dark:bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-600 dark:hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 disabled:opacity-50"
          >
            {buttonText}
          </button>
        </form>

        <div className="mt-4 text-center">
          <button
            onClick={handleModeSwitch}
            className="text-blue-500 dark:text-blue-400 hover:text-blue-600 dark:hover:text-blue-300 text-sm"
          >
            {switchModeText}
          </button>
        </div>
      </div>
    </div>
  );
});

export default AuthModal;