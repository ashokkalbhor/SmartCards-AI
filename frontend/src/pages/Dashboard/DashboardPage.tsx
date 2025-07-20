import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { CreditCard, Banknote, Gift, Activity, ArrowUpRight, ArrowDownRight, Building2 } from 'lucide-react';
import { formatRupees } from '../../utils/currency';
import ChatBot from '../../components/UI/ChatBot';

const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  
  // Mock data - replace with actual API calls
  const stats = {
    totalCards: 4,
    totalBankAccounts: 3,
    totalSpent: 284750.00,
    totalRewards: 8542.50,
    monthlySavings: 12.5,
  };

  const recentTransactions = [
    { id: 1, merchant: 'Amazon', amount: 7500.00, date: '2024-01-15', category: 'Shopping' },
    { id: 2, merchant: 'Starbucks', amount: 395.00, date: '2024-01-15', category: 'Food' },
    { id: 3, merchant: 'Shell', amount: 3780.00, date: '2024-01-14', category: 'Gas' },
    { id: 4, merchant: 'Netflix', amount: 1330.00, date: '2024-01-14', category: 'Entertainment' },
  ];

  const topCards = [
    { id: 1, name: 'HDFC Regalia Gold', rewards: 15680.00, percentage: 5.5 },
    { id: 2, name: 'SBI Elite', rewards: 8945.00, percentage: 3.2 },
    { id: 3, name: 'ICICI Amazon Pay', rewards: 3850.00, percentage: 1.8 },
  ];

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
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3 flex-shrink-0"
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

        {/* Total Bank Accounts */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700">
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
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700">
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

        {/* Total Rewards */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs font-medium text-gray-600 dark:text-gray-400">Total Rewards</p>
              <p className="text-xl font-bold text-gray-900 dark:text-white">{formatRupees(stats.totalRewards)}</p>
            </div>
            <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
              <Gift className="h-5 w-5 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
        </div>

        {/* Monthly Savings */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700">
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
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* ChatBot */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-2"
          {...({} as any)}
        >
          <ChatBot />
        </motion.div>

        {/* Right Column */}
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
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Top Cards</h2>
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
                      <p className="text-xs text-gray-500 dark:text-gray-400">{formatRupees(card.rewards)} rewards</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1">
                    <ArrowUpRight className="h-3 w-3 text-green-500" />
                    <span className="text-xs font-medium text-green-600 dark:text-green-400">
                      {card.percentage}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Recent Transactions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm border border-gray-200 dark:border-gray-700"
            {...({} as any)}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Recent Transactions</h2>
              <button className="text-primary-600 hover:text-primary-500 dark:text-primary-400 dark:hover:text-primary-300 text-sm font-medium">
                View all
              </button>
            </div>
            <div className="space-y-3 max-h-80 overflow-y-auto">
              {recentTransactions.map((transaction) => (
                <div key={transaction.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900 rounded-lg flex items-center justify-center">
                      <Activity className="h-4 w-4 text-primary-600 dark:text-primary-400" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white text-sm">{transaction.merchant}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{transaction.category}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900 dark:text-white text-sm">{formatRupees(transaction.amount)}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{transaction.date}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage; 