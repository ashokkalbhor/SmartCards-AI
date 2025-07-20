import React, { useState, useEffect, useRef } from 'react';
import { Search, Filter, Download, Info, AlertCircle, Loader2, CreditCard } from 'lucide-react';
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
  const exportRef = useRef<HTMLDivElement>(null);

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
      'SBI': 'bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-800',
      'HDFC': 'bg-orange-50 border-orange-200 dark:bg-orange-900/20 dark:border-orange-800',
      'AXIS': 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800',
      'ICICI': 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800',
      'KOTAK': 'bg-purple-50 border-purple-200 dark:bg-purple-900/20 dark:border-purple-800',
    };
    return colors[bankName.toUpperCase()] || 'bg-gray-50 border-gray-200 dark:bg-gray-900/20 dark:border-gray-800';
  };

  // Helper function to get text color that contrasts well with card background
  const getCardTextColor = (bankName: string) => {
    // Use dark text for light backgrounds, light text for dark backgrounds
    return 'text-gray-900 dark:text-gray-100';
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

  // Get color for reward rate - highlight only the highest value(s) in each row
  const getCellColor = (value: string, rowValues: string[]) => {
    if (value === '-' || value === '') return '';
    
    // Get all numeric values in the row
    const numericValues = rowValues
      .map(v => v === '-' || v === '' ? 0 : parseFloat(v.replace(/[^0-9.]/g, '')))
      .filter(v => v > 0);
    
    if (numericValues.length === 0) return '';
    
    const maxValue = Math.max(...numericValues);
    const currentValue = parseFloat(value.replace(/[^0-9.]/g, ''));
    
    // Highlight only if this cell has the maximum value
    if (currentValue === maxValue && currentValue > 0) {
      return 'text-green-600 font-semibold bg-green-50 dark:bg-green-900/20 dark:text-green-400';
    }
    
    return '';
  };

  // Export table as image with branding
  const handleExport = () => {
    if (!exportRef.current) return;

    // Create a new window for printing/saving as image
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;

    const currentDate = new Date().toLocaleDateString();
    const brandingStyles = `
      <style>
        body { 
          font-family: 'Inter', system-ui, sans-serif; 
          margin: 20px; 
          background: white;
        }
        .export-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 20px;
          padding-bottom: 15px;
          border-bottom: 2px solid #0284c7;
        }
        .brand-section {
          display: flex;
          align-items: center;
          gap: 10px;
        }
        .brand-icon {
          width: 32px;
          height: 32px;
          background: #0284c7;
          border-radius: 6px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-weight: bold;
        }
        .brand-text {
          font-size: 20px;
          font-weight: bold;
          color: #1f2937;
        }
        .export-date {
          font-size: 14px;
          color: #6b7280;
        }
        .export-title {
          font-size: 18px;
          font-weight: 600;
          color: #1f2937;
          margin-bottom: 10px;
        }
        table { 
          width: 100%; 
          border-collapse: collapse; 
          font-size: 12px;
        }
        th, td { 
          border: 1px solid #d1d5db; 
          padding: 8px; 
          text-align: center; 
        }
        th { 
          background-color: #f9fafb; 
          font-weight: 600;
        }
        .highlight { 
          background-color: #dcfce7 !important; 
          color: #166534 !important; 
          font-weight: 600;
        }
        @media print {
          body { margin: 0; }
          .no-print { display: none; }
        }
      </style>
    `;

    const tableHtml = exportRef.current.innerHTML;
    const printContent = `
      <!DOCTYPE html>
      <html>
        <head>
          <title>UNGI SmartCards AI - Credit Card Comparison</title>
          ${brandingStyles}
        </head>
        <body>
          <div class="export-header">
            <div class="brand-section">
              <div class="brand-icon">💳</div>
              <div>
                <div class="brand-text">UNGI SmartCards AI</div>
                <div class="export-title">Credit Card Comparison Report</div>
              </div>
            </div>
            <div class="export-date">Generated on: ${currentDate}</div>
          </div>
          ${tableHtml}
          <div style="margin-top: 20px; font-size: 12px; color: #6b7280; text-align: center;">
            © 2024 UNGI SmartCards AI. Every swipe, Optimized.
          </div>
        </body>
      </html>
    `;

    printWindow.document.write(printContent);
    printWindow.document.close();
    
    // Auto-trigger print dialog after content loads
    printWindow.onload = () => {
      printWindow.print();
    };
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="flex items-center justify-center h-64">
          <Loader2 className="w-8 h-8 animate-spin text-primary-600 dark:text-primary-400" />
          <span className="ml-2 text-gray-900 dark:text-white">Loading card comparison data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <p className="text-red-600 dark:text-red-400 mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Credit Card Comparison</h1>
          <p className="text-gray-600 dark:text-gray-300">Compare rewards, fees, and benefits across different credit cards</p>
        </div>

        {/* Controls */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4 mb-6 border border-gray-200 dark:border-gray-700">
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <div className="flex flex-col sm:flex-row gap-4 flex-1">
              {/* Search */}
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search cards or banks..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent w-full bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
                />
              </div>

              {/* Category Filter */}
              <div className="relative">
                <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 dark:text-gray-500 w-4 h-4" />
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="pl-10 pr-8 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
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
                  className="rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500 dark:bg-gray-700"
                />
                <span className="text-sm text-gray-700 dark:text-gray-300">My Cards Only</span>
              </label>
            </div>

            {/* Export Button */}
            <button
              onClick={handleExport}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
            >
              <Download className="w-4 h-4" />
              Export Image
            </button>
          </div>
        </div>

        {filteredCards.length === 0 ? (
          <div className="text-center py-12">
            <Info className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
            <p className="text-gray-600 dark:text-gray-300">No cards found matching your criteria.</p>
          </div>
        ) : (
          /* Comparison Table */
          <div ref={exportRef} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm overflow-x-auto border border-gray-200 dark:border-gray-700">
            {/* Branding Header - Only visible in exports */}
            <div className="hidden print:block p-4 border-b border-gray-200 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                    <CreditCard className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <div className="text-lg font-bold text-gray-900 dark:text-white">UNGI SmartCards AI</div>
                    <div className="text-sm text-gray-600 dark:text-gray-300">Credit Card Comparison Report</div>
                  </div>
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400">
                  Generated on: {new Date().toLocaleDateString()}
                </div>
              </div>
            </div>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
                  <th className="text-left p-3 font-semibold sticky left-0 bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 min-w-[200px] text-gray-900 dark:text-white">
                    Card Details
                  </th>
                  {filteredCards.map((card) => (
                    <th key={card.id} className={`p-3 text-center min-w-[140px] border-r border-gray-200 dark:border-gray-700 ${getCardColor(card.bank_name)}`}>
                      <div className={`font-semibold ${getCardTextColor(card.bank_name)}`}>{card.display_name}</div>
                      <div className={`text-xs mt-1 ${getCardTextColor(card.bank_name)} opacity-75`}>{card.bank_name}</div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {/* Basic Information */}
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <td className="p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">Joining Fee</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-center border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">{card.joining_fee_display}</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <td className="p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">Annual Fee</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-center border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">{card.annual_fee_display}</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <td className="p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">Lounge Visits</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-center border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">{formatLoungeVisits(card)}</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                  <td className="p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">Lounge Spends</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-center border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">{formatLoungeSpends(card)}</td>
                  ))}
                </tr>

                {/* Categories */}
                {allCategories.length > 0 && (
                  <>
                    <tr className="bg-primary-50 dark:bg-primary-900/20">
                      <td className="p-3 font-semibold sticky left-0 bg-primary-50 dark:bg-primary-900/20 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white" colSpan={filteredCards.length + 1}>
                        Spending Categories
                      </td>
                    </tr>
                    {allCategories.map((category) => (
                      <tr key={category} className="border-b border-gray-200 dark:border-gray-700">
                        <td className="p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">
                          {category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </td>
                        {filteredCards.map((card) => {
                          const rowValues = filteredCards.map(c => c.categories[category] || '-');
                          return (
                            <td key={card.id} className={`p-3 text-center border-r border-gray-200 dark:border-gray-700 ${getCellColor(card.categories[category] || '-', rowValues)}`}>
                              {card.categories[category] || '-'}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </>
                )}

                {/* Merchants */}
                {allMerchants.length > 0 && (
                  <>
                    <tr className="bg-green-50 dark:bg-green-900/20">
                      <td className="p-3 font-semibold sticky left-0 bg-green-50 dark:bg-green-900/20 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white" colSpan={filteredCards.length + 1}>
                        Merchant Rewards
                      </td>
                    </tr>
                    {allMerchants.map((merchant) => (
                      <tr key={merchant} className="border-b border-gray-200 dark:border-gray-700">
                        <td className="p-3 font-medium sticky left-0 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">
                          {merchant.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </td>
                        {filteredCards.map((card) => {
                          const rowValues = filteredCards.map(c => c.merchants[merchant] || '-');
                          return (
                            <td key={card.id} className={`p-3 text-center border-r border-gray-200 dark:border-gray-700 ${getCellColor(card.merchants[merchant] || '-', rowValues)}`}>
                              {card.merchants[merchant] || '-'}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </>
                )}

                {/* Additional Info */}
                <tr className="bg-yellow-50 dark:bg-yellow-900/20">
                  <td className="p-3 font-semibold sticky left-0 bg-yellow-50 dark:bg-yellow-900/20 border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white">Additional Info</td>
                  {filteredCards.map((card) => (
                    <td key={card.id} className="p-3 text-xs text-center border-r border-gray-200 dark:border-gray-700 max-w-[140px] text-gray-900 dark:text-white">
                      <div className="break-words">{card.additional_info || '-'}</div>
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
            {/* Branding Footer - Only visible in exports */}
            <div className="hidden print:block p-4 border-t border-gray-200 dark:border-gray-700 text-center">
              <div className="text-sm text-gray-500 dark:text-gray-400">
                © 2024 UNGI SmartCards AI. Every swipe, Optimized.
              </div>
              <div className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                Visit us at UNGI SmartCards AI for personalized credit card recommendations
              </div>
            </div>
          </div>
        )}


      </div>
    </div>
  );
};

export default CardComparisonPage; 