import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ConfirmationModal from './ConfirmationModal';

const SparkQuiz = ({ selectedTechnology, onBack }) => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  useEffect(() => {
    fetchQuestions();
  }, [selectedTechnology]);

  const fetchQuestions = async () => {
    try {
      setLoading(true);
      const params = {};
      if (selectedTechnology && selectedTechnology !== 'all') {
        params.technology = selectedTechnology;
      }
      
      const response = await axios.get('http://localhost:8000/questions/', { params });
      setQuestions(response.data);
      setCurrentQuestion(0);
      setScore(0);
      setShowResults(false);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching questions:', error);
      setLoading(false);
    }
  };

  const handleAnswer = (answer) => {
    if (answer === questions[currentQuestion].correct_answer) {
      setScore(score + 1);
    }

    if (currentQuestion + 1 < questions.length) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setShowResults(true);
    }
  };

  const resetQuiz = () => {
    setCurrentQuestion(0);
    setScore(0);
    setShowResults(false);
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
            {score / questions.length >= 0.8 ? '🎉' : score / questions.length >= 0.6 ? '👍' : '📚'}
          </div>
          <p className="text-xl mb-4">
            Votre score: {score} sur {questions.length}
          </p>
          <p className="text-lg mb-6 text-gray-600">
            Pourcentage: {((score / questions.length) * 100).toFixed(1)}%
          </p>
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

export default SparkQuiz;