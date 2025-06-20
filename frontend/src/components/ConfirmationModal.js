import React from 'react';

const ConfirmationModal = React.memo(({ isOpen, onClose, onConfirm }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-sm w-full mx-4">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Êtes-vous sûr ?</h2>
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          Voulez-vous vraiment quitter le quiz ? Votre progression sera perdue.
        </p>
        <div className="flex justify-end space-x-4">
          <button
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-gray-700 dark:text-gray-300"
          >
            Annuler
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 bg-red-500 dark:bg-red-600 text-white rounded hover:bg-red-600 dark:hover:bg-red-500 transition-colors"
          >
            Quitter
          </button>
        </div>
      </div>
    </div>
  );
});

export default ConfirmationModal; 