import React, { useState, useEffect } from 'react';
import { TrendingUp, Users, Download, Search, Star, TrendingDown } from 'lucide-react';
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

interface MerchantPopularityInfoProps {
  merchantName: string;
  className?: string;
}

const MerchantPopularityInfo: React.FC<MerchantPopularityInfoProps> = ({ 
  merchantName, 
  className = "" 
}) => {
  const [popularityData, setPopularityData] = useState<MerchantPopularityData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPopularityData = async () => {
      if (!merchantName) return;
      
      try {
        setLoading(true);
        setError(null);
        
        // Get all merchants and find the one we need
        const response = await cardMasterDataAPI.getMerchantPopularity(50);
        const merchant = response.merchants.find(
          (m: MerchantPopularityData) => m.merchant_name === merchantName.toLowerCase()
        );
        
        if (merchant) {
          setPopularityData(merchant);
        } else {
          setError('Merchant popularity data not available');
        }
      } catch (err) {
        console.error('Error fetching merchant popularity data:', err);
        setError('Failed to load popularity data');
      } finally {
        setLoading(false);
      }
    };

    fetchPopularityData();
  }, [merchantName]);

  if (loading) {
    return (
      <div className={`flex items-center space-x-2 text-sm text-gray-500 ${className}`}>
        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
        <span>Loading popularity data...</span>
      </div>
    );
  }

  if (error || !popularityData) {
    return null; // Don't show anything if there's an error or no data
  }

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

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 ${className}`}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
          Market Popularity
        </h3>
        <div className={`px-2 py-1 rounded-full text-xs font-medium ${getTierColor(popularityData.tier)}`}>
          {getTierLabel(popularityData.tier)}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Popularity Score */}
        <div className="flex items-center space-x-2">
          <Star className="h-4 w-4 text-yellow-500" />
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Popularity Score</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {popularityData.popularity_score}/100
            </p>
          </div>
        </div>

        {/* Market Rank */}
        <div className="flex items-center space-x-2">
          <TrendingUp className="h-4 w-4 text-green-500" />
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Market Rank</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              #{popularityData.rank}
            </p>
          </div>
        </div>

        {/* Market Share */}
        <div className="flex items-center space-x-2">
          <div className="h-4 w-4 bg-blue-500 rounded-full"></div>
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Market Share</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {popularityData.market_share_percent}%
            </p>
          </div>
        </div>

        {/* Growth Rate */}
        <div className="flex items-center space-x-2">
          {popularityData.growth_rate_percent > 0 ? (
            <TrendingUp className="h-4 w-4 text-green-500" />
          ) : (
            <TrendingDown className="h-4 w-4 text-red-500" />
          )}
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Growth Rate</p>
            <p className={`text-lg font-semibold ${
              popularityData.growth_rate_percent > 0 
                ? 'text-green-600 dark:text-green-400' 
                : 'text-red-600 dark:text-red-400'
            }`}>
              {popularityData.growth_rate_percent > 0 ? '+' : ''}{popularityData.growth_rate_percent}%
            </p>
          </div>
        </div>

        {/* Monthly Active Users */}
        <div className="flex items-center space-x-2">
          <Users className="h-4 w-4 text-purple-500" />
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">Monthly Users</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {formatNumber(popularityData.monthly_active_users_millions)}M
            </p>
          </div>
        </div>

        {/* App Downloads */}
        <div className="flex items-center space-x-2">
          <Download className="h-4 w-4 text-indigo-500" />
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">App Downloads</p>
            <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {formatNumber(popularityData.app_downloads_millions)}M
            </p>
          </div>
        </div>
      </div>

      {/* Additional Info */}
      <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-600 dark:text-gray-400">Search Volume</p>
            <p className="font-medium text-gray-900 dark:text-gray-100">
              {popularityData.search_volume_index}/100
            </p>
          </div>
          <div>
            <p className="text-gray-600 dark:text-gray-400">Revenue Impact</p>
            <p className="font-medium text-gray-900 dark:text-gray-100">
              {popularityData.revenue_impact_score}/100
            </p>
          </div>
        </div>
      </div>

      {/* Category */}
      <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Category: <span className="font-medium text-gray-900 dark:text-gray-100 capitalize">
            {popularityData.category.replace('_', ' ')}
          </span>
        </p>
      </div>
    </div>
  );
};

export default MerchantPopularityInfo;
