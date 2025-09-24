import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { 
  User, 
  Heart, 
  Bell, 
  Search, 
  Settings, 
  TrendingDown,
  Eye,
  Trash2,
  Edit3,
  LogOut
} from 'lucide-react';
import { 
  getUserProfile, 
  getWishlist, 
  getPriceAlerts, 
  getSearchHistory,
  deleteWishlistItem,
  deletePriceAlert,
  deleteSearchHistoryItem
} from '../utils/api';

const UserDashboard = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    profile: null,
    wishlist: [],
    priceAlerts: [],
    searchHistory: []
  });

  useEffect(() => {
    if (user) {
      loadUserData();
    }
  }, [user]);

  const loadUserData = async () => {
    setLoading(true);
    try {
      const [profileRes, wishlistRes, alertsRes, historyRes] = await Promise.all([
        getUserProfile(),
        getWishlist(),
        getPriceAlerts(),
        getSearchHistory()
      ]);

      setData({
        profile: profileRes.data,
        wishlist: wishlistRes.data || [],
        priceAlerts: alertsRes.data || [],
        searchHistory: historyRes.data || []
      });
    } catch (error) {
      console.error('Error loading user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteWishlistItem = async (itemId) => {
    try {
      await deleteWishlistItem(itemId);
      setData(prev => ({
        ...prev,
        wishlist: prev.wishlist.filter(item => item.id !== itemId)
      }));
    } catch (error) {
      console.error('Error deleting wishlist item:', error);
    }
  };

  const handleDeletePriceAlert = async (alertId) => {
    try {
      await deletePriceAlert(alertId);
      setData(prev => ({
        ...prev,
        priceAlerts: prev.priceAlerts.filter(alert => alert.id !== alertId)
      }));
    } catch (error) {
      console.error('Error deleting price alert:', error);
    }
  };

  const handleDeleteSearchItem = async (itemId) => {
    try {
      await deleteSearchHistoryItem(itemId);
      setData(prev => ({
        ...prev,
        searchHistory: prev.searchHistory.filter(item => item.id !== itemId)
      }));
    } catch (error) {
      console.error('Error deleting search history item:', error);
    }
  };

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'wishlist', label: 'Wishlist', icon: Heart },
    { id: 'alerts', label: 'Price Alerts', icon: Bell },
    { id: 'history', label: 'Search History', icon: Search }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8">
          <div className="flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
            <p className="text-white text-lg">Loading dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative min-h-screen p-4">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-6 mb-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <User className="w-8 h-8 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-white">
                    Welcome back, {user?.username || 'User'}!
                  </h1>
                  <p className="text-gray-300">Manage your shopping preferences</p>
                </div>
              </div>
              <button
                onClick={logout}
                className="flex items-center space-x-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 rounded-lg text-red-300 hover:text-red-200 transition-all"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>

          {/* Tab Navigation */}
          <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-2 mb-6">
            <div className="flex space-x-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 px-4 py-3 rounded-lg font-medium transition-all ${
                      activeTab === tab.id
                        ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                        : 'text-gray-300 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Tab Content */}
          <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-6">
            {/* Profile Tab */}
            {activeTab === 'profile' && (
              <div className="space-y-6">
                <h2 className="text-xl font-bold text-white mb-4">Profile Information</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div>
                      <label className="block text-gray-300 text-sm font-medium mb-2">Username</label>
                      <div className="p-3 bg-white/10 border border-white/20 rounded-lg text-white">
                        {data.profile?.username || user?.username || 'N/A'}
                      </div>
                    </div>
                    <div>
                      <label className="block text-gray-300 text-sm font-medium mb-2">Email</label>
                      <div className="p-3 bg-white/10 border border-white/20 rounded-lg text-white">
                        {data.profile?.email || user?.email || 'N/A'}
                      </div>
                    </div>
                    <div>
                      <label className="block text-gray-300 text-sm font-medium mb-2">Full Name</label>
                      <div className="p-3 bg-white/10 border border-white/20 rounded-lg text-white">
                        {data.profile?.full_name || 'Not provided'}
                      </div>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-gray-300 text-sm font-medium mb-2">Phone Number</label>
                      <div className="p-3 bg-white/10 border border-white/20 rounded-lg text-white">
                        {data.profile?.phone_number || 'Not provided'}
                      </div>
                    </div>
                    <div>
                      <label className="block text-gray-300 text-sm font-medium mb-2">Date of Birth</label>
                      <div className="p-3 bg-white/10 border border-white/20 rounded-lg text-white">
                        {data.profile?.date_of_birth || 'Not provided'}
                      </div>
                    </div>
                    <div>
                      <label className="block text-gray-300 text-sm font-medium mb-2">Member Since</label>
                      <div className="p-3 bg-white/10 border border-white/20 rounded-lg text-white">
                        {data.profile?.created_at ? new Date(data.profile.created_at).toLocaleDateString() : 'N/A'}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex justify-end">
                  <button className="flex items-center space-x-2 px-4 py-2 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 rounded-lg text-blue-300 hover:text-blue-200 transition-all">
                    <Edit3 className="w-4 h-4" />
                    <span>Edit Profile</span>
                  </button>
                </div>
              </div>
            )}

            {/* Wishlist Tab */}
            {activeTab === 'wishlist' && (
              <div className="space-y-6">
                <h2 className="text-xl font-bold text-white mb-4">Your Wishlist</h2>
                {data.wishlist.length === 0 ? (
                  <div className="text-center py-12">
                    <Heart className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-300 text-lg">Your wishlist is empty</p>
                    <p className="text-gray-400">Start adding products you love!</p>
                  </div>
                ) : (
                  <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {data.wishlist.map((item) => (
                      <div key={item.id} className="bg-white/10 border border-white/20 rounded-lg p-4">
                        <div className="flex justify-between items-start mb-3">
                          <h3 className="text-white font-medium text-sm">{item.product_name}</h3>
                          <button
                            onClick={() => handleDeleteWishlistItem(item.id)}
                            className="text-red-400 hover:text-red-300 transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                        <p className="text-gray-300 text-sm mb-2">Price: ${item.price}</p>
                        <p className="text-gray-400 text-xs">
                          Added: {new Date(item.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Price Alerts Tab */}
            {activeTab === 'alerts' && (
              <div className="space-y-6">
                <h2 className="text-xl font-bold text-white mb-4">Price Alerts</h2>
                {data.priceAlerts.length === 0 ? (
                  <div className="text-center py-12">
                    <Bell className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-300 text-lg">No price alerts set</p>
                    <p className="text-gray-400">Get notified when prices drop!</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {data.priceAlerts.map((alert) => (
                      <div key={alert.id} className="bg-white/10 border border-white/20 rounded-lg p-4">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h3 className="text-white font-medium mb-2">{alert.product_name}</h3>
                            <div className="flex items-center space-x-4 text-sm">
                              <span className="text-gray-300">
                                Target: <span className="text-green-400">${alert.target_price}</span>
                              </span>
                              <span className="text-gray-300">
                                Current: <span className="text-blue-400">${alert.current_price}</span>
                              </span>
                              <span className={`px-2 py-1 rounded-full text-xs ${
                                alert.is_active 
                                  ? 'bg-green-500/20 text-green-300' 
                                  : 'bg-gray-500/20 text-gray-300'
                              }`}>
                                {alert.is_active ? 'Active' : 'Inactive'}
                              </span>
                            </div>
                          </div>
                          <button
                            onClick={() => handleDeletePriceAlert(alert.id)}
                            className="text-red-400 hover:text-red-300 transition-colors ml-4"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Search History Tab */}
            {activeTab === 'history' && (
              <div className="space-y-6">
                <h2 className="text-xl font-bold text-white mb-4">Search History</h2>
                {data.searchHistory.length === 0 ? (
                  <div className="text-center py-12">
                    <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-300 text-lg">No search history</p>
                    <p className="text-gray-400">Your searches will appear here</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {data.searchHistory.map((item) => (
                      <div key={item.id} className="bg-white/10 border border-white/20 rounded-lg p-4">
                        <div className="flex justify-between items-center">
                          <div className="flex items-center space-x-3">
                            <Search className="w-4 h-4 text-gray-400" />
                            <span className="text-white">{item.query}</span>
                            <span className="text-gray-400 text-sm">
                              {new Date(item.searched_at).toLocaleDateString()}
                            </span>
                          </div>
                          <button
                            onClick={() => handleDeleteSearchItem(item.id)}
                            className="text-red-400 hover:text-red-300 transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;