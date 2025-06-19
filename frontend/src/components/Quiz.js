import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
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
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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

  const resetQuiz = () => {
    fetchQuestions();
  };

  const handleBackClick = () => {
    if (!showResults && currentQuestion > 0) {
      setShowConfirmModal(true);
    } else {
      onBack();
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Chargement des questions...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="mb-8 flex justify-between items-center">
        <h1 className="text-3xl font-bold">
          Quiz {selectedTechnology ? selectedTechnology.toUpperCase() : ''}
        </h1>
        <button
          onClick={handleBackClick}
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
          </svg>
          Retour
        </button>
      </div>

      {!showResults ? (
        questions.length > 0 ? (
          <div className="bg-white shadow-lg rounded-lg p-6">
            <div className="mb-4">
              <span className="text-sm text-gray-500">
                Question {currentQuestion + 1} sur {questions.length}
              </span>
              <span className="ml-4 text-sm text-gray-500">
                Technologie: {questions[currentQuestion].technology}
              </span>
              <span className="ml-4 text-sm text-gray-500">
                Catégorie: {questions[currentQuestion].category}
              </span>
              <span className="ml-4 text-sm text-gray-500">
                Difficulté: {questions[currentQuestion].difficulty}/5
              </span>
            </div>

            <h2 className="text-xl font-semibold mb-4">
              {questions[currentQuestion].question_text}
            </h2>

            <div className="space-y-2">
              {questions[currentQuestion].options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => handleAnswer(option)}
                  className="w-full p-3 text-left border rounded hover:bg-blue-50 hover:border-blue-300 transition-colors"
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="text-center bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Aucune question disponible</h2>
            <p className="text-gray-600">
              Aucune question trouvée pour la technologie {selectedTechnology}.
            </p>
          </div>
        )
      ) : (
        <div className="text-center bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Quiz terminé !</h2>
          <div className="text-6xl mb-4">
            {finalResults ? 
              (finalResults.score_percentage >= 80 ? '🎉' : finalResults.score_percentage >= 60 ? '👍' : '📚') :
              (userAnswers.filter(a => a.is_correct).length / questions.length >= 0.8 ? '🎉' : 
               userAnswers.filter(a => a.is_correct).length / questions.length >= 0.6 ? '👍' : '📚')
            }
          </div>
          
          {finalResults ? (
            <>
              <p className="text-xl mb-4">
                Score final: {finalResults.correct_answers} sur {finalResults.total_questions}
              </p>
              <p className="text-lg mb-4 text-gray-600">
                Pourcentage: {finalResults.score_percentage}%
              </p>
              <p className="text-sm mb-6 text-gray-500">
                Temps: {Math.floor(finalResults.time_spent_seconds / 60)}m {finalResults.time_spent_seconds % 60}s
              </p>
            </>
          ) : (
            <>
              <p className="text-xl mb-4">
                Score local: {userAnswers.filter(a => a.is_correct).length} sur {questions.length}
              </p>
              <p className="text-lg mb-6 text-gray-600">
                Pourcentage: {((userAnswers.filter(a => a.is_correct).length / questions.length) * 100).toFixed(1)}%
              </p>
            </>
          )}
          
          <div className="space-x-4">
            <button
              onClick={resetQuiz}
              className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 transition-colors"
            >
              Recommencer
            </button>
            <button
              onClick={onBack}
              className="bg-gray-500 text-white px-6 py-2 rounded hover:bg-gray-600 transition-colors"
            >
              Retour à l'accueil
            </button>
          </div>
        </div>
      )}

      <ConfirmationModal
        isOpen={showConfirmModal}
        onClose={() => setShowConfirmModal(false)}
        onConfirm={() => {
          setShowConfirmModal(false);
          onBack();
        }}
      />
    </div>
  );
};

export default Quiz;