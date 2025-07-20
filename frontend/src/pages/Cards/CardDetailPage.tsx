import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, CreditCard, Edit, Trash2 } from 'lucide-react';
import { formatRupees } from '../../utils/currency';
import { creditCardsAPI } from '../../services/api';

interface Card {
  id: number;
  card_name: string;
  card_network: string;
  card_number_last4: string;
  card_holder_name: string;
  expiry_month: number;
  expiry_year: number;
  current_balance: number | null;
  credit_limit: number | null;
  available_credit: number | null;
  reward_rate_general: number | null;
  reward_rate_dining: number | null;
  reward_rate_groceries: number | null;
  reward_rate_travel: number | null;
  annual_fee: number | null;
  due_date: string | null;
  minimum_payment: number | null;
  is_active: boolean;
  created_at: string;
}

const CardDetailPage: React.FC = () => {
  const { cardId } = useParams<{ cardId: string }>();
  const navigate = useNavigate();
  const [card, setCard] = useState<Card | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch existing card data
  useEffect(() => {
    const fetchCard = async () => {
      if (!cardId) return;
      
      try {
        setLoading(true);
        console.log('Fetching card with ID:', cardId);
        const card = await creditCardsAPI.getCard(cardId);
        console.log('Card data received:', card);
        setCard(card);
      } catch (error: any) {
        console.error('Error fetching card:', error);
        console.error('Error details:', error.response?.data);
      } finally {
        setLoading(false);
      }
    };

    fetchCard();
  }, [cardId]);

  const handleEdit = () => {
    navigate(`/cards/${cardId}/edit`);
  };

  const handleDelete = async () => {
    if (!cardId || !window.confirm('Are you sure you want to delete this card?')) return;
    
    try {
      await creditCardsAPI.deleteCard(cardId);
      navigate('/cards');
    } catch (error) {
      console.error('Error deleting card:', error);
      alert('Failed to delete card. Please try again.');
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-center">Loading card details...</div>
      </div>
    );
  }

  if (!card) {
    return (
      <div className="p-6">
        <div className="text-center text-red-600">Card not found</div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <button
          onClick={() => navigate('/cards')}
          className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <ArrowLeft className="h-6 w-6" />
        </button>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{card.card_name}</h1>
        <div className="flex space-x-2 ml-auto">
          <button
            onClick={handleEdit}
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <Edit className="h-5 w-5" />
          </button>
          <button
            onClick={handleDelete}
            className="p-2 text-red-400 hover:text-red-600"
          >
            <Trash2 className="h-5 w-5" />
          </button>
        </div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        {...({} as any)}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Card Information</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Card Number</span>
                  <span className="font-medium">•••• •••• •••• {card.card_number_last4}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Card Holder</span>
                  <span className="font-medium">{card.card_holder_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Expiry Date</span>
                  <span className="font-medium">{card.expiry_month.toString().padStart(2, '0')}/{card.expiry_year}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Network</span>
                  <span className="font-medium">{card.card_network}</span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Financial Details</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Current Balance</span>
                  <span className="font-medium">{card.current_balance ? formatRupees(card.current_balance) : '₹0'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Credit Limit</span>
                  <span className="font-medium">{card.credit_limit ? formatRupees(card.credit_limit, false) : '₹0'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Available Credit</span>
                  <span className="font-medium">{card.available_credit ? formatRupees(card.available_credit, false) : '₹0'}</span>
                </div>
                {card.due_date && (
                  <div className="flex justify-between">
                    <span className="text-gray-500 dark:text-gray-400">Due Date</span>
                    <span className="font-medium">{new Date(card.due_date).toLocaleDateString()}</span>
                  </div>
                )}
                {card.minimum_payment && (
                  <div className="flex justify-between">
                    <span className="text-gray-500 dark:text-gray-400">Minimum Payment</span>
                    <span className="font-medium">{formatRupees(card.minimum_payment)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Reward Rates</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">General</span>
                  <span className="font-medium">{card.reward_rate_general ? `${card.reward_rate_general}%` : 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Dining</span>
                  <span className="font-medium">{card.reward_rate_dining ? `${card.reward_rate_dining}%` : 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Groceries</span>
                  <span className="font-medium">{card.reward_rate_groceries ? `${card.reward_rate_groceries}%` : 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Travel</span>
                  <span className="font-medium">{card.reward_rate_travel ? `${card.reward_rate_travel}%` : 'N/A'}</span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Card Details</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Annual Fee</span>
                  <span className="font-medium">{card.annual_fee ? formatRupees(card.annual_fee) : '₹0'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Status</span>
                  <span className={`font-medium ${card.is_active ? 'text-green-600' : 'text-red-600'}`}>
                    {card.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500 dark:text-gray-400">Added On</span>
                  <span className="font-medium">{new Date(card.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default CardDetailPage; 