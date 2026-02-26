import React from 'react';
import { motion } from 'framer-motion';

const RecommendationsPage: React.FC = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Recommendations</h1>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        {...({} as any)}
      >
        <p className="text-gray-600 dark:text-gray-400">AI-powered card recommendations will be displayed here</p>
      </motion.div>
    </div>
  );
};

export default RecommendationsPage; 