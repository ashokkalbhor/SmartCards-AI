import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { CreditCard, Search, Plus, ArrowLeft, AlertCircle, CheckCircle, Calendar, DollarSign, Percent, Shield, Eye } from 'lucide-react';
import { cardMasterDataAPI, creditCardsAPI } from '../../services/api';

interface MasterCard {
  id: number;
  bank_name: string;
  card_name: string;
  display_name: string;
  card_network: string;
  joining_fee_display: string;
  annual_fee_display: string;
  annual_fee: number;
}

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

const AddCardPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const initialMode = searchParams.get('mode') === 'quick' ? 'quick' : 'select';
  const [addMode, setAddMode] = useState<'select' | 'quick' | 'manual'>(initialMode);
  const [masterCards, setMasterCards] = useState<MasterCard[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMasterCard, setSelectedMasterCard] = useState<MasterCard | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [addedCards, setAddedCards] = useState<Set<number>>(new Set());

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

  // Fetch master card data for quick add
  useEffect(() => {
    if (addMode === 'quick') {
      fetchMasterCards();
    }
  }, [addMode]);

  const fetchMasterCards = async () => {
    try {
      setLoading(true);
      const data = await cardMasterDataAPI.getCards();
      setMasterCards(data);
    } catch (err) {
      setError('Failed to load card options. Please try manual entry.');
    } finally {
      setLoading(false);
    }
  };

  const filteredCards = masterCards.filter(card =>
    card.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    card.bank_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleMasterCardSelect = (card: MasterCard) => {
    setSelectedMasterCard(card);
    setFormData(prev => ({
      ...prev,
      card_name: card.display_name,
      card_type: card.card_network,
      card_network: card.card_network,
      annual_fee: card.annual_fee || 0,
    }));
  };

  const handleQuickAddCard = async (card: MasterCard) => {
    try {
      setSubmitting(true);
      setError(null);
      
      // Create minimal card data for quick add
      const quickCardData = {
        card_name: card.display_name,
        card_type: card.card_network,
        card_network: card.card_network,
        card_number_last4: '0000', // Default placeholder
        card_holder_name: 'Card Holder', // Default placeholder
        expiry_month: 12,
        expiry_year: new Date().getFullYear() + 3,
        current_balance: 0,
        annual_fee: card.annual_fee || 0,
        reward_rate_general: 1.0,
        is_default: false,
        is_primary: false,
      };

      await creditCardsAPI.addCard(quickCardData);
      
      // Mark card as added
      setAddedCards(prev => new Set([...Array.from(prev), card.id]));
      
      // Clear any previous errors
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add card. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

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
    if (!validateForm()) return;

    try {
      setSubmitting(true);
      setError(null);
      await creditCardsAPI.addCard(formData);
      setSuccess(true);
      setTimeout(() => {
        navigate('/cards');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add card. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 text-center max-w-md"
          {...({} as any)}
        >
          <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Card Added Successfully!</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">Your credit card has been added to your portfolio.</p>
          <p className="text-sm text-gray-500 dark:text-gray-400">Redirecting to your cards...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/cards')}
            className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Cards</span>
          </button>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Add New Credit Card</h1>
          <p className="text-gray-600 dark:text-gray-300">Choose how you'd like to add your credit card</p>
        </div>

        {addMode === 'select' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid md:grid-cols-2 gap-6"
            {...({} as any)}
          >
            {/* Quick Add Option */}
            <motion.div
              whileHover={{ y: -4 }}
              onClick={() => setAddMode('quick')}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 cursor-pointer hover:shadow-xl transition-all"
              {...({} as any)}
            >
              <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center mx-auto mb-6">
                <Search className="w-8 h-8 text-primary-600 dark:text-primary-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3 text-center">Quick Add</h3>
              <p className="text-gray-600 dark:text-gray-300 text-center mb-4">
                Choose from our database of popular credit cards with pre-filled reward rates and benefits
              </p>
              <div className="flex items-center justify-center space-x-2 text-primary-600 dark:text-primary-400">
                <span className="text-sm font-medium">Recommended</span>
                <div className="w-2 h-2 bg-primary-600 dark:bg-primary-400 rounded-full"></div>
              </div>
            </motion.div>

            {/* Manual Add Option */}
            <motion.div
              whileHover={{ y: -4 }}
              onClick={() => setAddMode('manual')}
              className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-200 dark:border-gray-700 cursor-pointer hover:shadow-xl transition-all"
              {...({} as any)}
            >
              <div className="w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mx-auto mb-6">
                <Plus className="w-8 h-8 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3 text-center">Manual Entry</h3>
              <p className="text-gray-600 dark:text-gray-300 text-center mb-4">
                Manually enter your credit card details with custom reward rates and benefits
              </p>
              <div className="flex items-center justify-center space-x-2 text-green-600 dark:text-green-400">
                <span className="text-sm font-medium">Full Control</span>
                <div className="w-2 h-2 bg-green-600 dark:bg-green-400 rounded-full"></div>
              </div>
            </motion.div>
          </motion.div>
        )}

        {addMode === 'quick' && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700"
            {...({} as any)}
          >
            {!selectedMasterCard ? (
    <div className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Choose Your Card</h2>
                  {addedCards.size > 0 && (
                    <button
                      onClick={() => navigate('/cards')}
                      className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                    >
                      <Eye className="w-4 h-4" />
                      <span>View My Cards ({addedCards.size})</span>
                    </button>
                  )}
                </div>

                {/* Error Display */}
                {error && (
                  <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-center space-x-3 mb-4">
                    <AlertCircle className="w-5 h-5 text-red-500" />
                    <span className="text-red-700 dark:text-red-400">{error}</span>
                  </div>
                )}
                
                {/* Search */}
                <div className="relative mb-6">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 w-5 h-5" />
                  <input
                    type="text"
                    placeholder="Search for your credit card..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  />
                </div>

                {/* Cards List */}
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {loading ? (
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
                      <p className="text-gray-500 dark:text-gray-400 mt-2">Loading cards...</p>
                    </div>
                  ) : filteredCards.length === 0 ? (
                    <div className="text-center py-8">
                      <p className="text-gray-500 dark:text-gray-400">No cards found. Try manual entry instead.</p>
                    </div>
                  ) : (
                    filteredCards.map((card) => (
                      <div
                        key={card.id}
                        className="p-4 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                      >
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="font-semibold text-gray-900 dark:text-white">{card.display_name}</h3>
                            <p className="text-sm text-gray-600 dark:text-gray-400">{card.card_network}</p>
                          </div>
                          <div className="text-right mr-4">
                            <p className="text-sm text-gray-600 dark:text-gray-400">Annual Fee</p>
                            <p className="font-semibold text-gray-900 dark:text-white">{card.annual_fee_display}</p>
                          </div>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              if (!addedCards.has(card.id)) {
                                handleQuickAddCard(card);
                              }
                            }}
                            disabled={submitting || addedCards.has(card.id)}
                            className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors ${
                              addedCards.has(card.id)
                                ? 'bg-green-500 text-white cursor-default'
                                : 'bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white'
                            }`}
                          >
                            {submitting ? (
                              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                            ) : addedCards.has(card.id) ? (
                              <>
                                <CheckCircle className="w-4 h-4" />
                                <span>Added</span>
                              </>
                            ) : (
                              <>
                                <Plus className="w-4 h-4" />
                                <span>Add</span>
                              </>
                            )}
                          </button>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="p-6">
                <div className="mb-6">
                  <button
                    type="button"
                    onClick={() => setSelectedMasterCard(null)}
                    className="text-primary-600 dark:text-primary-400 hover:underline mb-2"
                  >
                    ← Choose different card
                  </button>
                  <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Add {selectedMasterCard.display_name}</h2>
                </div>

                <CardForm 
                  formData={formData}
                  handleInputChange={handleInputChange}
                  handleCardNumberChange={handleCardNumberChange}
                  error={error}
                  submitting={submitting}
                  isQuickAdd={true}
                />
              </form>
            )}
          </motion.div>
        )}

        {addMode === 'manual' && (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-gray-700"
        {...({} as any)}
      >
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">Manual Card Entry</h2>
            
            <form onSubmit={handleSubmit}>
              <CardForm 
                formData={formData}
                handleInputChange={handleInputChange}
                handleCardNumberChange={handleCardNumberChange}
                error={error}
                submitting={submitting}
                isQuickAdd={false}
              />
            </form>
          </motion.div>
        )}
      </div>
    </div>
  );
};

// Reusable Card Form Component
interface CardFormProps {
  formData: CardFormData;
  handleInputChange: (field: keyof CardFormData, value: any) => void;
  handleCardNumberChange: (value: string) => void;
  error: string | null;
  submitting: boolean;
  isQuickAdd: boolean;
}

const CardForm: React.FC<CardFormProps> = ({
  formData,
  handleInputChange,
  handleCardNumberChange,
  error,
  submitting,
  isQuickAdd
}) => {
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 20 }, (_, i) => currentYear + i);
  const months = Array.from({ length: 12 }, (_, i) => i + 1);

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-center space-x-3">
          <AlertCircle className="w-5 h-5 text-red-500" />
          <span className="text-red-700 dark:text-red-400">{error}</span>
        </div>
      )}

      {/* Basic Card Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Card Name *
          </label>
          <input
            type="text"
            value={formData.card_name}
            onChange={(e) => handleInputChange('card_name', e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            placeholder="e.g., HDFC Regalia Gold"
            disabled={isQuickAdd}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Card Network *
          </label>
          <select
            value={formData.card_network}
            onChange={(e) => handleInputChange('card_network', e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            disabled={isQuickAdd}
          >
            <option value="">Select Network</option>
            <option value="Visa">Visa</option>
            <option value="Mastercard">Mastercard</option>
            <option value="American Express">American Express</option>
            <option value="RuPay">RuPay</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Card Holder Name *
          </label>
          <input
            type="text"
            value={formData.card_holder_name}
            onChange={(e) => handleInputChange('card_holder_name', e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            placeholder="Name as on card"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Last 4 Digits *
          </label>
          <input
            type="text"
            value={formData.card_number_last4}
            onChange={(e) => handleCardNumberChange(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            placeholder="1234"
            maxLength={4}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Expiry Month *
          </label>
          <select
            value={formData.expiry_month}
            onChange={(e) => handleInputChange('expiry_month', parseInt(e.target.value))}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            {months.map(month => (
              <option key={month} value={month}>
                {month.toString().padStart(2, '0')}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Expiry Year *
          </label>
          <select
            value={formData.expiry_year}
            onChange={(e) => handleInputChange('expiry_year', parseInt(e.target.value))}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            {years.map(year => (
              <option key={year} value={year}>{year}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Financial Information */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <DollarSign className="w-5 h-5 mr-2" />
          Financial Details
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Credit Limit
            </label>
            <input
              type="number"
              value={formData.credit_limit || ''}
              onChange={(e) => handleInputChange('credit_limit', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              placeholder="500000"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Current Balance
            </label>
            <input
              type="number"
              value={formData.current_balance}
              onChange={(e) => handleInputChange('current_balance', parseFloat(e.target.value) || 0)}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              placeholder="0"
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
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              placeholder="0"
              disabled={isQuickAdd}
            />
          </div>
        </div>
      </div>

      {/* Reward Rates */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
          <Percent className="w-5 h-5 mr-2" />
          Reward Rates (%)
        </h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              General
            </label>
            <input
              type="number"
              step="0.1"
              value={formData.reward_rate_general}
              onChange={(e) => handleInputChange('reward_rate_general', parseFloat(e.target.value) || 1.0)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              disabled={isQuickAdd}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Dining
            </label>
            <input
              type="number"
              step="0.1"
              value={formData.reward_rate_dining || ''}
              onChange={(e) => handleInputChange('reward_rate_dining', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              disabled={isQuickAdd}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Groceries
            </label>
            <input
              type="number"
              step="0.1"
              value={formData.reward_rate_groceries || ''}
              onChange={(e) => handleInputChange('reward_rate_groceries', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              disabled={isQuickAdd}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Travel
            </label>
            <input
              type="number"
              step="0.1"
              value={formData.reward_rate_travel || ''}
              onChange={(e) => handleInputChange('reward_rate_travel', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              disabled={isQuickAdd}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Online Shopping
            </label>
            <input
              type="number"
              step="0.1"
              value={formData.reward_rate_online_shopping || ''}
              onChange={(e) => handleInputChange('reward_rate_online_shopping', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              disabled={isQuickAdd}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Fuel
            </label>
            <input
              type="number"
              step="0.1"
              value={formData.reward_rate_fuel || ''}
              onChange={(e) => handleInputChange('reward_rate_fuel', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              disabled={isQuickAdd}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Entertainment
            </label>
            <input
              type="number"
              step="0.1"
              value={formData.reward_rate_entertainment || ''}
              onChange={(e) => handleInputChange('reward_rate_entertainment', e.target.value ? parseFloat(e.target.value) : undefined)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              disabled={isQuickAdd}
            />
          </div>
        </div>
      </div>

      {/* Additional Information */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Additional Information</h3>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Notes
            </label>
            <textarea
              value={formData.notes || ''}
              onChange={(e) => handleInputChange('notes', e.target.value)}
              rows={3}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              placeholder="Any additional notes about this card..."
            />
          </div>

          <div className="flex items-center space-x-6">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.is_default}
                onChange={(e) => handleInputChange('is_default', e.target.checked)}
                className="rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">Set as default card</span>
            </label>

            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.is_primary}
                onChange={(e) => handleInputChange('is_primary', e.target.checked)}
                className="rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">Set as primary card</span>
            </label>
          </div>
        </div>
      </div>

      {/* Submit Button */}
      <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-primary-600 hover:bg-primary-700 disabled:bg-gray-400 text-white py-4 px-6 rounded-lg font-semibold text-lg transition-colors flex items-center justify-center space-x-2"
        >
          {submitting ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Adding Card...</span>
            </>
          ) : (
            <>
              <CreditCard className="w-5 h-5" />
              <span>Add Credit Card</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default AddCardPage; 