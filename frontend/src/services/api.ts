import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://smartcards-ai-2.onrender.com/api/v1'  // Render backend URL
    : 'http://localhost:8000/api/v1',
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
            : 'http://localhost:8000/api/v1/auth/refresh',
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
};

export default api; 