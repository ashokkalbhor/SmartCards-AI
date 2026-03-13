import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { adminAPI } from '../../services/api';
import { useAuth } from '../../hooks/useAuth';
import { ArrowLeft, Users, Activity, Clock, BarChart3 } from 'lucide-react';

interface DAUEntry {
  day: string;
  dau: number;
}

interface TopPageEntry {
  path_root: string;
  views: number;
}

interface AvgDurationEntry {
  path_root: string;
  avg_duration: number;
}

const AdminAnalyticsPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [dau, setDau] = useState<DAUEntry[]>([]);
  const [mau, setMau] = useState<number>(0);
  const [topPages, setTopPages] = useState<TopPageEntry[]>([]);
  const [avgDuration, setAvgDuration] = useState<AvgDurationEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      setError(null);
      try {
        const [dauData, mauData, topPagesData, avgDurationData] = await Promise.all([
          adminAPI.getDAU(),
          adminAPI.getMAU(),
          adminAPI.getTopPages(),
          adminAPI.getAvgDuration(),
        ]);
        setDau(dauData);
        setMau(mauData.mau);
        setTopPages(topPagesData);
        setAvgDuration(avgDurationData);
      } catch (err: any) {
        setError(err?.message || 'Failed to fetch analytics');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (!user || user.email !== 'ashokkalbhor@gmail.com') {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Access Denied</h1>
          <p className="text-gray-600 dark:text-gray-400">You don't have admin privileges.</p>
        </div>
      </div>
    );
  }

  const totalPageViews = topPages.reduce((sum, p) => sum + p.views, 0);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/admin')}
              className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Admin</span>
            </button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Analytics</h1>
              <p className="text-gray-600 dark:text-gray-400 text-sm mt-1">Last 30 days</p>
            </div>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600"></div>
          </div>
        ) : error ? (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-700 dark:text-red-300">
            {error}
          </div>
        ) : (
          <>
            {/* Stat Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="flex items-center">
                  <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                    <Users className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Active Users</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{mau}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="flex items-center">
                  <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                    <Activity className="w-6 h-6 text-green-600 dark:text-green-400" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Page Views</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalPageViews.toLocaleString()}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="flex items-center">
                  <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
                    <BarChart3 className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div className="ml-4">
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Days with Activity</p>
                    <p className="text-2xl font-bold text-gray-900 dark:text-white">{dau.length}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Two column grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              {/* Top Pages */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                    <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
                    Top Pages by Views
                  </h2>
                </div>
                <div className="overflow-x-auto">
                  {topPages.length === 0 ? (
                    <p className="p-6 text-gray-500 dark:text-gray-400 text-sm">No page view data yet.</p>
                  ) : (
                    <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                      <thead className="bg-gray-50 dark:bg-gray-700">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Page</th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Views</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                        {topPages.map((page) => (
                          <tr key={page.path_root} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                            <td className="px-6 py-3 text-sm font-mono text-gray-900 dark:text-gray-100">{page.path_root}</td>
                            <td className="px-6 py-3 text-sm text-right font-medium text-gray-900 dark:text-white">{page.views.toLocaleString()}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              </div>

              {/* Avg Duration */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                    <Clock className="w-5 h-5 mr-2 text-primary-600" />
                    Avg Time on Page
                  </h2>
                </div>
                <div className="overflow-x-auto">
                  {avgDuration.length === 0 ? (
                    <p className="p-6 text-gray-500 dark:text-gray-400 text-sm">No duration data yet.</p>
                  ) : (
                    <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                      <thead className="bg-gray-50 dark:bg-gray-700">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Page</th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Avg Duration</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                        {avgDuration.map((page) => (
                          <tr key={page.path_root} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                            <td className="px-6 py-3 text-sm font-mono text-gray-900 dark:text-gray-100">{page.path_root}</td>
                            <td className="px-6 py-3 text-sm text-right font-medium text-gray-900 dark:text-white">
                              {page.avg_duration != null ? `${Math.round(page.avg_duration)}s` : '-'}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              </div>
            </div>

            {/* DAU Table */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                  <Activity className="w-5 h-5 mr-2 text-primary-600" />
                  Daily Active Users — Last 30 Days
                </h2>
              </div>
              <div className="overflow-x-auto">
                {dau.length === 0 ? (
                  <p className="p-6 text-gray-500 dark:text-gray-400 text-sm">No daily activity data yet.</p>
                ) : (
                  <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead className="bg-gray-50 dark:bg-gray-700">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
                        <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Active Users</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                      {[...dau].reverse().map((entry) => (
                        <tr key={entry.day} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                          <td className="px-6 py-3 text-sm text-gray-900 dark:text-gray-100">{entry.day}</td>
                          <td className="px-6 py-3 text-sm text-right font-medium text-gray-900 dark:text-white">{entry.dau}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AdminAnalyticsPage;
