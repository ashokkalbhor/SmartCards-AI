import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://smartcards-ai-2.onrender.com/api/v1'  // Render backend URL
    : 'http://localhost:8001/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
                  const response = await axios.post(
          process.env.NODE_ENV === 'production' 
            ? 'https://smartcards-ai-2.onrender.com/api/v1/auth/refresh'
            : 'http://localhost:8001/api/v1/auth/refresh',
          {
            refresh_token: refreshToken,
          }
        );

          const { access_token, refresh_token } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh token failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (userData: {
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
  }) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  login: async (credentials: { email: string; password: string }) => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },
};

// Users API
export const usersAPI = {
  getProfile: async () => {
    const response = await api.get('/users/me');
    return response.data;
  },

  updateProfile: async (userData: any) => {
    const response = await api.put('/users/me', userData);
    return response.data;
  },
};

// Credit Cards API
export const creditCardsAPI = {
  getCards: async () => {
    const response = await api.get('/credit-cards?limit=1000');
    return response.data;
  },

  addCard: async (cardData: any) => {
    const response = await api.post('/credit-cards', cardData);
    return response.data;
  },

  getCard: async (id: string) => {
    const response = await api.get(`/credit-cards/${id}`);
    return response.data;
  },

  updateCard: async (id: string, cardData: any) => {
    const response = await api.put(`/credit-cards/${id}`, cardData);
    return response.data;
  },

  deleteCard: async (id: string) => {
    const response = await api.delete(`/credit-cards/${id}`);
    return response.data;
  },

  getDashboardStats: async () => {
    const response = await api.get('/credit-cards/dashboard/stats');
    return response.data;
  },

  getPopularCards: async (limit: number = 5) => {
    const response = await api.get(`/credit-cards/popular-cards?limit=${limit}`);
    return response.data;
  },
};

// Transactions API
export const transactionsAPI = {
  getTransactions: async () => {
    const response = await api.get('/transactions');
    return response.data;
  },

  addTransaction: async (transactionData: any) => {
    const response = await api.post('/transactions', transactionData);
    return response.data;
  },
};

// Rewards API
export const rewardsAPI = {
  getRewards: async () => {
    const response = await api.get('/rewards');
    return response.data;
  },
};

// Recommendations API
export const recommendationsAPI = {
  getRecommendations: async () => {
    const response = await api.get('/recommendations');
    return response.data;
  },
};

// Card Master Data API
export const cardMasterDataAPI = {
  getComparison: async (userCardsOnly?: boolean, cardIds?: number[]) => {
    const params = new URLSearchParams();
    if (userCardsOnly) params.append('user_cards_only', 'true');
    if (cardIds && cardIds.length > 0) {
      cardIds.forEach(id => params.append('card_ids', id.toString()));
    }
    
    const response = await api.get(`/card-master-data/comparison?${params.toString()}`);
    return response.data;
  },

  getCards: async (bankName?: string, cardTier?: string, isActive?: boolean) => {
    const params = new URLSearchParams();
    if (bankName) params.append('bank_name', bankName);
    if (cardTier) params.append('card_tier', cardTier);
    if (isActive !== undefined) params.append('is_active', isActive.toString());
    // Request a higher limit to get more cards
    params.append('limit', '1000');
    
    const response = await api.get(`/card-master-data/cards?${params.toString()}`);
    return response.data;
  },

  getCardById: async (cardId: string) => {
    const response = await api.get(`/card-master-data/cards/${cardId}`);
    return response.data;
  },

  getBanks: async () => {
    const response = await api.get('/card-master-data/banks');
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get('/card-master-data/categories');
    return response.data;
  },

  getMerchants: async () => {
    const response = await api.get('/card-master-data/merchants');
    return response.data;
  },

  // New merchant popularity API
  getMerchantPopularity: async (limit?: number, category?: string, tier?: string) => {
    const params = new URLSearchParams();
    if (limit) params.append('limit', limit.toString());
    if (category) params.append('category', category);
    if (tier) params.append('tier', tier);
    
    const response = await api.get(`/merchants/popularity-ranking?${params.toString()}`);
    return response.data;
  },

  getMerchantCategories: async () => {
    const response = await api.get('/merchants/categories');
    return response.data;
  },

  getMerchantTiers: async () => {
    const response = await api.get('/merchants/tiers');
    return response.data;
  },

  getGrowthMerchants: async (minGrowthRate?: number) => {
    const params = new URLSearchParams();
    if (minGrowthRate) params.append('min_growth_rate', minGrowthRate.toString());
    
    const response = await api.get(`/merchants/growth-merchants?${params.toString()}`);
    return response.data;
  },
};

