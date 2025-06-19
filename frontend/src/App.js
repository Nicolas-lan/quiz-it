import React, { useState } from 'react';
import { AuthProvider } from './context/AuthContext';
import HomePage from './components/HomePage';
import Quiz from './components/Quiz';
import Dashboard from './components/Dashboard';

function App() {
  const [selectedTech, setSelectedTech] = useState(null);
  const [showDashboard, setShowDashboard] = useState(false);

  const handleBack = () => {
    setSelectedTech(null);
    setShowDashboard(false);
  };

  if (showDashboard) {
    return (
      <AuthProvider>
        <div className="App">
          <Dashboard onBack={handleBack} />
        </div>
      </AuthProvider>
    );
  }

  if (selectedTech) {
    return (
      <AuthProvider>
        <div className="App">
          <Quiz selectedTechnology={selectedTech} onBack={handleBack} />
        </div>
      </AuthProvider>
    );
  }

  return (
    <AuthProvider>
      <div className="App">
        <HomePage 
          onSelectTech={setSelectedTech} 
          onShowDashboard={() => setShowDashboard(true)} 
        />
      </div>
    </AuthProvider>
  );
}

export default App;