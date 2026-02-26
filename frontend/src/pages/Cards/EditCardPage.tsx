import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, CreditCard, AlertCircle, CheckCircle, Calendar, DollarSign, Percent, Shield, Eye } from 'lucide-react';
import { creditCardsAPI } from '../../services/api';

interface CardFormData {
  card_name: string;
  card_type: string;
  card_network: string;
  card_number_last4: string;
  card_holder_name: string;
  expiry_month: number;
  expiry_year: number;
  credit_limit?: number;
  current_balance: number;
  annual_fee: number;
  reward_rate_general: number;
  reward_rate_dining?: number;
  reward_rate_groceries?: number;
  reward_rate_travel?: number;
  reward_rate_online_shopping?: number;
  reward_rate_fuel?: number;
  reward_rate_entertainment?: number;
  notes?: string;
  is_default: boolean;
  is_primary: boolean;
}

const EditCardPage: React.FC = () => {
  const { cardId } = useParams<{ cardId: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const [formData, setFormData] = useState<CardFormData>({
    card_name: '',
    card_type: '',
    card_network: '',
    card_number_last4: '',
    card_holder_name: '',
    expiry_month: 1,
    expiry_year: new Date().getFullYear(),
    current_balance: 0,
    annual_fee: 0,
    reward_rate_general: 1.0,
    is_default: false,
    is_primary: false,
  });

  // Fetch existing card data
  useEffect(() => {
    const fetchCard = async () => {
      if (!cardId) return;
      
      try {
        setLoading(true);
        const card = await creditCardsAPI.getCard(cardId);
        
        // Map API response to form data
        setFormData({
          card_name: card.card_name,
          card_type: card.card_type,
          card_network: card.card_network,
          card_number_last4: card.card_number_last4,
          card_holder_name: card.card_holder_name,
          expiry_month: card.expiry_month,
          expiry_year: card.expiry_year,
          credit_limit: card.credit_limit || undefined,
          current_balance: card.current_balance || 0,
          annual_fee: card.annual_fee || 0,
          reward_rate_general: card.reward_rate_general || 1.0,
          reward_rate_dining: card.reward_rate_dining || undefined,
          reward_rate_groceries: card.reward_rate_groceries || undefined,
          reward_rate_travel: card.reward_rate_travel || undefined,
          reward_rate_online_shopping: card.reward_rate_online_shopping || undefined,
          reward_rate_fuel: card.reward_rate_fuel || undefined,
          reward_rate_entertainment: card.reward_rate_entertainment || undefined,
          notes: card.notes || undefined,
          is_default: card.is_default || false,
          is_primary: card.is_primary || false,
        });
      } catch (error) {
        console.error('Error fetching card:', error);
        setError('Failed to load card details');
      } finally {
        setLoading(false);
      }
    };

    fetchCard();
  }, [cardId]);

  const handleInputChange = (field: keyof CardFormData, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const detectCardNetwork = (cardNumber: string) => {
    if (cardNumber.startsWith('4')) return 'Visa';
    if (cardNumber.startsWith('5') || cardNumber.startsWith('2')) return 'Mastercard';
    if (cardNumber.startsWith('3')) return 'American Express';
    if (cardNumber.startsWith('6')) return 'RuPay';
    return '';
  };

  const handleCardNumberChange = (value: string) => {
    const numericValue = value.replace(/\D/g, '');
    if (numericValue.length <= 4) {
      handleInputChange('card_number_last4', numericValue);
      if (numericValue.length >= 1) {
        const network = detectCardNetwork(numericValue);
        if (network && !formData.card_network) {
          handleInputChange('card_network', network);
        }
      }
    }
  };

  const validateForm = (): boolean => {
    if (!formData.card_name.trim()) {
      setError('Card name is required');
      return false;
    }
    if (!formData.card_holder_name.trim()) {
      setError('Card holder name is required');
      return false;
    }
    if (!formData.card_number_last4 || formData.card_number_last4.length !== 4) {
      setError('Last 4 digits of card number are required');
      return false;
    }
    if (formData.expiry_month < 1 || formData.expiry_month > 12) {
      setError('Valid expiry month is required');
      return false;
    }
    if (formData.expiry_year < new Date().getFullYear()) {
      setError('Card appears to be expired');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm() || !cardId) return;

    try {
      setSubmitting(true);
      setError(null);
      await creditCardsAPI.updateCard(cardId, formData);
      setSuccess(true);
      setTimeout(() => {
        navigate('/cards');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update card. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="text-center">Loading card details...</div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center space-x-4">
        <button
          onClick={() => navigate(`/cards/${cardId}`)}
          className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <ArrowLeft className="h-6 w-6" />
        </button>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Edit Card</h1>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-center space-x-3"
          {...({} as any)}
        >
          <AlertCircle className="h-5 w-5 text-red-500" />
          <span className="text-red-700 dark:text-red-400">{error}</span>
        </motion.div>
      )}

      {success && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4 flex items-center space-x-3"
          {...({} as any)}
        >
          <CheckCircle className="h-5 w-5 text-green-500" />
          <span className="text-green-700 dark:text-green-400">Card updated successfully!</span>
        </motion.div>
      )}

      <motion.form
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        onSubmit={handleSubmit}
        className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 space-y-6"
        {...({} as any)}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Card Information */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center space-x-2">
              <CreditCard className="h-5 w-5" />
              <span>Card Information</span>
            </h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Card Name
              </label>
              <input
                type="text"
                value={formData.card_name}
                onChange={(e) => handleInputChange('card_name', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Enter card name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Card Holder Name
              </label>
              <input
                type="text"
                value={formData.card_holder_name}
                onChange={(e) => handleInputChange('card_holder_name', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Enter card holder name"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Last 4 Digits
              </label>
              <input
                type="text"
                value={formData.card_number_last4}
                onChange={(e) => handleCardNumberChange(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="1234"
                maxLength={4}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Expiry Month
                </label>
                <select
                  value={formData.expiry_month}
                  onChange={(e) => handleInputChange('expiry_month', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                  {Array.from({ length: 12 }, (_, i) => i + 1).map(month => (
                    <option key={month} value={month}>
                      {month.toString().padStart(2, '0')}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Expiry Year
                </label>
                <select
                  value={formData.expiry_year}
                  onChange={(e) => handleInputChange('expiry_year', parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                >
                  {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() + i).map(year => (
                    <option key={year} value={year}>
                      {year}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Financial Details */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center space-x-2">
              <DollarSign className="h-5 w-5" />
              <span>Financial Details</span>
            </h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Current Balance
              </label>
              <input
                type="number"
                value={formData.current_balance}
                onChange={(e) => handleInputChange('current_balance', parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="0.00"
                step="0.01"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Credit Limit
              </label>
              <input
                type="number"
                value={formData.credit_limit || ''}
                onChange={(e) => handleInputChange('credit_limit', e.target.value ? parseFloat(e.target.value) : undefined)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Enter credit limit"
                step="0.01"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Annual Fee
              </label>
              <input
                type="number"
                value={formData.annual_fee}
                onChange={(e) => handleInputChange('annual_fee', parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="0.00"
                step="0.01"
              />
            </div>
          </div>
        </div>

        {/* Reward Rates */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center space-x-2">
            <Percent className="h-5 w-5" />
            <span>Reward Rates (%)</span>
          </h3>
          
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                General
              </label>
              <input
                type="number"
                value={formData.reward_rate_general}
                onChange={(e) => handleInputChange('reward_rate_general', parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="1.0"
                step="0.1"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Dining
              </label>
              <input
                type="number"
                value={formData.reward_rate_dining || ''}
                onChange={(e) => handleInputChange('reward_rate_dining', e.target.value ? parseFloat(e.target.value) : undefined)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Optional"
                step="0.1"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Groceries
              </label>
              <input
                type="number"
                value={formData.reward_rate_groceries || ''}
                onChange={(e) => handleInputChange('reward_rate_groceries', e.target.value ? parseFloat(e.target.value) : undefined)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Optional"
                step="0.1"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Travel
              </label>
              <input
                type="number"
                value={formData.reward_rate_travel || ''}
                onChange={(e) => handleInputChange('reward_rate_travel', e.target.value ? parseFloat(e.target.value) : undefined)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Optional"
                step="0.1"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Online Shopping
              </label>
              <input
                type="number"
                value={formData.reward_rate_online_shopping || ''}
                onChange={(e) => handleInputChange('reward_rate_online_shopping', e.target.value ? parseFloat(e.target.value) : undefined)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Optional"
                step="0.1"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Fuel
              </label>
              <input
                type="number"
                value={formData.reward_rate_fuel || ''}
                onChange={(e) => handleInputChange('reward_rate_fuel', e.target.value ? parseFloat(e.target.value) : undefined)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder="Optional"
                step="0.1"
              />
            </div>
          </div>
        </div>

        {/* Card Settings */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center space-x-2">
            <Shield className="h-5 w-5" />
            <span>Card Settings</span>
          </h3>
          
          <div className="flex items-center space-x-6">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.is_default}
                onChange={(e) => handleInputChange('is_default', e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">Set as default card</span>
            </label>
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.is_primary}
                onChange={(e) => handleInputChange('is_primary', e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">Primary card</span>
            </label>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate(`/cards/${cardId}`)}
            className="px-6 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {submitting ? 'Updating...' : 'Update Card'}
          </button>
        </div>
      </motion.form>
    </div>
  );
};

export default EditCardPage; 