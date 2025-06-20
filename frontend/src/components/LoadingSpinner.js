import React from 'react';

const LoadingSpinner = () => (
  <div className="min-h-screen bg-white dark:bg-gray-900 flex items-center justify-center transition-colors duration-200">
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-500 dark:border-blue-400 mx-auto mb-4"></div>
      <p className="text-lg text-gray-700 dark:text-gray-300">Chargement...</p>
    </div>
  </div>
);

export default LoadingSpinner;