// Card Reviews API
export const cardReviewsAPI = {
  getCardReviews: async (cardId: string, params?: any) => {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await api.get(`/reviews/cards/${cardId}/reviews?${queryParams.toString()}`);
    return response.data;
  },
  
  createReview: async (cardId: string, reviewData: any) => {
    const response = await api.post(`/reviews/cards/${cardId}/reviews`, reviewData);
    return response.data;
  },
  
  updateReview: async (reviewId: string, reviewData: any) => {
    const response = await api.put(`/reviews/${reviewId}`, reviewData);
    return response.data;
  },
  
  deleteReview: async (reviewId: string) => {
    const response = await api.delete(`/reviews/${reviewId}`);
    return response.data;
  },
  
  voteOnReview: async (reviewId: string, voteType: 'helpful' | 'not_helpful') => {
    const response = await api.post(`/reviews/${reviewId}/vote`, { vote_type: voteType });
    return response.data;
  },
};

// Community API
export const communityAPI = {
  // Posts
  getCardPosts: async (cardId: string, params?: {
    skip?: number;
    limit?: number;
    sort_by?: 'newest' | 'oldest' | 'votes';
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.sort_by) queryParams.append('sort_by', params.sort_by);
    
    const response = await api.get(`/community/cards/${cardId}/posts?${queryParams.toString()}`);
    return response.data;
  },

  createPost: async (cardId: string, postData: { title: string; body?: string }) => {
    const response = await api.post(`/community/cards/${cardId}/posts`, postData);
    return response.data;
  },

  getPostDetail: async (postId: string) => {
    const response = await api.get(`/community/posts/${postId}`);
    return response.data;
  },

  updatePost: async (postId: string, postData: { title: string; body?: string }) => {
    const response = await api.put(`/community/posts/${postId}`, postData);
    return response.data;
  },

  deletePost: async (postId: string) => {
    const response = await api.delete(`/community/posts/${postId}`);
    return response.data;
  },

  // Comments
  createComment: async (postId: string, commentData: { body: string; parent_id?: number }) => {
    const response = await api.post(`/community/posts/${postId}/comments`, commentData);
    return response.data;
  },

  updateComment: async (commentId: string, commentData: { body: string }) => {
    const response = await api.put(`/community/comments/${commentId}`, commentData);
    return response.data;
  },

  deleteComment: async (commentId: string) => {
    const response = await api.delete(`/community/comments/${commentId}`);
    return response.data;
  },

  // Voting
  voteOnPost: async (postId: string, voteType: 'upvote' | 'downvote') => {
    const response = await api.post(`/community/posts/${postId}/vote`, { vote_type: voteType });
    return response.data;
  },

  voteOnComment: async (commentId: string, voteType: 'upvote' | 'downvote') => {
    const response = await api.post(`/community/comments/${commentId}/vote`, { vote_type: voteType });
    return response.data;
  },

  getTopDiscussions: async (limit: number = 5) => {
    const response = await api.get(`/community/top-discussions?limit=${limit}`);
    return response.data;
  },
};

// Admin API
export const adminAPI = {
  getStats: async () => {
    const response = await api.get('/admin/stats');
    return response.data;
  },

  getUsers: async (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    role_filter?: string;
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.search) queryParams.append('search', params.search);
    if (params?.role_filter) queryParams.append('role_filter', params.role_filter);
    
    const response = await api.get(`/admin/users?${queryParams.toString()}`);
    return response.data;
  },

  getModeratorRequests: async (params?: {
    status_filter?: string;
    skip?: number;
    limit?: number;
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.status_filter) queryParams.append('status_filter', params.status_filter);
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await api.get(`/admin/moderator-requests?${queryParams.toString()}`);
    return response.data;
  },

  reviewModeratorRequest: async (requestId: number, reviewData: { status: string }) => {
    const response = await api.put(`/admin/moderator-requests/${requestId}`, reviewData);
    return response.data;
  },

  getEditSuggestions: async (params?: {
    status_filter?: string;
    field_type?: string;
    skip?: number;
    limit?: number;
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.status_filter) queryParams.append('status_filter', params.status_filter);
    if (params?.field_type) queryParams.append('field_type', params.field_type);
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await api.get(`/admin/edit-suggestions?${queryParams.toString()}`);
    return response.data;
  },

  reviewEditSuggestion: async (suggestionId: number, reviewData: { 
    status: string; 
    review_notes?: string;
  }) => {
    const response = await api.put(`/admin/edit-suggestions/${suggestionId}`, reviewData);
    return response.data;
  },

  getCardDocuments: async (params?: {
    status_filter?: string;
    document_type?: string;
    skip?: number;
    limit?: number;
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.status_filter) queryParams.append('status_filter', params.status_filter);
    if (params?.document_type) queryParams.append('document_type', params.document_type);
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await api.get(`/admin/card-documents?${queryParams.toString()}`);
    return response.data;
  },

  reviewCardDocument: async (documentId: number, reviewData: { 
    status: string; 
    review_notes?: string;
  }) => {
    const response = await api.put(`/admin/card-documents/${documentId}`, reviewData);
    return response.data;
  },
};

