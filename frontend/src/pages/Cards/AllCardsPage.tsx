import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Search, Star, CreditCard, ArrowLeft, X, SlidersHorizontal } from 'lucide-react';
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

const TIER_CONFIG: Record<string, { label: string; stars: number; color: string }> = {
  basic:         { label: 'Basic',         stars: 1, color: 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300' },
  premium:       { label: 'Premium',       stars: 2, color: 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300' },
  super_premium: { label: 'Super Premium', stars: 3, color: 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300' },
  elite:         { label: 'Elite',         stars: 4, color: 'bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300' },
};

const NETWORK_COLOR: Record<string, string> = {
  Visa:       'bg-blue-600',
  Mastercard: 'bg-red-500',
  Amex:       'bg-green-600',
  RuPay:      'bg-orange-500',
};

const AllCardsPage: React.FC = () => {
  const navigate = useNavigate();
  const [cards, setCards] = useState<CardData[]>([]);
  const [filteredCards, setFilteredCards] = useState<CardData[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBank, setSelectedBank] = useState('');
  const [selectedTier, setSelectedTier] = useState('');
  const [banks, setBanks] = useState<string[]>([]);

  useEffect(() => { loadCards(); }, []);

  const loadCards = async () => {
    try {
      setLoading(true);
      const response = await cardMasterDataAPI.getCards(undefined, undefined, undefined);
      const allCards = Array.isArray(response) ? response : response.cards || [];
      setCards(allCards);
      setFilteredCards(allCards);
      setBanks(Array.from(new Set(allCards.map((c: CardData) => c.bank_name))).sort() as string[]);
    } catch (error) {
      console.error('Error loading cards:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let filtered = cards;
    if (searchTerm)    filtered = filtered.filter(c => c.display_name.toLowerCase().includes(searchTerm.toLowerCase()) || c.bank_name.toLowerCase().includes(searchTerm.toLowerCase()) || c.description?.toLowerCase().includes(searchTerm.toLowerCase()));
    if (selectedBank)  filtered = filtered.filter(c => c.bank_name === selectedBank);
    if (selectedTier)  filtered = filtered.filter(c => c.card_tier === selectedTier);
    setFilteredCards(filtered);
  }, [cards, searchTerm, selectedBank, selectedTier]);

  const hasFilters = !!(searchTerm || selectedBank || selectedTier);
  const clearFilters = () => { setSearchTerm(''); setSelectedBank(''); setSelectedTier(''); };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center space-x-2 text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white mb-4 transition-colors text-sm"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Dashboard</span>
          </button>
          <div className="flex items-end justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Credit Cards</h1>
              <p className="text-gray-500 dark:text-gray-400 mt-1">Explore and compare cards from leading banks</p>
            </div>
            <span className="text-sm font-medium text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-3 py-1 rounded-full shadow-sm">
              {filteredCards.length} {filteredCards.length === 1 ? 'card' : 'cards'}
            </span>
          </div>
        </div>

        {/* Search + Filters */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-4 mb-8">
          <div className="flex flex-col md:flex-row gap-3">
            {/* Search */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
              <input
                type="text"
                placeholder="Search by card name, bank..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 text-sm border border-gray-200 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400"
              />
            </div>

            {/* Bank filter */}
            <div className="relative">
              <SlidersHorizontal className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
              <select
                value={selectedBank}
                onChange={e => setSelectedBank(e.target.value)}
                className="pl-9 pr-8 py-2.5 text-sm border border-gray-200 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white appearance-none cursor-pointer"
              >
                <option value="">All Banks</option>
                {banks.map(bank => <option key={bank} value={bank}>{bank}</option>)}
              </select>
            </div>

            {/* Tier filter */}
            <select
              value={selectedTier}
              onChange={e => setSelectedTier(e.target.value)}
              className="px-4 py-2.5 text-sm border border-gray-200 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white appearance-none cursor-pointer"
            >
              <option value="">All Tiers</option>
              <option value="basic">Basic</option>
              <option value="premium">Premium</option>
              <option value="super_premium">Super Premium</option>
              <option value="elite">Elite</option>
            </select>

            {/* Clear */}
            {hasFilters && (
              <button
                onClick={clearFilters}
                className="flex items-center space-x-1.5 px-4 py-2.5 text-sm text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 border border-gray-200 dark:border-gray-600 rounded-lg hover:border-red-300 dark:hover:border-red-700 transition-colors"
              >
                <X className="w-3.5 h-3.5" />
                <span>Clear</span>
              </button>
            )}
          </div>
        </div>

        {/* Cards Grid */}
        {filteredCards.length === 0 ? (
          <div className="text-center py-20">
            <CreditCard className="w-12 h-12 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
            <p className="text-gray-500 dark:text-gray-400 text-lg font-medium">No cards match your filters</p>
            <p className="text-gray-400 dark:text-gray-500 text-sm mt-1">Try adjusting your search or filters</p>
            {hasFilters && (
              <button onClick={clearFilters} className="mt-4 text-primary-600 dark:text-primary-400 text-sm hover:underline">
                Clear all filters
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {filteredCards.map((card, index) => {
              const tier = TIER_CONFIG[card.card_tier] || TIER_CONFIG.basic;
              const networkColor = NETWORK_COLOR[card.card_network] || 'bg-gray-500';
              return (
                <motion.div
                  key={card.id}
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.03 }}
                  onClick={() => navigate(`/card/${card.id}`)}
                  className="group bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 cursor-pointer overflow-hidden"
                  {...({} as any)}
                >
                  {/* Card top accent bar */}
                  <div className={`h-1 bg-gradient-to-r ${card.is_active ? 'from-primary-500 to-primary-400' : 'from-amber-400 to-amber-300'}`} />

                  <div className="p-5">
                    {/* Bank + Network */}
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide">
                        {card.bank_name}
                      </span>
                      <div className="flex items-center gap-1.5">
                        {!card.is_active && (
                          <span className="text-xs font-semibold text-amber-700 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 px-2 py-0.5 rounded-full">
                            Outdated Data
                          </span>
                        )}
                        <span className={`text-xs font-bold text-white px-2 py-0.5 rounded-full ${networkColor}`}>
                          {card.card_network}
                        </span>
                      </div>
                    </div>

                    {/* Card Name */}
                    <h3 className="font-semibold text-gray-900 dark:text-white text-base leading-tight mb-1 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                      {card.card_name}
                    </h3>
                    {card.card_variant && (
                      <p className="text-xs text-gray-400 dark:text-gray-500 mb-3">{card.card_variant}</p>
                    )}

                    {/* Tier */}
                    <div className="flex items-center gap-2 mb-4">
                      <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${tier.color}`}>
                        {tier.label}
                      </span>
                      <div className="flex items-center gap-0.5">
                        {[1, 2, 3, 4].map(i => (
                          <Star key={i} className={`w-3 h-3 ${i <= tier.stars ? 'text-amber-400 fill-current' : 'text-gray-200 dark:text-gray-600'}`} />
                        ))}
                      </div>
                    </div>

                    {/* Fee row */}
                    <div className="flex items-center justify-between pt-3 border-t border-gray-100 dark:border-gray-700">
                      <div>
                        <p className="text-xs text-gray-400 dark:text-gray-500">Annual Fee</p>
                        <p className={`text-sm font-semibold ${card.is_lifetime_free ? 'text-green-600 dark:text-green-400' : 'text-gray-900 dark:text-white'}`}>
                          {card.annual_fee_display}
                        </p>
                      </div>
                      <span className="text-xs font-medium text-primary-600 dark:text-primary-400 group-hover:underline">
                        View Details →
                      </span>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default AllCardsPage;
