import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { motion } from 'framer-motion';
import {
  Users,
  Shield,
  FileText,
  CheckCircle,
  XCircle,
  Clock,
  Activity,
  BarChart3,
  Eye,
  Edit,
  ExternalLink,
  MessageSquare,
  RefreshCw,
  Plus
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { adminAPI, cardMasterDataAPI } from '../../services/api';
import { useNavigate } from 'react-router-dom';
import LoadingSpinner from '../../components/UI/LoadingSpinner';

interface AdminStats {
  users: {
    total: number;
    active: number;
    moderators: number;
  };
  moderator_requests: {
    pending: number;
  };
  edit_suggestions: {
    pending: number;
    approved: number;
    rejected: number;
  };
  card_documents: {
    pending: number;
    approved: number;
    rejected: number;
  };
  recent_activity: Array<{
    action: string;
    user: string;
    timestamp: string;
    summary: string;
  }>;
}

interface ChatAccessRequest {
  id: number;
  user_id: number;
  user_name: string;
  user_email: string;
  status: string;
  requested_at: string;
  reviewed_at?: string;
  reviewed_by?: number;
  review_notes?: string;
}

interface ChatAccessStats {
  total_requests: number;
  pending_requests: number;
  approved_requests: number;
  denied_requests: number;
}

interface UserInfo {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  current_role: string | null;
  has_moderator_request: boolean;
  moderator_request_status: string | null;
}

interface ModeratorRequest {
  id: number;
  user_id: number;
  request_reason: string;
  status: string;
  created_at: string;
  user: {
    email: string;
    full_name: string;
  };
}

interface EditSuggestion {
  id: number;
  field_type: string;
  field_name: string;
  old_value: string;
  new_value: string;
  status: string;
  created_at: string;
  user_name: string;
  card_name: string;
  bank_name: string;
  suggestion_reason: string;
}

interface CardDocument {
  id: number;
  title: string;
  description: string;
  document_type: string;
  content: string;
  status: string;
  created_at: string;
  user_name: string;
  card_name: string;
  bank_name: string;
  submission_reason: string;
}

export const SUGGESTIONS_PAGE_SIZE = 25;

const getStatusWeight = (status: string) => {
  switch (status) {
    case 'pending':
      return 0;
    case 'approved':
      return 1;
    case 'rejected':
      return 2;
    default:
      return 3;
  }
};

const AdminDashboardPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<UserInfo[]>([]);
  const [moderatorRequests, setModeratorRequests] = useState<ModeratorRequest[]>([]);
  const [editSuggestions, setEditSuggestions] = useState<EditSuggestion[]>([]);
  const [cardDocuments, setCardDocuments] = useState<CardDocument[]>([]);
  const [chatAccessRequests, setChatAccessRequests] = useState<ChatAccessRequest[]>([]);
  const [chatAccessStats, setChatAccessStats] = useState<ChatAccessStats | null>(null);
  const [chatAccessFilter, setChatAccessFilter] = useState<string>('pending');
  const [suggestionPage, setSuggestionPage] = useState(0);
  const [hasMoreSuggestions, setHasMoreSuggestions] = useState(true);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);
  const [bulkActionLoading, setBulkActionLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'users' | 'moderators' | 'suggestions' | 'documents' | 'chat-approvals'>('overview');
  const [isAddCardModalOpen, setIsAddCardModalOpen] = useState(false);
  const [addCardLoading, setAddCardLoading] = useState(false);
  const [addCardSuccessMessage, setAddCardSuccessMessage] = useState<string | null>(null);
  const [addCardFormData, setAddCardFormData] = useState({
    bank_name: '',
    card_name: '',
    card_variant: '',
    card_network: 'Visa', // Default
    official_url: '',
  });

  const pendingSuggestions = useMemo(
    () => editSuggestions.filter((suggestion) => suggestion.status === 'pending'),
    [editSuggestions]
  );
  const pendingSuggestionIds = useMemo(
    () => pendingSuggestions.map((suggestion) => suggestion.id),
    [pendingSuggestions]
  );
  const hasPendingSuggestions = pendingSuggestionIds.length > 0;
  const suggestionActionDisabled = bulkActionLoading || loadingSuggestions;
  const bulkActionDisabled = suggestionActionDisabled || !hasPendingSuggestions;

  const fetchEditSuggestionsPage = useCallback(
    async (page = 0, reset = false) => {
      setLoadingSuggestions(true);
      try {
        const response = await adminAPI.getEditSuggestions({
          skip: page * SUGGESTIONS_PAGE_SIZE,
          limit: SUGGESTIONS_PAGE_SIZE,
        });

        setHasMoreSuggestions(response.length === SUGGESTIONS_PAGE_SIZE);
        setSuggestionPage(page);
        setEditSuggestions(prev => {
          const merged = reset || page === 0 ? response : [...prev, ...response];
          const sorted = [...merged].sort((a, b) => {
            const statusDiff = getStatusWeight(a.status) - getStatusWeight(b.status);
            if (statusDiff !== 0) {
              return statusDiff;
            }
            return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
          });
          return sorted;
        });
      } catch (error) {
        console.error('Error fetching edit suggestions:', error);
        if (reset) {
          setEditSuggestions([]);
        }
        setHasMoreSuggestions(false);
      } finally {
        setLoadingSuggestions(false);
      }
    },
    []
  );

  const fetchAdminData = useCallback(async (resetSuggestions = true) => {
    try {
      setLoading(true);
      const [statsData, usersData, requestsData, documentsData] = await Promise.all([
        adminAPI.getStats(),
        adminAPI.getUsers(),
        adminAPI.getModeratorRequests(),
        adminAPI.getCardDocuments()
      ]);

      setStats(statsData);
      setUsers(usersData);
      setModeratorRequests(requestsData);
      setCardDocuments(documentsData);
      if (resetSuggestions) {
        await fetchEditSuggestionsPage(0, true);
      }
    } catch (error) {
      console.error('Error fetching admin data:', error);
    } finally {
      setLoading(false);
    }
  }, [fetchEditSuggestionsPage]);

  const processEditSuggestions = useCallback(
    async (
      suggestionIds: number[],
      status: 'approved' | 'rejected',
      options?: { reviewNotes?: string; showBulkLoader?: boolean }
    ) => {
      if (!suggestionIds.length) {
        return;
      }

      const { reviewNotes, showBulkLoader = true } = options ?? {};

      if (showBulkLoader) {
        setBulkActionLoading(true);
      }

      try {
        await Promise.all(
          suggestionIds.map((id) =>
            adminAPI.reviewEditSuggestion(id, {
              status,
              review_notes: reviewNotes,
            })
          )
        );
        await fetchAdminData();
      } catch (error) {
        console.error('Error reviewing edit suggestions:', error);
      } finally {
        if (showBulkLoader) {
          setBulkActionLoading(false);
        }
      }
    },
    [fetchAdminData]
  );
  const fetchChatAccessRequests = useCallback(async () => {
    try {
      const response = await adminAPI.getChatAccessRequests(chatAccessFilter);
      setChatAccessRequests(response);
    } catch (error) {
      console.error('Error fetching chat access requests:', error);
    }
  }, [chatAccessFilter]);

  const fetchChatAccessStats = useCallback(async () => {
    try {
      const response = await adminAPI.getChatAccessStats();
      setChatAccessStats(response);
    } catch (error) {
      console.error('Error fetching chat access stats:', error);
    }
  }, []);

  useEffect(() => {
    fetchAdminData();
  }, [fetchAdminData]);

  useEffect(() => {
    if (activeTab === 'chat-approvals') {
      fetchChatAccessRequests();
      fetchChatAccessStats();
    }
  }, [activeTab, chatAccessFilter, fetchChatAccessRequests, fetchChatAccessStats]);

  const handleChatAccessReview = async (requestId: number, status: 'approved' | 'denied', notes?: string) => {
    try {
      await adminAPI.reviewChatAccessRequest(requestId, status, notes);
      await fetchChatAccessRequests();
      await fetchChatAccessStats();
    } catch (error) {
      console.error('Error reviewing chat access request:', error);
    }
  };

  const handleModeratorRequest = async (requestId: number, status: 'approved' | 'rejected') => {
    try {
      await adminAPI.reviewModeratorRequest(requestId, { status });
      await fetchAdminData(); // Refresh data
    } catch (error) {
      console.error('Error reviewing moderator request:', error);
    }
  };

  const handleEditSuggestion = async (suggestionId: number, status: 'approved' | 'rejected', notes?: string) => {
    await processEditSuggestions(
      [suggestionId],
      status,
      {
        reviewNotes: notes,
        showBulkLoader: false,
      }
    );
  };

  const handleCardDocument = async (documentId: number, status: 'approved' | 'rejected', notes?: string) => {
    try {
      await adminAPI.reviewCardDocument(documentId, { status, review_notes: notes });
      await fetchAdminData(); // Refresh data
    } catch (error) {
      console.error('Error reviewing card document:', error);
    }
  };
  const handleBulkEditSuggestions = async (status: 'approved' | 'rejected') => {
    if (bulkActionDisabled) {
      return;
    }
    await processEditSuggestions(pendingSuggestionIds, status, { showBulkLoader: true });
  };

  const handleAddCard = async (e: React.FormEvent) => {
    e.preventDefault();
    setAddCardLoading(true);
    try {
      // 1. Create Card
      const newCard = await cardMasterDataAPI.createCard({
        bank_name: addCardFormData.bank_name,
        card_name: addCardFormData.card_name,
        card_variant: addCardFormData.card_variant || null,
        card_network: addCardFormData.card_network,
        terms_and_conditions_url: addCardFormData.official_url,
        is_active: true,
      });

      // 2. Trigger Update
      if (newCard && newCard.id) {
        await adminAPI.triggerCardUpdate(newCard.id);
      }

      // Reset and Close
      setIsAddCardModalOpen(false);
      setAddCardFormData({
        bank_name: '',
        card_name: '',
        card_variant: '',
        card_network: 'Visa',
        official_url: '',
      });
      await fetchAdminData();
      setAddCardSuccessMessage(`Card added! Details are being fetched by the AI agent — this may take up to a minute.`);
      setTimeout(() => setAddCardSuccessMessage(null), 8000);
    } catch (error) {
      console.error('Error adding card:', error);
      setAddCardSuccessMessage('❌ Failed to add card. Check console for details.');
      setTimeout(() => setAddCardSuccessMessage(null), 5000);
    } finally {
      setAddCardLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (!user || user.email !== 'ashokkalbhor@gmail.com') {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <Shield className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Access Denied</h1>
          <p className="text-gray-600 dark:text-gray-400">You don't have admin privileges.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Success / Error Toast Banner */}
      {addCardSuccessMessage && (
        <div className={`fixed top-4 right-4 z-50 flex items-start gap-3 px-5 py-4 rounded-xl shadow-lg text-sm font-medium max-w-sm transition-all ${
          addCardSuccessMessage.startsWith('❌')
            ? 'bg-red-50 dark:bg-red-900/40 border border-red-200 dark:border-red-700 text-red-800 dark:text-red-200'
            : 'bg-green-50 dark:bg-green-900/40 border border-green-200 dark:border-green-700 text-green-800 dark:text-green-200'
        }`}>
          <span className="text-base leading-none mt-0.5">{addCardSuccessMessage.startsWith('❌') ? '❌' : '✅'}</span>
          <span>{addCardSuccessMessage.startsWith('❌') ? addCardSuccessMessage.slice(2).trim() : addCardSuccessMessage}</span>
        </div>
      )}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Admin Dashboard
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Manage users, moderators, and content suggestions
            </p>
          </div>

          {/* Quick Action: Card Updates */}
          {/* Quick Action: Card Updates */}
          <div className="flex gap-3">
            <button
              onClick={() => setIsAddCardModalOpen(true)}
              className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors shadow-sm"
            >
              <Plus className="w-5 h-5" />
              <span>Add New Card</span>
            </button>
            <button
              onClick={() => navigate('/admin/card-updates')}
              className="flex items-center space-x-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors shadow-sm"
            >
              <RefreshCw className="w-5 h-5" />
              <span>Card Updates</span>
            </button>
            <button
              onClick={() => navigate('/admin/analytics')}
              className="flex items-center space-x-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors shadow-sm"
            >
              <BarChart3 className="w-5 h-5" />
              <span>Analytics</span>
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700"
              {...({} as any)}
            >
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                  <Users className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Users</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.users.total}</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700"
              {...({} as any)}
            >
              <div className="flex items-center">
                <div className="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                  <Shield className="w-6 h-6 text-green-600 dark:text-green-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Moderators</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.users.moderators}</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700"
              {...({} as any)}
            >
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
                  <Clock className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Pending Requests</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.moderator_requests.pending}</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700"
              {...({} as any)}
            >
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
                  <FileText className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Pending Suggestions</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.edit_suggestions.pending}</p>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-sm border border-gray-200 dark:border-gray-700"
              {...({} as any)}
            >
              <div className="flex items-center">
                <div className="p-2 bg-orange-100 dark:bg-orange-900 rounded-lg">
                  <FileText className="w-6 h-6 text-orange-600 dark:text-orange-400" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Pending Documents</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{stats.card_documents.pending}</p>
                </div>
              </div>
            </motion.div>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="mb-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'users', label: 'Users', icon: Users },
              { id: 'moderators', label: 'Moderator Requests', icon: Shield },
              { id: 'suggestions', label: 'Edit Suggestions', icon: FileText },
              { id: 'documents', label: 'Card Documents', icon: FileText },
              { id: 'chat-approvals', label: 'Chat Approvals', icon: MessageSquare }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${activeTab === tab.id
                    ? 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                    }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          {activeTab === 'overview' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Recent Activity</h2>
              <div className="space-y-4">
                {stats?.recent_activity.map((activity, index) => (
                  <div key={index} className="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                    <Activity className="w-5 h-5 text-gray-400" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">{activity.summary}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">
                        {activity.user} • {new Date(activity.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'users' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">User Management</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead className="bg-gray-50 dark:bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        User
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Role
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    {users.map((user) => (
                      <tr key={user.id}>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div>
                            <div className="text-sm font-medium text-gray-900 dark:text-white">{user.full_name}</div>
                            <div className="text-sm text-gray-500 dark:text-gray-400">{user.email}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${user.current_role === 'moderator'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : user.current_role === 'admin'
                              ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                              : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                            }`}>
                            {user.current_role || 'user'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${user.is_active
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                            }`}>
                            {user.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <div className="flex space-x-2">
                            <button className="text-primary-600 hover:text-primary-900 dark:text-primary-400 dark:hover:text-primary-300">
                              <Eye className="w-4 h-4" />
                            </button>
                            <button className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-300">
                              <Edit className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'moderators' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Moderator Requests</h2>
              <div className="space-y-4">
                {moderatorRequests.map((request) => (
                  <div key={request.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white">{request.user.full_name}</h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">{request.user.email}</p>
                        <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">{request.request_reason}</p>
                        <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                          Requested: {new Date(request.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        {request.status === 'pending' && (
                          <>
                            <button
                              onClick={() => handleModeratorRequest(request.id, 'approved')}
                              className="flex items-center space-x-1 px-3 py-1 bg-green-100 text-green-700 rounded-md hover:bg-green-200 dark:bg-green-900 dark:text-green-200 dark:hover:bg-green-800"
                            >
                              <CheckCircle className="w-4 h-4" />
                              <span>Approve</span>
                            </button>
                            <button
                              onClick={() => handleModeratorRequest(request.id, 'rejected')}
                              className="flex items-center space-x-1 px-3 py-1 bg-red-100 text-red-700 rounded-md hover:bg-red-200 dark:bg-red-900 dark:text-red-200 dark:hover:bg-red-800"
                            >
                              <XCircle className="w-4 h-4" />
                              <span>Reject</span>
                            </button>
                          </>
                        )}
                        {request.status !== 'pending' && (
                          <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${request.status === 'approved'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                            }`}>
                            {request.status}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'suggestions' && (
            <div className="p-6">
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Edit Suggestions</h2>
                <div className="flex flex-wrap items-center gap-3">
                  {typeof stats?.edit_suggestions?.pending === 'number' && (
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      Showing {editSuggestions.length} suggestions • Pending total {stats.edit_suggestions.pending}
                    </span>
                  )}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleBulkEditSuggestions('approved')}
                      disabled={bulkActionDisabled}
                      className={`px-3 py-1 text-sm font-medium rounded-md border transition-colors ${bulkActionDisabled
                        ? 'opacity-60 cursor-not-allowed border-gray-300 dark:border-gray-700 text-gray-400 dark:text-gray-500'
                        : 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200 border-green-200 dark:border-green-800 hover:bg-green-200 dark:hover:bg-green-800'
                        }`}
                    >
                      {bulkActionLoading ? 'Processing…' : 'Approve All Pending'}
                    </button>
                    <button
                      onClick={() => handleBulkEditSuggestions('rejected')}
                      disabled={bulkActionDisabled}
                      className={`px-3 py-1 text-sm font-medium rounded-md border transition-colors ${bulkActionDisabled
                        ? 'opacity-60 cursor-not-allowed border-gray-300 dark:border-gray-700 text-gray-400 dark:text-gray-500'
                        : 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-200 border-red-200 dark:border-red-800 hover:bg-red-200 dark:hover:bg-red-800'
                        }`}
                    >
                      {bulkActionLoading ? 'Processing…' : 'Reject All Pending'}
                    </button>
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                {editSuggestions.length === 0 && !loadingSuggestions && (
                  <div className="text-center py-12 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg text-gray-500 dark:text-gray-400">
                    No suggestions to review right now.
                  </div>
                )}
                {editSuggestions.map((suggestion) => (
                  <div key={suggestion.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                            {suggestion.card_name}
                          </h3>
                          <span className="text-sm text-gray-500 dark:text-gray-400">
                            ({suggestion.bank_name})
                          </span>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                          <div>
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Field</p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                              {suggestion.field_type.replace('_', ' ')}: {suggestion.field_name}
                            </p>
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Change</p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                              {suggestion.old_value} → {suggestion.new_value}
                            </p>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                          <strong>Reason:</strong> {suggestion.suggestion_reason}
                        </p>
                        <div className="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
                          <span>By: {suggestion.user_name}</span>
                          <span>{new Date(suggestion.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <div className="flex space-x-2 ml-4">
                        {suggestion.status === 'pending' && (
                          <>
                            <button
                              onClick={() => handleEditSuggestion(suggestion.id, 'approved')}
                              disabled={suggestionActionDisabled}
                              className={`flex items-center space-x-1 px-3 py-1 rounded-md transition-colors ${suggestionActionDisabled
                                ? 'bg-green-100/60 text-green-400 cursor-not-allowed dark:bg-green-900/60 dark:text-green-600'
                                : 'bg-green-100 text-green-700 hover:bg-green-200 dark:bg-green-900 dark:text-green-200 dark:hover:bg-green-800'
                                }`}
                            >
                              <CheckCircle className="w-4 h-4" />
                              <span>Approve</span>
                            </button>
                            <button
                              onClick={() => handleEditSuggestion(suggestion.id, 'rejected')}
                              disabled={suggestionActionDisabled}
                              className={`flex items-center space-x-1 px-3 py-1 rounded-md transition-colors ${suggestionActionDisabled
                                ? 'bg-red-100/60 text-red-400 cursor-not-allowed dark:bg-red-900/60 dark:text-red-600'
                                : 'bg-red-100 text-red-700 hover:bg-red-200 dark:bg-red-900 dark:text-red-200 dark:hover:bg-red-800'
                                }`}
                            >
                              <XCircle className="w-4 h-4" />
                              <span>Reject</span>
                            </button>
                          </>
                        )}
                        {suggestion.status !== 'pending' && (
                          <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${suggestion.status === 'approved'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                            }`}>
                            {suggestion.status}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {loadingSuggestions && (
                  <div className="flex justify-center py-4">
                    <LoadingSpinner />
                  </div>
                )}
                {hasMoreSuggestions && !loadingSuggestions && (
                  <div className="flex justify-center pt-2">
                    <button
                      onClick={() => fetchEditSuggestionsPage(suggestionPage + 1)}
                      disabled={bulkActionLoading}
                      className={`px-4 py-2 text-sm font-medium border rounded-md transition-colors ${bulkActionLoading
                        ? 'text-primary-300 border-primary-100 cursor-not-allowed dark:text-primary-600 dark:border-primary-800 opacity-60'
                        : 'text-primary-600 hover:text-primary-700 border-primary-200 dark:text-primary-300 dark:hover:text-primary-200 dark:border-primary-700'
                        }`}
                    >
                      Load more suggestions
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'documents' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Card Documents</h2>
              <div className="space-y-4">
                {cardDocuments.map((document) => (
                  <div key={document.id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                            {document.title}
                          </h3>
                          <span className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded">
                            {document.document_type.replace('_', ' ')}
                          </span>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                          <div>
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Card</p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                              {document.card_name} ({document.bank_name})
                            </p>
                          </div>
                          <div>
                            <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Type</p>
                            <p className="text-sm text-gray-600 dark:text-gray-400">
                              {document.document_type.replace('_', ' ')}
                            </p>
                          </div>
                        </div>
                        {document.description && (
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                            <strong>Description:</strong> {document.description}
                          </p>
                        )}
                        <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                          <strong>Reason:</strong> {document.submission_reason}
                        </p>
                        {document.document_type === 'link' && (
                          <a
                            href={document.content}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 dark:text-blue-400 hover:underline text-sm flex items-center"
                          >
                            <ExternalLink className="w-3 h-3 mr-1" />
                            View Document
                          </a>
                        )}
                        {(document.document_type === 'policy_update' || document.document_type === 'terms_change') && (
                          <div className="bg-gray-50 dark:bg-gray-700 rounded p-3 mt-2">
                            <p className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{document.content}</p>
                          </div>
                        )}
                        <div className="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400 mt-2">
                          <span>By: {document.user_name}</span>
                          <span>{new Date(document.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <div className="flex space-x-2 ml-4">
                        {document.status === 'pending' && (
                          <>
                            <button
                              onClick={() => handleCardDocument(document.id, 'approved')}
                              className="flex items-center space-x-1 px-3 py-1 bg-green-100 text-green-700 rounded-md hover:bg-green-200 dark:bg-green-900 dark:text-green-200 dark:hover:bg-green-800"
                            >
                              <CheckCircle className="w-4 h-4" />
                              <span>Approve</span>
                            </button>
                            <button
                              onClick={() => handleCardDocument(document.id, 'rejected')}
                              className="flex items-center space-x-1 px-3 py-1 bg-red-100 text-red-700 rounded-md hover:bg-red-200 dark:bg-red-900 dark:text-red-200 dark:hover:bg-red-800"
                            >
                              <XCircle className="w-4 h-4" />
                              <span>Reject</span>
                            </button>
                          </>
                        )}
                        {document.status !== 'pending' && (
                          <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${document.status === 'approved'
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                            }`}>
                            {document.status}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                {cardDocuments.length === 0 && (
                  <div className="text-center py-8">
                    <FileText className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">No card documents found.</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Chat Approvals Tab */}
          {activeTab === 'chat-approvals' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">Chat Access Requests</h2>

              {/* Stats Cards */}
              {chatAccessStats && (
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Requests</p>
                        <p className="text-2xl font-bold text-gray-900 dark:text-white">{chatAccessStats.total_requests}</p>
                      </div>
                      <FileText className="h-8 w-8 text-blue-600" />
                    </div>
                  </div>
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Pending</p>
                        <p className="text-2xl font-bold text-yellow-600">{chatAccessStats.pending_requests}</p>
                      </div>
                      <Clock className="h-8 w-8 text-yellow-600" />
                    </div>
                  </div>
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Approved</p>
                        <p className="text-2xl font-bold text-green-600">{chatAccessStats.approved_requests}</p>
                      </div>
                      <CheckCircle className="h-8 w-8 text-green-600" />
                    </div>
                  </div>
                  <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Denied</p>
                        <p className="text-2xl font-bold text-red-600">{chatAccessStats.denied_requests}</p>
                      </div>
                      <XCircle className="h-8 w-8 text-red-600" />
                    </div>
                  </div>
                </div>
              )}

              {/* Filter Tabs */}
              <div className="flex space-x-1 bg-gray-100 dark:bg-gray-700 p-1 rounded-lg mb-6">
                {['pending', 'approved', 'denied'].map((status) => (
                  <button
                    key={status}
                    onClick={() => setChatAccessFilter(status)}
                    className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${chatAccessFilter === status
                      ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow-sm'
                      : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                      }`}
                  >
                    {status.charAt(0).toUpperCase() + status.slice(1)}
                  </button>
                ))}
              </div>

              {/* Requests List */}
              <div className="space-y-4">
                {chatAccessRequests.map((request) => (
                  <div key={request.id} className="border border-gray-200 dark:border-gray-600 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <div>
                            <h4 className="font-medium text-gray-900 dark:text-white">{request.user_name}</h4>
                            <p className="text-sm text-gray-600 dark:text-gray-400">{request.user_email}</p>
                          </div>
                          <span className={`px-2 py-1 text-xs font-medium rounded-full ${request.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                            request.status === 'approved' ? 'bg-green-100 text-green-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                            {request.status}
                          </span>
                        </div>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                          Requested: {new Date(request.requested_at).toLocaleString()}
                        </p>
                      </div>
                      {request.status === 'pending' && (
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleChatAccessReview(request.id, 'approved')}
                            className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-sm font-medium"
                          >
                            Approve
                          </button>
                          <button
                            onClick={() => handleChatAccessReview(request.id, 'denied')}
                            className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-sm font-medium"
                          >
                            Deny
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {chatAccessRequests.length === 0 && (
                  <div className="text-center py-8">
                    <MessageSquare className="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
                    <p className="text-gray-500 dark:text-gray-400">No chat access requests found.</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
      {/* Add Card Modal */}
      {isAddCardModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md overflow-hidden"
            {...({} as any)}
          >
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">Add New Card</h3>
                <button
                  onClick={() => setIsAddCardModalOpen(false)}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              <form onSubmit={handleAddCard} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Bank Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={addCardFormData.bank_name}
                    onChange={(e) => setAddCardFormData({ ...addCardFormData, bank_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="e.g. HDFC Bank"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Card Name *
                  </label>
                  <input
                    type="text"
                    required
                    value={addCardFormData.card_name}
                    onChange={(e) => setAddCardFormData({ ...addCardFormData, card_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="e.g. Millennia"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Card Network *
                  </label>
                  <select
                    value={addCardFormData.card_network}
                    onChange={(e) => setAddCardFormData({ ...addCardFormData, card_network: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  >
                    <option value="Visa">Visa</option>
                    <option value="Mastercard">Mastercard</option>
                    <option value="RuPay">RuPay</option>
                    <option value="Amex">Amex</option>
                    <option value="Diners Club">Diners Club</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Card Variant
                  </label>
                  <input
                    type="text"
                    value={addCardFormData.card_variant}
                    onChange={(e) => setAddCardFormData({ ...addCardFormData, card_variant: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="e.g. Visa Signature (Optional)"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Official URL (For Auto-Extraction)
                  </label>
                  <input
                    type="url"
                    value={addCardFormData.official_url}
                    onChange={(e) => setAddCardFormData({ ...addCardFormData, official_url: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="https://..."
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Providing this URL allows the AI agent to automatically fetch fees, rewards, and benefits.
                  </p>
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <button
                    type="button"
                    onClick={() => setIsAddCardModalOpen(false)}
                    className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600 rounded-md"
                    disabled={addCardLoading}
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={addCardLoading}
                    className="flex items-center px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-md disabled:opacity-50"
                  >
                    {addCardLoading ? (
                      <>
                        <LoadingSpinner size="sm" color="white" className="mr-2" />
                        Creating...
                      </>
                    ) : (
                      'Add Card'
                    )}
                  </button>
                </div>
              </form>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboardPage; 
