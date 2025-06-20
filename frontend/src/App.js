import React, { useState, Suspense, lazy } from 'react';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import HomePage from './components/HomePage';
import LoadingSpinner from './components/LoadingSpinner';

// Lazy loading des composants moins critiques
const Quiz = lazy(() => import('./components/Quiz'));
const Dashboard = lazy(() => import('./components/Dashboard'));

function App() {
  const [selectedTech, setSelectedTech] = useState(null);
  const [showDashboard, setShowDashboard] = useState(false);

  const handleBack = () => {
    setSelectedTech(null);
    setShowDashboard(false);
  };

  if (showDashboard) {
    return (
      <ThemeProvider>
        <AuthProvider>
          <div className="App">
            <Suspense fallback={<LoadingSpinner />}>
              <Dashboard onBack={handleBack} />
            </Suspense>
          </div>
        </AuthProvider>
      </ThemeProvider>
    );
  }

  if (selectedTech) {
    return (
      <ThemeProvider>
        <AuthProvider>
          <div className="App">
            <Suspense fallback={<LoadingSpinner />}>
              <Quiz selectedTechnology={selectedTech} onBack={handleBack} />
            </Suspense>
          </div>
        </AuthProvider>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider>
      <AuthProvider>
        <div className="App">
          <HomePage 
            onSelectTech={setSelectedTech} 
            onShowDashboard={() => setShowDashboard(true)} 
          />
        </div>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;