import React from 'react';

const TECHNOLOGIES = [
  {
    value: 'spark',
    label: 'Apache Spark',
    description: 'Big Data & Traitement distribué',
    color: 'bg-orange-100',
    icon: '🔥',
  },
  {
    value: 'docker',
    label: 'Docker',
    description: 'Conteneurisation & DevOps',
    color: 'bg-blue-100',
    icon: '🐳',
  },
  {
    value: 'git',
    label: 'Git',
    description: 'Gestion de version',
    color: 'bg-red-100',
    icon: '🌱',
  },
  // Ajoute d'autres technos ici
];

export default function HomePage({ onSelectTech }) {
  return (
    <div className="min-h-screen flex flex-col justify-between bg-gray-50">
      <div>
        <h1 className="text-4xl font-bold text-center mt-4 mb-2">Bienvenue sur le Quiz IT</h1>
        <p className="text-center text-lg text-gray-600 mb-10">Choisissez une technologie pour commencer</p>
        <div className="max-w-4xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          {TECHNOLOGIES.map(tech => (
            <div key={tech.value} className={`rounded-xl shadow-md p-6 flex flex-col items-center ${tech.color}`}>
              <div className="text-5xl mb-4">{tech.icon}</div>
              <h2 className="text-2xl font-semibold mb-2">{tech.label}</h2>
              <p className="text-gray-700 mb-4">{tech.description}</p>
              <button
                onClick={() => onSelectTech(tech.value)}
                className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              >
                Commencer
              </button>
            </div>
          ))}
        </div>
      </div>
      <footer className="text-center text-gray-400 py-6 text-sm">
        Powered by MonProjetData
      </footer>
    </div>
  );
} 