import React from 'react';
import { motion } from 'framer-motion';

const AddCardPage: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Add New Card</h1>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 max-w-2xl"
        {...({} as any)}
      >
        <p className="text-gray-600 dark:text-gray-400 mb-6">Add a new credit card to your portfolio</p>
        {/* Form will be implemented here */}
        <div className="text-center py-8">
          <p className="text-gray-500 dark:text-gray-400">Form coming soon...</p>
        </div>
      </motion.div>
    </div>
  );
};

export default AddCardPage; 