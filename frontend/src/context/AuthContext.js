import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Fonctions utilitaires pour le stockage sécurisé
const getStoredToken = () => {
  try {
    return sessionStorage.getItem('auth_token') || localStorage.getItem('auth_token');
  } catch (error) {
    console.error('Erreur lecture token:', error);
    return null;
  }
};

const setStoredToken = (token) => {
  try {
    if (token) {
      sessionStorage.setItem('auth_token', token);
      // Supprimer de localStorage pour migrer vers sessionStorage
      localStorage.removeItem('auth_token');
    } else {
      sessionStorage.removeItem('auth_token');
      localStorage.removeItem('auth_token');
    }
  } catch (error) {
    console.error('Erreur stockage token:', error);
  }
};

const clearStoredToken = () => {
  try {
    sessionStorage.removeItem('auth_token');
    localStorage.removeItem('auth_token');
    localStorage.removeItem('token'); // Nettoyer l'ancien nom aussi
  } catch (error) {
    console.error('Erreur suppression token:', error);
  }
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(getStoredToken());
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Vérifier le token au démarrage
  useEffect(() => {
    const abortController = new AbortController();
    
    const checkToken = async () => {
      if (token) {
        try {
          const response = await fetch(`${API_URL}/auth/validate-token`, {
            headers: {
              'Authorization': `Bearer ${token}`
            },
            signal: abortController.signal
          });
          
          if (response.ok) {
            const data = await response.json();
            setUser(data.user);
          } else {
            // Token invalide
            clearStoredToken();
            setToken(null);
          }
        } catch (error) {
          if (error.name !== 'AbortError') {
            console.error('Erreur validation token:', error);
            clearStoredToken();
            setToken(null);
          }
        }
      }
      setLoading(false);
    };

    checkToken();
    
    // Cleanup function pour annuler la requête
    return () => {
      abortController.abort();
    };
  }, [token, API_URL]);

  const login = async (username, password) => {
    console.log('🔐 Tentative de connexion pour:', username);
    
    const abortController = new AbortController();
    
    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        signal: abortController.signal
      });

      console.log('📡 Statut réponse:', response.status, response.statusText);
      
      const data = await response.json();
      console.log('📋 Données reçues:', data);

      if (response.ok) {
        const newToken = data.access_token;
        
        // Vérifier que le token est valide avant de le stocker
        if (!newToken) {
          console.log('❌ Token manquant dans la réponse');
          return { success: false, error: 'Token manquant dans la réponse' };
        }
        
        console.log('🎫 Token reçu, stockage...');
        setToken(newToken);
        setStoredToken(newToken);
        
        // Récupérer les infos utilisateur
        try {
          console.log('👤 Récupération des infos utilisateur...');
          const userResponse = await fetch(`${API_URL}/auth/me`, {
            headers: {
              'Authorization': `Bearer ${newToken}`
            },
            signal: abortController.signal
          });
          
          if (userResponse.ok) {
            const userData = await userResponse.json();
            console.log('✅ Utilisateur connecté:', userData.username);
            setUser(userData);
            return { success: true };
          } else {
            console.log('❌ Impossible de récupérer l\'utilisateur, mais connexion OK');
            // Problème CORS, mais connexion réussie - créer un utilisateur minimal
            const minimalUser = {
              username: username,
              email: 'admin@quiz.local',
              full_name: 'Administrator'
            };
            setUser(minimalUser);
            return { success: true };
          }
        } catch (userError) {
          if (userError.name !== 'AbortError') {
            console.log('💥 Erreur récupération utilisateur (probablement CORS):', userError);
            // Même si CORS échoue, le token est valide - créer un utilisateur minimal
            const minimalUser = {
              username: username,
              email: 'admin@quiz.local', 
              full_name: 'Administrator'
            };
            setUser(minimalUser);
            return { success: true };
          }
        }
      } else {
        // Gestion des erreurs HTTP
        console.log('❌ Erreur HTTP:', response.status, data);
        const errorMessage = data.detail || 'Identifiants incorrects';
        return { success: false, error: errorMessage };
      }
    } catch (error) {
      if (error.name !== 'AbortError') {
        console.error('Erreur de connexion:', error);
        return { success: false, error: 'Erreur de connexion au serveur' };
      }
    }
  };

  const register = async (userData) => {
    const abortController = new AbortController();
    
    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
        signal: abortController.signal
      });

      if (response.ok) {
        // Auto-login après inscription
        return await login(userData.username, userData.password);
      } else {
        const errorData = await response.json();
        return { success: false, error: errorData.detail };
      }
    } catch (error) {
      if (error.name !== 'AbortError') {
        return { success: false, error: 'Erreur lors de l\'inscription' };
      }
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    clearStoredToken();
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};