import React, { useState, useEffect } from 'react';
import { TrendingUp, Users, Download, Search, Star, TrendingDown, Filter, BarChart3 } from 'lucide-react';
import { cardMasterDataAPI } from '../../services/api';

interface MerchantPopularityData {
  rank: number;
  merchant_name: string;
  display_name: string;
  category: string;
  tier: string;
  popularity_score: number;
  market_share_percent: number;
  monthly_active_users_millions: number;
  growth_rate_percent: number;
  search_volume_index: number;
  social_media_followers_millions: number;
  app_downloads_millions: number;
  revenue_impact_score: number;
}

interface CategoryData {
  [key: string]: {
    top_merchants: string[];
    merchant_count: number;
  };
}

interface TierData {
  [key: string]: {
    merchants: string[];
    merchant_count: number;
    description: string;
  };
}

const MerchantPopularityPage: React.FC = () => {
  const [merchants, setMerchants] = useState<MerchantPopularityData[]>([]);
  const [categories, setCategories] = useState<CategoryData>({});
  const [tiers, setTiers] = useState<TierData>({});
  const [growthMerchants, setGrowthMerchants] = useState<MerchantPopularityData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedTier, setSelectedTier] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'popularity' | 'growth' | 'market_share'>('popularity');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch all data in parallel
        const [merchantsRes, categoriesRes, tiersRes, growthRes] = await Promise.all([
          cardMasterDataAPI.getMerchantPopularity(50),
          cardMasterDataAPI.getMerchantCategories(),
          cardMasterDataAPI.getMerchantTiers(),
          cardMasterDataAPI.getGrowthMerchants(25)
        ]);

        setMerchants(merchantsRes.merchants);
        setCategories(categoriesRes.categories);
        setTiers(tiersRes.tiers);
        setGrowthMerchants(growthRes.growth_merchants);
      } catch (err) {
        console.error('Error fetching merchant data:', err);
        setError('Failed to load merchant popularity data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getFilteredMerchants = () => {
    let filtered = [...merchants];

    if (selectedCategory !== 'all') {
      filtered = filtered.filter(m => m.category === selectedCategory);
    }

    if (selectedTier !== 'all') {
      filtered = filtered.filter(m => m.tier === selectedTier);
    }

    // Sort by selected criteria
    switch (sortBy) {
      case 'popularity':
        filtered.sort((a, b) => b.popularity_score - a.popularity_score);
        break;
      case 'growth':
        filtered.sort((a, b) => b.growth_rate_percent - a.growth_rate_percent);
        break;
      case 'market_share':
        filtered.sort((a, b) => b.market_share_percent - a.market_share_percent);
        break;
    }

    return filtered;
  };

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'tier_1_super_popular':
        return 'text-purple-600 bg-purple-100 dark:text-purple-400 dark:bg-purple-900/20';
      case 'tier_2_very_popular':
        return 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900/20';
      case 'tier_3_popular':
        return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/20';
      case 'tier_4_moderate':
        return 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/20';
      case 'tier_5_emerging':
        return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
      default:
        return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
    }
  };

  const getTierLabel = (tier: string) => {
    switch (tier) {
      case 'tier_1_super_popular':
        return 'Super Popular';
      case 'tier_2_very_popular':
        return 'Very Popular';
      case 'tier_3_popular':
        return 'Popular';
      case 'tier_4_moderate':
        return 'Moderate';
      case 'tier_5_emerging':
        return 'Emerging';
      default:
        return 'Unknown';
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p className="text-red-800 dark:text-red-200">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  const filteredMerchants = getFilteredMerchants();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            Merchant Popularity Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Market research-based merchant popularity and demand analysis
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 dark:bg-blue-900/20 rounded-lg">
                <BarChart3 className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Merchants</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{merchants.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 dark:bg-green-900/20 rounded-lg">
                <TrendingUp className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600 dark:text-gray-400">High Growth</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{growthMerchants.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 dark:bg-purple-900/20 rounded-lg">
                <Star className="h-6 w-6 text-purple-600 dark:text-purple-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600 dark:text-gray-400">Categories</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{Object.keys(categories).length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg">
                <Users className="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600 dark:text-gray-400">Tiers</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{Object.keys(tiers).length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 mb-8">
          <div className="flex items-center space-x-4">
            <Filter className="h-5 w-5 text-gray-500" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Filters</h3>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            {/* Category Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Category
              </label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              >
                <option value="all">All Categories</option>
                {Object.keys(categories).map(category => (
                  <option key={category} value={category}>
                    {category.replace('_', ' ').toUpperCase()} ({categories[category].merchant_count})
                  </option>
                ))}
              </select>
            </div>

            {/* Tier Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Popularity Tier
              </label>
              <select
                value={selectedTier}
                onChange={(e) => setSelectedTier(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              >
                <option value="all">All Tiers</option>
                {Object.entries(tiers).map(([tier, data]) => (
                  <option key={tier} value={tier}>
                    {getTierLabel(tier)} ({data.merchant_count})
                  </option>
                ))}
              </select>
            </div>

            {/* Sort By */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Sort By
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
              >
                <option value="popularity">Popularity Score</option>
                <option value="growth">Growth Rate</option>
                <option value="market_share">Market Share</option>
              </select>
            </div>
          </div>
        </div>

        {/* Merchants Table */}
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              Merchant Rankings ({filteredMerchants.length} merchants)
            </h3>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Rank
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Merchant
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Tier
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Popularity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Market Share
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Growth
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Users (M)
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Downloads (M)
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {filteredMerchants.map((merchant) => (
                  <tr key={merchant.merchant_name} className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100">
                      #{merchant.rank}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {merchant.display_name}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400 capitalize">
                          {merchant.category.replace('_', ' ')}
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getTierColor(merchant.tier)}`}>
                        {getTierLabel(merchant.tier)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                      {merchant.popularity_score}/100
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                      {merchant.market_share_percent}%
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        {merchant.growth_rate_percent > 0 ? (
                          <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                        ) : (
                          <TrendingDown className="h-4 w-4 text-red-500 mr-1" />
                        )}
                        <span className={`text-sm font-medium ${
                          merchant.growth_rate_percent > 0 
                            ? 'text-green-600 dark:text-green-400' 
                            : 'text-red-600 dark:text-red-400'
                        }`}>
                          {merchant.growth_rate_percent > 0 ? '+' : ''}{merchant.growth_rate_percent}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                      {formatNumber(merchant.monthly_active_users_millions)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                      {formatNumber(merchant.app_downloads_millions)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Growth Merchants Section */}
        {growthMerchants.length > 0 && (
          <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                High Growth Merchants (25%+ growth)
              </h3>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
              {growthMerchants.map((merchant) => (
                <div key={merchant.merchant_name} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-900 dark:text-gray-100">
                      {merchant.display_name}
                    </h4>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getTierColor(merchant.tier)}`}>
                      {getTierLabel(merchant.tier)}
                    </span>
                  </div>
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-2">
                    <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                    <span className="text-green-600 dark:text-green-400 font-medium">
                      +{merchant.growth_rate_percent}% growth
                    </span>
                  </div>
                  <div className="text-sm text-gray-500 dark:text-gray-400 capitalize">
                    {merchant.category.replace('_', ' ')} • {merchant.market_share_percent}% market share
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MerchantPopularityPage;
