import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CreditCard, PlusCircle, BarChart3, LayoutGrid, Users, ThumbsUp, MessageSquare } from 'lucide-react';
import EnhancedChatBot from '../../components/UI/EnhancedChatBot';
import { creditCardsAPI, communityAPI, cardMasterDataAPI } from '../../services/api';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [totalUserCards, setTotalUserCards] = useState(0);
  const [totalAvailableCards, setTotalAvailableCards] = useState(0);
  const [isChatExpanded, setIsChatExpanded] = useState(false);

  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        const data = await creditCardsAPI.getDashboardStats();
        setTotalUserCards(data.totalCards ?? 0);
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      }
    };

    const fetchTotalAvailableCards = async () => {
      try {
        const data = await cardMasterDataAPI.getCards();
        setTotalAvailableCards(data.length);
      } catch (error) {
        console.error('Error fetching available cards count:', error);
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
    fetchTotalAvailableCards();
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
    <div className="h-full flex flex-col p-4 gap-4 lg:overflow-hidden">
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

      {/* Quick Action Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-2 lg:grid-cols-4 gap-3 flex-shrink-0"
        {...({} as any)}
      >
        {/* Add Card */}
        <div
          onClick={() => navigate('/cards/add?mode=quick')}
          className="group relative bg-gradient-to-br from-blue-600 to-blue-800 rounded-xl px-4 py-3 cursor-pointer overflow-hidden shadow-md hover:shadow-blue-500/30 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 border border-blue-500/30"
        >
          <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-xl" />
          <div className="flex items-center space-x-3">
            <div className="p-1.5 bg-white/15 rounded-lg flex-shrink-0">
              <PlusCircle className="h-5 w-5 text-white" />
            </div>
            <div>
              <p className="text-sm font-semibold text-white">Add Card</p>
              <p className="text-xs text-blue-200">Add a new card</p>
            </div>
          </div>
        </div>

        {/* My Cards */}
        <div
          onClick={() => navigate('/cards')}
          className="group relative bg-gradient-to-br from-violet-600 to-violet-800 rounded-xl px-4 py-3 cursor-pointer overflow-hidden shadow-md hover:shadow-violet-500/30 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 border border-violet-500/30"
        >
          <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-xl" />
          <div className="flex items-center space-x-3">
            <div className="p-1.5 bg-white/15 rounded-lg flex-shrink-0">
              <CreditCard className="h-5 w-5 text-white" />
            </div>
            <div>
              <p className="text-sm font-semibold text-white">My Cards</p>
              <p className="text-xs text-violet-200">
                {totalUserCards > 0 ? `${totalUserCards} Card${totalUserCards !== 1 ? 's' : ''}` : 'View your cards'}
              </p>
            </div>
          </div>
        </div>

        {/* Compare Cards */}
        <div
          onClick={() => navigate('/cards/compare')}
          className="group relative bg-gradient-to-br from-teal-600 to-teal-800 rounded-xl px-4 py-3 cursor-pointer overflow-hidden shadow-md hover:shadow-teal-500/30 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 border border-teal-500/30"
        >
          <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-xl" />
          <div className="flex items-center space-x-3">
            <div className="p-1.5 bg-white/15 rounded-lg flex-shrink-0">
              <BarChart3 className="h-5 w-5 text-white" />
            </div>
            <div>
              <p className="text-sm font-semibold text-white">Compare Cards</p>
              <p className="text-xs text-teal-200">Compare benefits</p>
            </div>
          </div>
        </div>

        {/* View All Cards */}
        <div
          onClick={() => navigate('/all-cards')}
          className="group relative bg-gradient-to-br from-amber-500 to-amber-700 rounded-xl px-4 py-3 cursor-pointer overflow-hidden shadow-md hover:shadow-amber-500/30 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-200 border border-amber-400/30"
        >
          <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-xl" />
          <div className="flex items-center space-x-3">
            <div className="p-1.5 bg-white/15 rounded-lg flex-shrink-0">
              <LayoutGrid className="h-5 w-5 text-white" />
            </div>
            <div>
              <p className="text-sm font-semibold text-white">View All Cards</p>
              <p className="text-xs text-amber-200">
                {totalAvailableCards > 0 ? `${totalAvailableCards} Cards available` : 'Browse all cards'}
              </p>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Content Grid - Natural content flow */}
      <motion.div
        className={`grid gap-4 flex-1 min-h-0 overflow-hidden ${isChatExpanded ? 'grid-cols-1 grid-rows-1' : 'grid-cols-1 lg:grid-cols-3 lg:grid-rows-1'}`}
        layout
        transition={{ duration: 0.3, ease: "easeInOut" }}
        {...({} as any)}
      >
        {/* ChatBot */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className={isChatExpanded ? 'col-span-1 h-full' : 'lg:col-span-2 h-full'}
          {...({} as any)}
        >
          <div className="relative h-full min-h-0">
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
          <div className="h-full flex flex-col gap-4 min-h-0">
          {/* Top Performing Cards - More compact */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex-none bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700"
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
            className="flex-1 min-h-0 flex flex-col bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700"
            {...({} as any)}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Top Discussions</h2>
            </div>
            <div className="space-y-3 flex-1 overflow-y-auto min-h-0">
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