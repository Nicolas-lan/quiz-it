import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

const Dashboard = ({ onBack }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token } = useAuth();
  const { isDarkMode } = useTheme();

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch(`${API_URL}/dashboard/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        setError('Erreur lors du chargement du dashboard');
      }
    } catch (err) {
      setError('Erreur de connexion');
      console.error('Erreur dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  // Mémoriser les fonctions utilitaires pour éviter les recréations
  const formatTime = useCallback((seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  }, []);

  const formatDate = useCallback((dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }, []);

  // Mémoriser les données traitées pour éviter les recalculs (avant les returns conditionnels)
  const stats = dashboardData?.statistics;
  const history = dashboardData?.quiz_history || [];
  
  const technologyEntries = useMemo(() => 
    stats?.quizzes_by_technology ? Object.entries(stats.quizzes_by_technology) : []
  , [stats?.quizzes_by_technology]);

  const recentHistory = useMemo(() => history.slice(0, 10), [history]);

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
        <div className="max-w-6xl mx-auto p-4">
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 dark:border-blue-400 mx-auto"></div>
            <p className="mt-2 text-gray-500 dark:text-gray-400">Chargement du dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
        <div className="max-w-6xl mx-auto p-4">
          <div className="text-center py-8">
            <p className="text-red-500 dark:text-red-400">{error}</p>
            <button
              onClick={onBack}
              className="mt-4 px-4 py-2 bg-blue-500 dark:bg-blue-600 text-white rounded hover:bg-blue-600 dark:hover:bg-blue-500"
            >
              Retour
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
      <div className="max-w-6xl mx-auto p-4">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white">
            Dashboard - {dashboardData?.user?.full_name || dashboardData?.user?.username}
          </h1>
          <button
            onClick={onBack}
            className="px-4 py-2 bg-gray-500 dark:bg-gray-600 text-white rounded hover:bg-gray-600 dark:hover:bg-gray-500 transition-colors"
          >
            ← Retour
          </button>
        </div>

        {/* Statistiques générales */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border-l-4 border-blue-500">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Quiz Total</h3>
            <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{stats?.total_quizzes || 0}</p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border-l-4 border-green-500">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Score Moyen</h3>
            <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{stats?.average_score || 0}%</p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border-l-4 border-yellow-500">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Meilleur Score</h3>
            <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{stats?.best_score || 0}%</p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md border-l-4 border-purple-500">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Temps Total</h3>
            <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">{formatTime(stats?.total_time_spent || 0)}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Quiz par technologie */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">Quiz par Technologie</h2>
            <div className="space-y-4">
              {technologyEntries.map(([tech, count]) => {
                const avgScore = stats.scores_by_technology[tech] || 0;
                return (
                  <div key={tech} className="flex justify-between items-center">
                    <div>
                      <p className="font-medium text-gray-800 dark:text-white">{tech}</p>
                      <p className="text-sm text-gray-500 dark:text-gray-400">{count} quiz(s) - Moyenne: {avgScore}%</p>
                    </div>
                    <div className="w-24 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div 
                        className="bg-blue-500 dark:bg-blue-400 h-2 rounded-full" 
                        style={{ width: `${avgScore}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
              {technologyEntries.length === 0 && (
                <p className="text-gray-500 dark:text-gray-400 text-center py-4">Aucun quiz terminé</p>
              )}
            </div>
          </div>

          {/* Activité récente */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">Activité Récente</h2>
            <div className="space-y-3">
              {stats?.recent_activity?.map((activity, index) => (
                <div key={activity.id || index} className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded">
                  <div>
                    <p className="font-medium text-gray-800 dark:text-white">{activity.technology_name}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {activity.correct_answers}/{activity.total_questions} - {formatDate(activity.completed_at)}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className={`font-bold ${activity.score_percentage >= 70 ? 'text-green-600 dark:text-green-400' : activity.score_percentage >= 50 ? 'text-yellow-600 dark:text-yellow-400' : 'text-red-600 dark:text-red-400'}`}>
                      {activity.score_percentage}%
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{formatTime(activity.time_spent_seconds)}</p>
                  </div>
                </div>
              )) || []}
              {(!stats?.recent_activity || stats.recent_activity.length === 0) && (
                <p className="text-gray-500 dark:text-gray-400 text-center py-4">Aucune activité récente</p>
              )}
            </div>
          </div>
        </div>

        {/* Historique complet */}
        {history.length > 0 && (
          <div className="mt-8 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">Historique Complet</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Technologie
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Score
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Questions
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Temps
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Date
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {recentHistory.map((quiz, index) => (
                    <tr key={quiz.id || index} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900 dark:text-white">{quiz.technology_name}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                          quiz.score_percentage >= 70 ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300' : 
                          quiz.score_percentage >= 50 ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300' : 
                          'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300'
                        }`}>
                          {quiz.score_percentage}%
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                        {quiz.correct_answers}/{quiz.total_questions}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {formatTime(quiz.time_spent_seconds)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {formatDate(quiz.completed_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;