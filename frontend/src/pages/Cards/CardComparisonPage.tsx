import React, { useState, useEffect } from 'react';
import { Search, Filter, Download, Info, AlertCircle, Loader2 } from 'lucide-react';
import { cardMasterDataAPI } from '../../services/api';

interface CardData {
  id: number;
  bank_name: string;
  card_name: string;
  display_name: string;
  joining_fee_display: string;
  annual_fee_display: string;
  annual_fee_waiver_spend: number | null;
  domestic_lounge_visits: number | null;
  lounge_spend_requirement: number | null;
  lounge_spend_period: string | null;
  categories: Record<string, string>;
  merchants: Record<string, string>;
  additional_info: string;
}

const CardComparisonPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [cardData, setCardData] = useState<CardData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showUserCards, setShowUserCards] = useState(false);

  // Fetch card comparison data
  useEffect(() => {
    const fetchCardData = async () => {
      try {
        setLoading(true);
        const data = await cardMasterDataAPI.getComparison(showUserCards);
        setCardData(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching card data:', err);
        setError('Failed to load card comparison data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchCardData();
  }, [showUserCards]);

  // Helper function to get the color for a card based on bank
  const getCardColor = (bankName: string) => {
    const colors: Record<string, string> = {
      'SBI': 'bg-blue-50 border-blue-200',
      'HDFC': 'bg-orange-50 border-orange-200',
      'AXIS': 'bg-red-50 border-red-200',
      'ICICI': 'bg-green-50 border-green-200',
      'KOTAK': 'bg-purple-50 border-purple-200',
    };
    return colors[bankName.toUpperCase()] || 'bg-gray-50 border-gray-200';
  };

  // Helper function to format lounge visits
  const formatLoungeVisits = (card: CardData) => {
    if (!card.domestic_lounge_visits) return '-';
    return `${card.domestic_lounge_visits} visits/year`;
  };

  // Helper function to format lounge spend requirement
  const formatLoungeSpends = (card: CardData) => {
    if (!card.lounge_spend_requirement) return '-';
    const amount = card.lounge_spend_requirement;
    const period = card.lounge_spend_period || 'quarter';
    return `₹${(amount / 1000).toFixed(0)}K/${period}`;
  };

  // Get all unique categories and merchants for the table headers
  const allCategories = Array.from(
    new Set(cardData.flatMap(card => Object.keys(card.categories)))
  ).sort();
  
  const allMerchants = Array.from(
    new Set(cardData.flatMap(card => Object.keys(card.merchants)))
  ).sort();

  // Filter cards based on search term and category
  const filteredCards = cardData.filter(card => {
    const matchesSearch = card.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         card.bank_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || 
                           Object.keys(card.categories).includes(selectedCategory) ||
                           Object.keys(card.merchants).includes(selectedCategory);
    return matchesSearch && matchesCategory;
  });

  // Get color for reward rate
  const getCellColor = (value: string) => {
    if (value === '-' || value === '') return '';
    
    const numericValue = parseFloat(value.replace(/[^0-9.]/g, ''));
    if (numericValue >= 5) return 'text-green-600 font-semibold bg-green-50';
    if (numericValue >= 4) return 'text-blue-600 font-semibold bg-blue-50';
    if (numericValue >= 1.5) return 'text-yellow-600 font-semibold bg-yellow-50';
    return '';
  };

  // Export data to CSV
  const handleExport = () => {
    const headers = [
      'Card Name',
      'Bank',
      'Joining Fee',
      'Annual Fee',
      'Lounge Visits',
      'Lounge Spends',
      ...allCategories.map(cat => `Category: ${cat}`),
      ...allMerchants.map(merchant => `Merchant: ${merchant}`),
      'Additional Info'
    ];

    const csvData = filteredCards.map(card => [
      card.display_name,
      card.bank_name,
      card.joining_fee_display,
      card.annual_fee_display,
      formatLoungeVisits(card),
      formatLoungeSpends(card),
      ...allCategories.map(cat => card.categories[cat] || '-'),
      ...allMerchants.map(merchant => card.merchants[merchant] || '-'),
      card.additional_info
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + 
      [headers, ...csvData].map(row => row.join(",")).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "credit_cards_comparison.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading card comparison data...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Credit Card Comparison</h1>
          <p className="text-gray-600">Compare rewards, fees, and benefits across different credit cards</p>
        </div>

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <div className="flex flex-col sm:flex-row gap-4 flex-1">
              {/* Search */}
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search cards or banks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent w-full"
                />
              </div>

              {/* Category Filter */}
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="pl-10 pr-8 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">All Categories</option>
                  {allCategories.map(category => (
                    <option key={category} value={category}>
                      {category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </option>
                  ))}
                  {allMerchants.map(merchant => (
                    <option key={merchant} value={merchant}>
                      {merchant.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </option>
                  ))}
                </select>
              </div>

              {/* User Cards Toggle */}
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={showUserCards}
                  onChange={(e) => setShowUserCards(e.target.checked)}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <span className="text-sm text-gray-700">My Cards Only</span>
              </label>
            </div>

            {/* Export Button */}
            <button
              onClick={handleExport}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Download className="w-4 h-4" />
              Export CSV
            </button>
          </div>
        </div>

        {filteredCards.length === 0 ? (
          <div className="text-center py-12">
            <Info className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No cards found matching your criteria.</p>
          </div>
        ) : (
          /* Comparison Table */
          <div className="bg-white rounded-lg shadow-sm overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-gray-50">
                  <th className="text-left p-3 font-semibold sticky left-0 bg-gray-50 border-r min-w-[200px]">
                    Card Details
                  </th>
                  {filteredCards.map((card) => (
                    <th key={card.id} className={`p-3 text-center min-w-[140px] border-r ${getCardColor(card.bank_name)}`}>
                      <div className="font-semibold">{card.display_name}</div>
                      <div className="text-xs text-gray-600 mt-1">{card.bank_name}</div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Basic Information */}
                <tr className="border-b">
                  <td className="p-3 font-medium sticky left-0 bg-white border-r">Joining Fee</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-center border-r">{card.joining_fee_display}</td>
                  ))}
                </tr>
                <tr className="border-b">
                  <td className="p-3 font-medium sticky left-0 bg-white border-r">Annual Fee</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-center border-r">{card.annual_fee_display}</td>
                  ))}
                </tr>
                <tr className="border-b">
                  <td className="p-3 font-medium sticky left-0 bg-white border-r">Lounge Visits</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-center border-r">{formatLoungeVisits(card)}</td>
                  ))}
                </tr>
                <tr className="border-b">
                  <td className="p-3 font-medium sticky left-0 bg-white border-r">Lounge Spends</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-center border-r">{formatLoungeSpends(card)}</td>
                  ))}
                </tr>

                {/* Categories */}
                {allCategories.length > 0 && (
                  <>
                    <tr className="bg-blue-50">
                      <td className="p-3 font-semibold sticky left-0 bg-blue-50 border-r" colSpan={filteredCards.length + 1}>
                        Spending Categories
                      </td>
                    </tr>
                    {allCategories.map((category) => (
                      <tr key={category} className="border-b">
                        <td className="p-3 font-medium sticky left-0 bg-white border-r">
                          {category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </td>
                        {filteredCards.map((card) => (
                          <td key={card.id} className={`p-3 text-center border-r ${getCellColor(card.categories[category] || '-')}`}>
                            {card.categories[category] || '-'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </>
                )}

                {/* Merchants */}
                {allMerchants.length > 0 && (
                  <>
                    <tr className="bg-green-50">
                      <td className="p-3 font-semibold sticky left-0 bg-green-50 border-r" colSpan={filteredCards.length + 1}>
                        Merchant Rewards
                      </td>
                    </tr>
                    {allMerchants.map((merchant) => (
                      <tr key={merchant} className="border-b">
                        <td className="p-3 font-medium sticky left-0 bg-white border-r">
                          {merchant.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </td>
                        {filteredCards.map((card) => (
                          <td key={card.id} className={`p-3 text-center border-r ${getCellColor(card.merchants[merchant] || '-')}`}>
                            {card.merchants[merchant] || '-'}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </>
                )}

                {/* Additional Info */}
                <tr className="bg-yellow-50">
                  <td className="p-3 font-semibold sticky left-0 bg-yellow-50 border-r">Additional Info</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-xs text-center border-r max-w-[140px]">
                      <div className="break-words">{card.additional_info || '-'}</div>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </div>
        )}

        {/* Legend */}
        <div className="mt-6 p-4 bg-white rounded-lg shadow-sm">
          <h3 className="font-semibold mb-3">Reward Rate Legend:</h3>
          <div className="flex flex-wrap gap-4 text-sm">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-green-50 border border-green-200 rounded"></div>
              <span>5%+ Excellent</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-blue-50 border border-blue-200 rounded"></div>
              <span>4%+ Very Good</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-yellow-50 border border-yellow-200 rounded"></div>
              <span>1.5%+ Good</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-gray-50 border border-gray-200 rounded"></div>
              <span>Below 1.5% or N/A</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CardComparisonPage; 