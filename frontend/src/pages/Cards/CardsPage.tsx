import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus, CreditCard, Edit, Trash2, Eye, BarChart3 } from 'lucide-react';
import { formatRupees } from '../../utils/currency';

const CardsPage: React.FC = () => {
  const navigate = useNavigate();
  
  const cards = [
    { id: 1, name: 'HDFC Regalia Gold', type: 'Visa', last4: '1234', rewards: 15680.00, limit: 500000 },
    { id: 2, name: 'SBI Elite', type: 'Mastercard', last4: '5678', rewards: 8945.00, limit: 750000 },
    { id: 3, name: 'ICICI Amazon Pay', type: 'Visa', last4: '9012', rewards: 3850.00, limit: 300000 },
  ];

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Cards</h1>
        <div className="flex items-center space-x-3">
          <button 
            onClick={() => navigate('/cards/compare')}
            className="border border-primary-600 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
          >
            <BarChart3 className="h-5 w-5" />
            <span>Compare Cards</span>
          </button>
          <button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2">
            <Plus className="h-5 w-5" />
            <span>Add Card</span>
          </button>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cards.map((card) => (
          <motion.div
            key={card.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
            {...({} as any)}
          >
            <div className="flex items-center justify-between mb-4">
              <CreditCard className="h-8 w-8 text-primary-600 dark:text-primary-400" />
              <div className="flex space-x-2">
                <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                  <Eye className="h-4 w-4" />
                </button>
                <button className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                  <Edit className="h-4 w-4" />
                </button>
                <button className="p-2 text-red-400 hover:text-red-600">
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{card.name}</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">•••• •••• •••• {card.last4}</p>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">Rewards</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">{formatRupees(card.rewards)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500 dark:text-gray-400">Limit</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">{formatRupees(card.limit, false)}</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default CardsPage; 