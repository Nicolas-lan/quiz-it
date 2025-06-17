import React, { useState } from 'react';
import HomePage from './components/HomePage';
import SparkQuiz from './components/SparkQuiz';

function App() {
  const [selectedTech, setSelectedTech] = useState(null);

  if (!selectedTech) {
    return (
      <div className="App">
        <HomePage onSelectTech={setSelectedTech} />
      </div>
    );
  }

  return (
    <div className="App">
      <SparkQuiz technology={selectedTech} onBack={() => setSelectedTech(null)} />
    </div>
  );
}

export default App;