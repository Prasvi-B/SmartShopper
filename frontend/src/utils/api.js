import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

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
          const response = await axios.post(`${API_BASE}/auth/refresh`, {
            refresh_token: refreshToken
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', newRefreshToken);

          // Retry original request
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
)

// Search Products
export const searchProducts = async (query, options = {}) => {
  try {
    const params = {
      q: query,
      ...options,
    }
    const response = await api.get('/search', { params })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Search failed')
  }
}

// Get Product Details
export const getProduct = async (productId) => {
  try {
    const response = await api.get(`/products/${productId}`)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch product')
  }
}

// Get Product Reviews
export const getProductReviews = async (productId) => {
  try {
    const response = await api.get(`/products/${productId}/reviews`)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch reviews')
  }
}

// Get Search Suggestions
export const getSearchSuggestions = async (query) => {
  try {
    const response = await api.get('/search/suggestions', {
      params: { q: query },
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch suggestions')
  }
}

// Create Price Alert
export const createPriceAlert = async (alertData) => {
  try {
    const response = await api.post('/alerts', alertData)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to create alert')
  }
}

// Get User Alerts
export const getUserAlerts = async (userEmail) => {
  try {
    const response = await api.get('/alerts', {
      params: { user_email: userEmail },
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch alerts')
  }
}

// Authentication API
export const authApi = {
  register: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  },

  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  },

  logout: async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    }
  },

  getCurrentUser: async () => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get user data');
    }
  },

  updateProfile: async (userData) => {
    try {
      const response = await api.patch('/auth/me', userData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Profile update failed');
    }
  },

  updatePreferences: async (preferences) => {
    try {
      const response = await api.patch('/auth/me/preferences', preferences);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Preferences update failed');
    }
  },

  refreshToken: async (refreshToken) => {
    try {
      const response = await api.post('/auth/refresh', { refresh_token: refreshToken });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Token refresh failed');
    }
  },
};

// User Features API
export const userApi = {
  // Wishlist
  addToWishlist: async (productId) => {
    try {
      const response = await api.post('/user/wishlist', { product_id: productId });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to add to wishlist');
    }
  },

  getWishlist: async () => {
    try {
      const response = await api.get('/user/wishlist');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get wishlist');
    }
  },

  removeFromWishlist: async (productId) => {
    try {
      await api.delete(`/user/wishlist/${productId}`);
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to remove from wishlist');
    }
  },

  // Price Alerts
  createPriceAlert: async (alertData) => {
    try {
      const response = await api.post('/user/alerts', alertData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to create price alert');
    }
  },

  getPriceAlerts: async (activeOnly = true) => {
    try {
      const response = await api.get('/user/alerts', { params: { active_only: activeOnly } });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get price alerts');
    }
  },

  updatePriceAlert: async (alertId, updateData) => {
    try {
      const response = await api.patch(`/user/alerts/${alertId}`, updateData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to update price alert');
    }
  },

  deletePriceAlert: async (alertId) => {
    try {
      await api.delete(`/user/alerts/${alertId}`);
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to delete price alert');
    }
  },

  // Search History
  getSearchHistory: async (limit = 50) => {
    try {
      const response = await api.get('/user/search-history', { params: { limit } });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get search history');
    }
  },

  deleteSearchHistoryItem: async (searchId) => {
    try {
      await api.delete(`/user/search-history/${searchId}`);
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to delete search history item');
    }
  },

  clearSearchHistory: async () => {
    try {
      await api.delete('/user/search-history');
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to clear search history');
    }
  },

  // Dashboard
  getDashboardStats: async () => {
    try {
      const response = await api.get('/user/dashboard/stats');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get dashboard stats');
    }
  },
};

// Updated product API to match new backend routes
export const productApi = {
  searchProducts: async (params) => {
    try {
      const response = await api.get('/products/search', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Search failed');
    }
  },

  getProduct: async (productId) => {
    try {
      const response = await api.get(`/products/${productId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch product');
    }
  },

  getProductOffers: async (productId) => {
    try {
      const response = await api.get(`/products/${productId}/offers`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch offers');
    }
  },

  listProducts: async (params) => {
    try {
      const response = await api.get('/products', { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to list products');
    }
  },

  getCategories: async () => {
    try {
      const response = await api.get('/products/categories/list');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get categories');
    }
  },

  getBrands: async () => {
    try {
      const response = await api.get('/products/brands/list');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get brands');
    }
  },
};

// Reviews API
export const reviewApi = {
  getProductReviews: async (productId, params) => {
    try {
      const response = await api.get(`/reviews/product/${productId}`, { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get reviews');
    }
  },

  createReview: async (reviewData) => {
    try {
      const response = await api.post('/reviews', reviewData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to create review');
    }
  },

  getReview: async (reviewId) => {
    try {
      const response = await api.get(`/reviews/${reviewId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get review');
    }
  },

  markHelpful: async (reviewId) => {
    try {
      const response = await api.patch(`/reviews/${reviewId}/helpful`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to mark review as helpful');
    }
  },

  getReviewSummary: async (productId) => {
    try {
      const response = await api.get(`/reviews/product/${productId}/summary`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to get review summary');
    }
  },

  analyzeSentiment: async (reviews) => {
    try {
      const response = await api.post('/reviews/sentiment/analyze', { reviews });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to analyze sentiment');
    }
  },
};

export default api
