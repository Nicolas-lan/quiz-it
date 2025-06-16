import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SparkQuiz = () => {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [selectedTechnology, setSelectedTechnology] = useState('all');

  const technologies = [
    'all',
    'spark',
    'git',
    'docker'
  ];

  const categories = [
    'all',
    'RDD',
    'DataFrame',
    'Spark SQL',
    'Spark Streaming',
    'MLlib',
    'GraphX',
    'Basics',
    'Concepts'
  ];

  const difficulties = [
    { value: 'all', label: 'All Levels' },
    { value: 1, label: 'Beginner' },
    { value: 2, label: 'Intermediate' },
    { value: 3, label: 'Advanced' }
  ];

  useEffect(() => {
    fetchQuestions();
  }, [selectedCategory, selectedDifficulty, selectedTechnology]);

  const fetchQuestions = async () => {
    try {
      const params = {};
      if (selectedCategory !== 'all') params.category = selectedCategory;
      if (selectedDifficulty !== 'all') params.difficulty = selectedDifficulty;
      if (selectedTechnology !== 'all') params.technology = selectedTechnology;
      
      const response = await axios.get('http://localhost:8000/questions/', { params });
      setQuestions(response.data);
      setCurrentQuestion(0);
      setScore(0);
      setShowResults(false);
    } catch (error) {
      console.error('Error fetching questions:', error);
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

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-4">Tech Quiz</h1>
        
        <div className="flex gap-4 mb-4">
          <select
            value={selectedTechnology}
            onChange={(e) => setSelectedTechnology(e.target.value)}
            className="p-2 border rounded"
          >
            {technologies.map(tech => (
              <option key={tech} value={tech}>
                {tech.charAt(0).toUpperCase() + tech.slice(1)}
              </option>
            ))}
          </select>

          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="p-2 border rounded"
          >
            {categories.map(category => (
              <option key={category} value={category}>
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </option>
            ))}
          </select>

          <select
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
            className="p-2 border rounded"
          >
            {difficulties.map(difficulty => (
              <option key={difficulty.value} value={difficulty.value}>
                {difficulty.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {!showResults ? (
        questions.length > 0 && (
          <div className="bg-white shadow-lg rounded-lg p-6">
            <div className="mb-4">
              <span className="text-sm text-gray-500">
                Question {currentQuestion + 1} of {questions.length}
              </span>
              <span className="ml-4 text-sm text-gray-500">
                Technology: {questions[currentQuestion].technology}
              </span>
              <span className="ml-4 text-sm text-gray-500">
                Category: {questions[currentQuestion].category}
              </span>
              <span className="ml-4 text-sm text-gray-500">
                Difficulty: {questions[currentQuestion].difficulty}
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
                  className="w-full p-3 text-left border rounded hover:bg-gray-100 transition-colors"
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        )
      ) : (
        <div className="text-center bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Quiz Completed!</h2>
          <p className="text-xl mb-4">
            Your score: {score} out of {questions.length}
          </p>
          <p className="text-lg mb-6">
            Percentage: {((score / questions.length) * 100).toFixed(1)}%
          </p>
          <button
            onClick={resetQuiz}
            className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 transition-colors"
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
};

export default SparkQuiz; 