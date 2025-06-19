import React from 'react';

export default function QuizPage({
  question,
  answers,
  selected,
  onSelect,
  onSubmit,
  questionNumber,
  totalQuestions,
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-700 relative overflow-hidden">
      {/* Motif technique subtil */}
      <div className="absolute inset-0 pointer-events-none opacity-20" style={{
        backgroundImage: `
          repeating-linear-gradient(135deg, #4a90e2 0 1px, transparent 1px 20px),
          repeating-linear-gradient(225deg, #4a90e2 0 1px, transparent 1px 20px)
        `
      }} />
      {/* Carte principale */}
      <div className="relative z-10 w-full max-w-3xl rounded-2xl shadow-2xl border-4 border-blue-600 bg-white">
        {/* En-tête */}
        <div className="rounded-t-xl bg-blue-600 px-8 py-6 flex items-center">
          <h1 className="text-white text-2xl font-bold flex-1 text-center">
            Certification IT - Quiz Platform
          </h1>
        </div>
        {/* Zone de contenu */}
        <div className="px-8 py-8 bg-blue-50 border-t-2 border-blue-400 rounded-b-2xl">
          <div className="mb-6">
            <span className="text-blue-900 font-bold text-lg">
              Question {questionNumber}/{totalQuestions} : {question}
            </span>
          </div>
          <div className="space-y-4 mb-8">
            {answers.map((ans, idx) => (
              <button
                key={idx}
                onClick={() => onSelect(idx)}
                className={`w-full text-left px-6 py-4 rounded-xl border-2
                  ${selected === idx ? 'border-blue-600 bg-blue-100' : 'border-blue-300 bg-blue-100 hover:bg-blue-200'}
                  text-blue-900 font-medium transition`}
              >
                {ans}
              </button>
            ))}
          </div>
          <div className="flex justify-center">
            <button
              onClick={onSubmit}
              className="px-8 py-3 bg-blue-500 text-white font-bold rounded-xl shadow hover:bg-blue-600 transition"
            >
              Soumettre la Réponse
            </button>
          </div>
        </div>
      </div>
      {/* Décorations */}
      <div className="absolute top-8 left-8 w-10 h-10 bg-blue-300 rounded-full opacity-70" />
      <div className="absolute top-8 right-8 w-10 h-10 bg-blue-300 rounded-full opacity-70" />
    </div>
  );
} 