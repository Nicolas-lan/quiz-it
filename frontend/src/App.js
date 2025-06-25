import React, { useState, Suspense, lazy } from 'react';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { LanguageProvider } from './i18n/LanguageContext';
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
      <LanguageProvider>
        <ThemeProvider>
          <AuthProvider>
            <div className="App">
              <Suspense fallback={<LoadingSpinner />}>
                <Dashboard onBack={handleBack} />
              </Suspense>
            </div>
          </AuthProvider>
        </ThemeProvider>
      </LanguageProvider>
    );
  }

  if (selectedTech) {
    return (
      <LanguageProvider>
        <ThemeProvider>
          <AuthProvider>
            <div className="App">
              <Suspense fallback={<LoadingSpinner />}>
                <Quiz selectedTechnology={selectedTech} onBack={handleBack} />
              </Suspense>
            </div>
          </AuthProvider>
        </ThemeProvider>
      </LanguageProvider>
    );
  }

  return (
    <LanguageProvider>
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
    </LanguageProvider>
  );
}

export default App;