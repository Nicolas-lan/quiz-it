import React, { useState } from 'react';
import HomePage from './components/HomePage';
import Questionnaire from './components/Questionnaire';

const TECHNOLOGIES = [
  { value: 'spark', label: 'Apache Spark' },
  { value: 'docker', label: 'Docker' },
  { value: 'git', label: 'Git' },
  // Ajoute d'autres technos ici
];

function App() {
  const [selectedTech, setSelectedTech] = useState(null);

  if (!selectedTech) {
    return <HomePage onSelectTech={setSelectedTech} />;
  }

  return <Questionnaire technology={selectedTech} onBack={() => setSelectedTech(null)} />;
}

export default App; 