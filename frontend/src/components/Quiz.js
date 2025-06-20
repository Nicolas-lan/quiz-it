import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import ConfirmationModal from './ConfirmationModal';

const Quiz = ({ selectedTechnology, onBack }) => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [userAnswers, setUserAnswers] = useState([]);
  const [quizSession, setQuizSession] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [finalResults, setFinalResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [startTime, setStartTime] = useState(null);
  
  const { token, isAuthenticated } = useAuth();
  const { isDarkMode } = useTheme();
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  // Mémoriser les calculs de score local pour éviter les recalculs
  const localScore = useMemo(() => {
    const correctAnswers = userAnswers.filter(a => a.is_correct).length;
    const totalQuestions = questions.length;
    return {
      correct: correctAnswers,
      total: totalQuestions,
      percentage: totalQuestions > 0 ? ((correctAnswers / totalQuestions) * 100).toFixed(1) : 0
    };
  }, [userAnswers, questions.length]);

  // Mémoriser l'icône de résultat
  const resultIcon = useMemo(() => {
    const score = finalResults ? finalResults.score_percentage : parseFloat(localScore.percentage);
    return score >= 80 ? '🎉' : score >= 60 ? '👍' : '📚';
  }, [finalResults, localScore.percentage]);

  useEffect(() => {
    if (selectedTechnology) {
      fetchQuestions();
    }
  }, [selectedTechnology]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      setStartTime(new Date());
      
      // Charger les questions
      const response = await fetch(`${API_URL}/questions/?technology=${selectedTechnology}`);
      const questions = await response.json();
      setQuestions(questions);
      setCurrentQuestion(0);
      setUserAnswers([]);
      setShowResults(false);
      setFinalResults(null);
      
      // Essayer de démarrer une session si connecté
      if (isAuthenticated && token) {
        try {
          await startQuizSession();
        } catch (error) {
          console.log('Session en base échouée, continuons en local:', error);
        }
      }
    } catch (error) {
      console.error('Error fetching questions:', error);
      alert('Erreur lors du chargement des questions');
    } finally {
      setLoading(false);
    }
  };

  const startQuizSession = async () => {
    // Trouver l'ID de la technologie
    const techResponse = await fetch(`${API_URL}/technologies`);
    const technologies = await techResponse.json();
    const technology = technologies.find(tech => tech.name === selectedTechnology);
    
    if (!technology) {
      throw new Error('Technologie non trouvée');
    }

    // Démarrer une session de quiz
    const sessionResponse = await fetch(`${API_URL}/quiz/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        technology_id: technology.id
      })
    });

    if (!sessionResponse.ok) {
      throw new Error('Erreur lors du démarrage du quiz');
    }

    const session = await sessionResponse.json();
    setQuizSession(session);
    console.log('Session quiz démarrée:', session.id);
  };

  const handleAnswer = async (answer) => {
    // Ajouter la réponse au state local
    const newAnswer = {
      question_id: questions[currentQuestion].id,
      user_answer: answer,
      correct_answer: questions[currentQuestion].correct_answer,
      is_correct: answer === questions[currentQuestion].correct_answer
    };
    
    setUserAnswers([...userAnswers, newAnswer]);

    // TODO: Réactiver la sauvegarde des réponses plus tard
    // if (isAuthenticated && token && quizSession) {
    //   try {
    //     await fetch(`${API_URL}/quiz/answer`, {
    //       method: 'POST',
    //       headers: {
    //         'Content-Type': 'application/json',
    //         'Authorization': `Bearer ${token}`
    //       },
    //       body: JSON.stringify({
    //         quiz_session_id: quizSession.id,
    //         question_id: questions[currentQuestion].id,
    //         user_answer: answer,
    //         time_spent_seconds: Math.floor((new Date() - startTime) / 1000)
    //       })
    //     });
    //   } catch (error) {
    //     console.log('Sauvegarde en base échouée, continuons en local:', error);
    //   }
    // }

    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      // Terminer le quiz
      await finishQuiz();
    }
  };

  const finishQuiz = async () => {
    const endTime = new Date();
    const totalTimeSeconds = Math.floor((endTime - startTime) / 1000);

    // Essayer de terminer la session si connecté
    if (isAuthenticated && token && quizSession) {
      try {
        const response = await fetch(`${API_URL}/quiz/${quizSession.id}/finish`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            time_spent_seconds: totalTimeSeconds
          })
        });

        if (response.ok) {
          const results = await response.json();
          setFinalResults(results);
          console.log('Quiz terminé et sauvegardé:', results);
        }
      } catch (error) {
        console.log('Sauvegarde finale échouée:', error);
      }
    }
    
    setShowResults(true);
  };

  // Mémoriser les callbacks pour éviter les re-renders
  const resetQuiz = useCallback(() => {
    fetchQuestions();
  }, []);

  const handleBackClick = useCallback(() => {
    if (!showResults && currentQuestion > 0) {
      setShowConfirmModal(true);
    } else {
      onBack();
    }
  }, [showResults, currentQuestion, onBack]);

  const handleConfirmModalClose = useCallback(() => {
    setShowConfirmModal(false);
  }, []);

  const handleConfirmModalConfirm = useCallback(() => {
    setShowConfirmModal(false);
    onBack();
  }, [onBack]);

  if (loading) {
    return (
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-xl text-gray-800 dark:text-white">Chargement des questions...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-200">
      <div className="max-w-4xl mx-auto p-4">
        <div className="mb-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white">
            Quiz {selectedTechnology ? selectedTechnology.toUpperCase() : ''}
          </h1>
          <button
            onClick={handleBackClick}
            className="px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors flex items-center"
          >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
          </svg>
          Retour
        </button>
      </div>

      {!showResults ? (
        questions.length > 0 ? (
            <div className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
              <div className="mb-4">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  Question {currentQuestion + 1} sur {questions.length}
                </span>
                <span className="ml-4 text-sm text-gray-500 dark:text-gray-400">
                  Technologie: {questions[currentQuestion].technology}
                </span>
                <span className="ml-4 text-sm text-gray-500 dark:text-gray-400">
                  Catégorie: {questions[currentQuestion].category}
                </span>
                <span className="ml-4 text-sm text-gray-500 dark:text-gray-400">
                  Difficulté: {questions[currentQuestion].difficulty}/5
                </span>
              </div>

              <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-white">
                {questions[currentQuestion].question_text}
              </h2>

              <div className="space-y-2">
                {questions[currentQuestion].options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswer(option)}
                    className="w-full p-3 text-left border dark:border-gray-600 rounded hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:border-blue-300 dark:hover:border-blue-600 transition-colors text-gray-800 dark:text-gray-200"
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="text-center bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
              <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Aucune question disponible</h2>
              <p className="text-gray-600 dark:text-gray-300">
                Aucune question trouvée pour la technologie {selectedTechnology}.
              </p>
            </div>
        )
        ) : (
          <div className="text-center bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Quiz terminé !</h2>
          <div className="text-6xl mb-4">
            {resultIcon}
          </div>
          
          {finalResults ? (
              <>
                <p className="text-xl mb-4 text-gray-800 dark:text-white">
                  Score final: {finalResults.correct_answers} sur {finalResults.total_questions}
                </p>
                <p className="text-lg mb-4 text-gray-600 dark:text-gray-300">
                  Pourcentage: {finalResults.score_percentage}%
                </p>
                <p className="text-sm mb-6 text-gray-500 dark:text-gray-400">
                  Temps: {Math.floor(finalResults.time_spent_seconds / 60)}m {finalResults.time_spent_seconds % 60}s
                </p>
              </>
          ) : (
              <>
                <p className="text-xl mb-4 text-gray-800 dark:text-white">
                  Score local: {localScore.correct} sur {localScore.total}
                </p>
                <p className="text-lg mb-6 text-gray-600 dark:text-gray-300">
                  Pourcentage: {localScore.percentage}%
                </p>
              </>
          )}
          
            <div className="space-x-4">
              <button
                onClick={resetQuiz}
                className="bg-blue-500 dark:bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-600 dark:hover:bg-blue-500 transition-colors"
              >
                Recommencer
              </button>
              <button
                onClick={onBack}
                className="bg-gray-500 dark:bg-gray-600 text-white px-6 py-2 rounded hover:bg-gray-600 dark:hover:bg-gray-500 transition-colors"
              >
                Retour à l'accueil
              </button>
            </div>
          </div>
        )}

        <ConfirmationModal
          isOpen={showConfirmModal}
          onClose={handleConfirmModalClose}
          onConfirm={handleConfirmModalConfirm}
        />
      </div>
    </div>
  );
};

export default Quiz;