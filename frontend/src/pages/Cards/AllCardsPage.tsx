import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Search, Star, CreditCard, Eye, ArrowLeft } from 'lucide-react';
import { cardMasterDataAPI } from '../../services/api';
import LoadingSpinner from '../../components/UI/LoadingSpinner';

interface CardData {
  id: number;
  bank_name: string;
  card_name: string;
  card_variant?: string;
  display_name: string;
  card_network: string;
  card_tier: string;
  joining_fee?: number;
  annual_fee?: number;
  is_lifetime_free: boolean;
  joining_fee_display: string;
  annual_fee_display: string;
  description?: string;
  is_active: boolean;
}

const AllCardsPage: React.FC = () => {
  const navigate = useNavigate();
  const [cards, setCards] = useState<CardData[]>([]);
  const [filteredCards, setFilteredCards] = useState<CardData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBank, setSelectedBank] = useState('');
  const [selectedTier, setSelectedTier] = useState('');
  const [banks, setBanks] = useState<string[]>([]);

  useEffect(() => {
    loadCards();
  }, []);

  const loadCards = async () => {
    try {
      setLoading(true);
      const response = await cardMasterDataAPI.getCards();
      // API returns array directly, not {cards: [...]}
      const activeCards = Array.isArray(response) ? response.filter((card: CardData) => card.is_active) : response.cards?.filter((card: CardData) => card.is_active) || [];
      setCards(activeCards);
      setFilteredCards(activeCards);
      
      // Extract unique banks
      const uniqueBanks = Array.from(new Set(activeCards.map((card: CardData) => card.bank_name))).sort() as string[];
      setBanks(uniqueBanks);
    } catch (error) {
      console.error('Error loading cards:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let filtered = cards;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(card =>
        card.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        card.bank_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        card.description?.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by bank
    if (selectedBank) {
      filtered = filtered.filter(card => card.bank_name === selectedBank);
    }

    // Filter by tier
    if (selectedTier) {
      filtered = filtered.filter(card => card.card_tier === selectedTier);
    }

    setFilteredCards(filtered);
  }, [cards, searchTerm, selectedBank, selectedTier]);

  const handleCardClick = (cardId: number) => {
    navigate(`/card/${cardId}`);
  };

  const renderStars = (tier: string) => {
    const tierMap: { [key: string]: number } = {
      'basic': 1,
      'premium': 2,
      'super_premium': 3,
      'elite': 4
    };
    
    const stars = [];
    const starCount = tierMap[tier] || 1;
    
    for (let i = 1; i <= 4; i++) {
      stars.push(
        <Star
          key={i}
          className={`w-3 h-3 ${
            i <= starCount ? 'text-yellow-400 fill-current' : 'text-gray-300'
          }`}
        />
      );
    }
    return stars;
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Dashboard</span>
          </button>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Credit Card Community</h1>
          <p className="text-gray-600 dark:text-gray-300">Explore and discover credit cards from various banks</p>
        </div>

        {/* Main Content - Exactly like AddCardPage */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700"
          {...({} as any)}
        >
          <div className="p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Browse All Cards</h2>
              <div className="text-sm text-gray-500 dark:text-gray-400">
                {filteredCards.length} cards found
              </div>
            </div>

            {/* Search - Exactly like AddCardPage */}
            <div className="relative mb-6">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 w-5 h-5" />
              <input
                type="text"
                placeholder="Search for credit cards..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            {/* Filters */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              {/* Bank Filter */}
              <select
                value={selectedBank}
                onChange={(e) => setSelectedBank(e.target.value)}
                className="px-3 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">All Banks</option>
                {banks.map(bank => (
                  <option key={bank} value={bank}>{bank}</option>
                ))}
              </select>

              {/* Tier Filter */}
              <select
                value={selectedTier}
                onChange={(e) => setSelectedTier(e.target.value)}
                className="px-3 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">All Tiers</option>
                <option value="basic">Basic</option>
                <option value="premium">Premium</option>
                <option value="super_premium">Super Premium</option>
                <option value="elite">Elite</option>
              </select>

              {/* Clear Filters */}
              {(searchTerm || selectedBank || selectedTier) && (
                <button
                  onClick={() => {
                    setSearchTerm('');
                    setSelectedBank('');
                    setSelectedTier('');
                  }}
                  className="px-4 py-3 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  Clear Filters
                </button>
              )}
            </div>

            {/* Cards List - Exactly like AddCardPage */}
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {filteredCards.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-500 dark:text-gray-400">No cards found. Try adjusting your search criteria.</p>
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
                        onClick={() => handleCardClick(card.id)}
                        className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg flex items-center space-x-2 transition-colors"
                      >
                        <Eye className="w-4 h-4" />
                        <span>View Details</span>
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default AllCardsPage; 