// Moderator API
export const moderatorAPI = {
  getStats: async () => {
    const response = await api.get('/moderator/stats');
    return response.data;
  },

  getEditSuggestions: async (params?: {
    status_filter?: string;
    field_type?: string;
    skip?: number;
    limit?: number;
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.status_filter) queryParams.append('status_filter', params.status_filter);
    if (params?.field_type) queryParams.append('field_type', params.field_type);
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await api.get(`/moderator/edit-suggestions?${queryParams.toString()}`);
    return response.data;
  },

  reviewSuggestion: async (suggestionId: number, reviewData: { 
    status: string; 
    review_notes?: string;
  }) => {
    const response = await api.put(`/moderator/edit-suggestions/${suggestionId}`, reviewData);
    return response.data;
  },
};

// User Roles API
export const userRolesAPI = {
  requestModerator: async (requestData: { request_reason?: string }) => {
    const response = await api.post('/user-roles/request-moderator', requestData);
    return response.data;
  },

  getMyModeratorRequest: async () => {
    const response = await api.get('/user-roles/my-moderator-request');
    return response.data;
  },

  getMyRole: async () => {
    const response = await api.get('/user-roles/my-role');
    return response.data;
  },

  submitEditSuggestion: async (cardId: number, suggestionData: {
    field_type: string;
    field_name: string;
    new_value: string;
    suggestion_reason?: string;
  }) => {
    const response = await api.post(`/user-roles/edit-suggestions?card_id=${cardId}`, suggestionData);
    return response.data;
  },

  getMySuggestions: async (params?: {
    status_filter?: string;
    skip?: number;
    limit?: number;
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.status_filter) queryParams.append('status_filter', params.status_filter);
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await api.get(`/user-roles/my-suggestions?${queryParams.toString()}`);
    return response.data;
  },

  getMySuggestionsStats: async () => {
    const response = await api.get('/user-roles/my-suggestions/stats');
    return response.data;
  },
};

// Card Documents API
export const cardDocumentsAPI = {
  submitDocument: async (cardId: number, formData: FormData) => {
    const response = await api.post(`/card-documents/submit?card_id=${cardId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getMySubmissions: async (params?: {
    status_filter?: string;
    skip?: number;
    limit?: number;
  }) => {
    const queryParams = new URLSearchParams();
    if (params?.status_filter) queryParams.append('status_filter', params.status_filter);
    if (params?.skip) queryParams.append('skip', params.skip.toString());
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    
    const response = await api.get(`/card-documents/my-submissions?${queryParams.toString()}`);
    return response.data;
  },

  getMySubmissionsStats: async () => {
    const response = await api.get('/card-documents/my-submissions/stats');
    return response.data;
  },

  getApprovedDocuments: async (cardId: number) => {
    const response = await api.get(`/card-documents/approved/${cardId}`);
    return response.data;
  },

  downloadDocument: async (documentId: number) => {
    // Create a direct download link
    const baseURL = process.env.NODE_ENV === 'production' 
      ? 'https://smartcards-ai-2.onrender.com/api/v1'  // Render backend URL
      : 'http://localhost:8000/api/v1';
    
    const downloadURL = `${baseURL}/card-documents/download/${documentId}`;
    
    // Create a temporary link and trigger download
    const link = document.createElement('a');
    link.href = downloadURL;
    link.download = ''; // Let the server set the filename
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  },
};

// SQL Agent API - Now integrated into main backend
const sqlAgentAPI = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://smartcards-ai-backend.onrender.com/api/v1'  // Production backend URL
    : 'http://localhost:8001/api/v1',  // Local backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth interceptor for SQL Agent API since it's now part of main backend
sqlAgentAPI.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const sqlAgentServiceAPI = {
  // Query endpoint
  processQuery: async (queryData: {
    query: string;
    user_id?: number;
    context?: any;
    include_sql?: boolean;
    include_explanation?: boolean;
    max_results?: number;
  }) => {
    const response = await sqlAgentAPI.post('/sql-agent/query', queryData);
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await sqlAgentAPI.get('/sql-agent/health');
    return response.data;
  },

  // Chat endpoints
  createConversation: async (conversationData: { title: string; user_id: number }) => {
    const response = await sqlAgentAPI.post('/chat/conversations', conversationData);
    return response.data;
  },

  getConversations: async (user_id: number) => {
    const response = await sqlAgentAPI.get(`/chat/conversations?user_id=${user_id}`);
    return response.data;
  },

  getChatHistory: async (conversation_id: string) => {
    const response = await sqlAgentAPI.get(`/chat/conversations/${conversation_id}/history`);
    return response.data;
  },

  deleteConversation: async (conversation_id: string) => {
    const response = await sqlAgentAPI.delete(`/chat/conversations/${conversation_id}`);
    return response.data;
  },

  // Document endpoints
  uploadDocument: async (formData: FormData) => {
    const response = await sqlAgentAPI.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getDocuments: async (user_id: number) => {
    const response = await sqlAgentAPI.get(`/documents?user_id=${user_id}`);
    return response.data;
  },

  getDocument: async (document_id: string) => {
    const response = await sqlAgentAPI.get(`/documents/${document_id}`);
    return response.data;
  },

  deleteDocument: async (document_id: string) => {
    const response = await sqlAgentAPI.delete(`/documents/${document_id}`);
    return response.data;
  },
};

export default api; 