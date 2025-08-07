import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CreditCard, Banknote, ArrowUpRight, Building2, Users, ThumbsUp, MessageSquare } from 'lucide-react';
import { formatRupees } from '../../utils/currency';
import EnhancedChatBot from '../../components/UI/EnhancedChatBot';
import { creditCardsAPI, communityAPI } from '../../services/api';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalCards: 0,
    totalBankAccounts: 0,
    totalSpent: 0,
    monthlySavings: 0,
  });
  const [isChatExpanded, setIsChatExpanded] = useState(false);

  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        const data = await creditCardsAPI.getDashboardStats();
        setStats(data);
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      }
    };

    const fetchPopularCards = async () => {
      try {
        const data = await creditCardsAPI.getPopularCards(5);
        setTopCards(data);
      } catch (error) {
        console.error('Error fetching popular cards:', error);
      }
    };

    const fetchTopDiscussions = async () => {
      try {
        const data = await communityAPI.getTopDiscussions(5);
        setTopDiscussions(data.discussions || []);
      } catch (error) {
        console.error('Error fetching top discussions:', error);
      }
    };

    fetchDashboardStats();
    fetchPopularCards();
    fetchTopDiscussions();
  }, []);



  const [topCards, setTopCards] = useState<Array<{
    id: number;
    name: string;
    holders: number;
    percentage: number;
  }>>([]);

  const [topDiscussions, setTopDiscussions] = useState<Array<{
    id: number;
    title: string;
    body?: string;
    user_name: string;
    card_name: string;
    upvotes: number;
    downvotes: number;
    comment_count: number;
    engagement_score: number;
    time_ago: string;
  }>>([]);

  return (
    <div className="min-h-screen flex flex-col p-4 space-y-4">
      {/* Compact Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between flex-shrink-0"
        {...({} as any)}
      >
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400">Welcome back! Here's your UNGI SmartCards AI overview.</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-gray-500 dark:text-gray-400">Last updated</p>
          <p className="text-sm font-medium text-gray-900 dark:text-white">Just now</p>
        </div>
      </motion.div>

      {/* Compact Stats Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-3 flex-shrink-0"
        {...({} as any)}
      >
        {/* Total Cards - Made clickable */}
        <div 
          onClick={() => navigate('/cards')}
          className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700 cursor-pointer hover:shadow-md hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-200 group"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Total Cards</p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">{stats.totalCards}</p>
            </div>
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg group-hover:bg-blue-200 dark:group-hover:bg-blue-800 transition-colors">
              <CreditCard className="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
        </div>

        {/* Community - New card for viewing all cards */}
        <div 
          onClick={() => navigate('/all-cards')}
          className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700 cursor-pointer hover:shadow-md hover:border-teal-300 dark:hover:border-teal-600 transition-all duration-200 group"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Community</p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">View All</p>
            </div>
            <div className="p-2 bg-teal-100 dark:bg-teal-900 rounded-lg group-hover:bg-teal-200 dark:group-hover:bg-teal-800 transition-colors">
              <Users className="h-5 w-5 text-teal-600 dark:text-teal-400" />
            </div>
          </div>
        </div>

        {/* Total Bank Accounts */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700 relative">
          {/* Coming Soon Banner */}
          <div className="absolute -top-2 -right-2 bg-yellow-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-md z-10">
            COMING SOON
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Total Bank Accounts</p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">{stats.totalBankAccounts}</p>
            </div>
            <div className="p-2 bg-indigo-100 dark:bg-indigo-900 rounded-lg">
              <Building2 className="h-5 w-5 text-indigo-600 dark:text-indigo-400" />
            </div>
          </div>
        </div>

        {/* Total Spent */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700 relative">
          {/* Coming Soon Banner */}
          <div className="absolute -top-2 -right-2 bg-yellow-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-md z-10">
            COMING SOON
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Total Spent</p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">{formatRupees(stats.totalSpent)}</p>
            </div>
            <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
              <Banknote className="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
          </div>
        </div>

        {/* Monthly Savings */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700 relative">
          {/* Coming Soon Banner */}
          <div className="absolute -top-2 -right-2 bg-yellow-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-md z-10">
            COMING SOON
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Monthly Savings</p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">{stats.monthlySavings}%</p>
            </div>
            <div className="p-2 bg-orange-100 dark:bg-orange-900 rounded-lg">
              <ArrowUpRight className="h-5 w-5 text-orange-600 dark:text-orange-400" />
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Content Grid - Natural content flow */}
      <motion.div 
        className={`grid gap-4 ${isChatExpanded ? 'grid-cols-1' : 'grid-cols-1 lg:grid-cols-3'}`}
        layout
        transition={{ duration: 0.3, ease: "easeInOut" }}
        {...({} as any)}
      >
        {/* ChatBot */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className={isChatExpanded ? 'col-span-1' : 'lg:col-span-2'}
          {...({} as any)}
        >
          <div className="relative">
            {/* Coming Soon Banner */}
            <div className="absolute -top-2 -right-2 bg-yellow-500 text-white text-xs font-bold px-2 py-1 rounded-full shadow-md z-20">
              COMING SOON
            </div>
            {/* Expand/Collapse Button */}
            <button
              onClick={() => setIsChatExpanded(!isChatExpanded)}
              className="absolute top-2 right-2 z-10 p-2 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-all duration-200"
              title={isChatExpanded ? "Collapse chat" : "Expand chat"}
            >
              {isChatExpanded ? (
                <svg className="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                </svg>
              )}
            </button>
            <EnhancedChatBot />
            {isChatExpanded && (
              <div className="absolute top-2 left-2 z-10 px-3 py-1 bg-primary-600 text-white text-xs font-medium rounded-full">
                Full Screen Chat
              </div>
            )}
          </div>
        </motion.div>

        {/* Right Column - Hidden when chat is expanded */}
        {!isChatExpanded && (
          <div className="space-y-4">
          {/* Top Performing Cards - More compact */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700"
            {...({} as any)}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Most Popular Cards</h2>
              <button className="text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium">
                View all
              </button>
            </div>
            <div className="space-y-3">
              {topCards.map((card, index) => (
                <div key={card.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-6 h-6 bg-gradient-to-r from-primary-500 to-primary-600 rounded-md flex items-center justify-center text-white text-xs font-bold">
                      {index + 1}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white text-sm">{card.name}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{card.holders.toLocaleString()} holders</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Users className="h-3 w-3 text-blue-500" />
                    <span className="text-xs font-medium text-blue-600 dark:text-blue-400">
                      {card.percentage}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Top Discussions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700"
            {...({} as any)}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Top Discussions</h2>
              <button 
                onClick={() => navigate('/all-cards')}
                className="text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium"
              >
                View all
              </button>
            </div>
            <div className="space-y-3 max-h-80 overflow-y-auto">
              {topDiscussions.length > 0 ? (
                topDiscussions.map((discussion, index) => (
                  <div 
                    key={discussion.id} 
                    onClick={() => navigate(`/community/post/${discussion.id}`)}
                    className="flex items-start justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                  >
                    <div className="flex items-start space-x-3 flex-1">
                      <div className="w-6 h-6 bg-gradient-to-r from-primary-500 to-primary-600 rounded-md flex items-center justify-center text-white text-xs font-bold mt-1">
                        {index + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-gray-900 dark:text-white text-sm line-clamp-2 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                          {discussion.title}
                        </p>
                        <div className="flex items-center space-x-4 mt-1">
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            {discussion.user_name}
                          </span>
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            {discussion.time_ago}
                          </span>
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            {discussion.card_name}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2 ml-3">
                      <div className="flex items-center space-x-1">
                        <ThumbsUp className="h-3 w-3 text-green-500" />
                        <span className="text-xs font-medium text-green-600 dark:text-green-400">
                          {discussion.upvotes}
                        </span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <MessageSquare className="h-3 w-3 text-blue-500" />
                        <span className="text-xs font-medium text-blue-600 dark:text-blue-400">
                          {discussion.comment_count}
                        </span>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8">
                  <MessageSquare className="w-8 h-8 text-gray-400 dark:text-gray-500 mx-auto mb-2" />
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    No discussions yet
                  </p>
                  <p className="text-xs text-gray-400 dark:text-gray-500">
                    Be the first to start a discussion!
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        </div>
        )}
      </motion.div>
    </div>
  );
};

export default DashboardPage; 