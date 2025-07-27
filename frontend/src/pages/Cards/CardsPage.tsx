import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Plus, CreditCard, Edit, Trash2, Eye, BarChart3 } from 'lucide-react';
import { formatRupees } from '../../utils/currency';
import { creditCardsAPI } from '../../services/api';

interface Card {
  id: number;
  card_name: string;
  card_network: string;
  card_number_last4: string;
  current_balance: number | null;
  credit_limit: number | null;
  reward_rate_general: number | null;
}

const CardsPage: React.FC = () => {
  const navigate = useNavigate();
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchCards = async () => {
      try {
        const data = await creditCardsAPI.getCards();
        // Sort cards alphabetically by card_name
        const sortedCards = data.sort((a: Card, b: Card) => a.card_name.localeCompare(b.card_name));
        setCards(sortedCards);
      } catch (error) {
        console.error('Error fetching cards:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchCards();
  }, []);

  // Refresh cards when returning from add card page
  useEffect(() => {
    const handleFocus = () => {
      // Refresh cards when window regains focus (user returns from add card page)
      const fetchCards = async () => {
        try {
          const data = await creditCardsAPI.getCards();
          // Sort cards alphabetically by card_name
          const sortedCards = data.sort((a: Card, b: Card) => a.card_name.localeCompare(b.card_name));
          setCards(sortedCards);
        } catch (error) {
          console.error('Error fetching cards:', error);
        }
      };
      fetchCards();
    };

    window.addEventListener('focus', handleFocus);
    return () => window.removeEventListener('focus', handleFocus);
  }, []);

  const handleViewCard = (cardId: number) => {
    navigate(`/cards/${cardId}`);
  };

  const handleEditCard = (cardId: number) => {
    navigate(`/cards/${cardId}/edit`);
  };

  const handleDeleteCard = async (cardId: number) => {
    if (window.confirm('Are you sure you want to delete this card?')) {
      try {
        await creditCardsAPI.deleteCard(cardId.toString());
        // Refresh the cards list after deletion
        const updatedCards = cards.filter(card => card.id !== cardId);
        setCards(updatedCards);
      } catch (error) {
        console.error('Error deleting card:', error);
        alert('Failed to delete card. Please try again.');
      }
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-center">Loading cards...</div>
      </div>
    );
  }

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
          <button 
            onClick={() => navigate('/cards/add?mode=quick')}
            className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
          >
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
                <button 
                  onClick={() => handleViewCard(card.id)}
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <Eye className="h-4 w-4" />
                </button>
                <button 
                  onClick={() => handleEditCard(card.id)}
                  className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <Edit className="h-4 w-4" />
                </button>
                <button 
                  onClick={() => handleDeleteCard(card.id)}
                  className="p-2 text-red-400 hover:text-red-600"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">{card.card_name}</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">•••• •••• •••• {card.card_number_last4}</p>
                          <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500 dark:text-gray-400">Rewards</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {card.reward_rate_general ? formatRupees(card.reward_rate_general) : '₹0'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-500 dark:text-gray-400">Limit</span>
                  <span className="text-sm font-medium text-gray-900 dark:text-white">
                    {card.credit_limit ? formatRupees(card.credit_limit, false) : '₹0'}
                  </span>
                </div>
              </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default CardsPage; 