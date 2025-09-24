import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Search, Sparkles, ShoppingBag, Star, TrendingUp, User, Heart } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import SearchBar from '../components/SearchBar'

const Home = () => {
  const navigate = useNavigate()
  const { user } = useAuth()

  const handleSearch = (query) => {
    navigate(`/search?q=${encodeURIComponent(query)}`)
  }

  const features = [
    {
      icon: <Search className="h-8 w-8 text-blue-600" />,
      title: "Multi-Platform Search",
      description: "Compare prices across Amazon, Flipkart, and other major e-commerce platforms"
    },
    {
      icon: <Star className="h-8 w-8 text-yellow-500" />,
      title: "Smart Review Analysis",
      description: "AI-powered sentiment analysis of product reviews to help you make informed decisions"
    },
    {
      icon: <TrendingUp className="h-8 w-8 text-green-600" />,
      title: "Price Tracking",
      description: "Get notified when your favorite products drop to your target price"
    },
    {
      icon: <Sparkles className="h-8 w-8 text-purple-600" />,
      title: "Smart Recommendations",
      description: "Find the best platform to buy based on price, reviews, and seller reputation"
    }
  ]

  return (
    <div className="space-y-16 animate-fadeInUp">
      {/* Welcome Section for Authenticated Users */}
      {user && (
        <div className="bg-gradient-to-r from-blue-500/10 to-purple-600/10 rounded-2xl p-6 border border-blue-500/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                <User className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-primary-600 dark:text-accent-blue">
                  Welcome back, {user.username}!
                </h2>
                <p className="text-slate-600 dark:text-gray-300">
                  Ready to find your next great deal?
                </p>
              </div>
            </div>
            <div className="flex space-x-3">
              <Link
                to="/dashboard"
                className="flex items-center space-x-2 px-4 py-2 bg-blue-500/20 hover:bg-blue-500/30 border border-blue-500/30 rounded-lg text-blue-600 dark:text-blue-400 transition-all"
              >
                <Heart className="w-4 h-4" />
                <span>Dashboard</span>
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Hero Section */}
      <div className="text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold text-primary-600 dark:text-accent-blue mb-6 drop-shadow-glow">
            Smart Shopping Made
            <span className="text-accent-blue"> Simple</span>
          </h1>
          <p className="text-xl text-slate-600 dark:text-gray-50 mb-8 max-w-2xl mx-auto">
            Compare prices, analyze reviews, and make informed purchasing decisions 
            with our AI-powered shopping assistant.
          </p>
          {/* Search Bar */}
          <div className="max-w-2xl mx-auto">
            <SearchBar onSearch={handleSearch} placeholder="Search for products..." />
          </div>
          {/* Quick suggestions */}
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            <span className="text-sm text-slate-500 dark:text-gray-50">Popular searches:</span>
            {['iPhone 15', 'MacBook Pro', 'AirPods', 'Samsung Galaxy'].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => handleSearch(suggestion)}
                className="px-3 py-1 bg-gray-100 dark:bg-dark-card hover:bg-gray-200 dark:hover:bg-slate-700 rounded-full text-sm text-gray-700 dark:text-white transition-colors shadow-glass backdrop-blur-xs"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {features.map((feature, index) => (
          <div key={index} className="text-center p-6 bg-white dark:bg-dark-card rounded-xl shadow-glass hover:shadow-glow transition-shadow animate-fadeInUp">
            <div className="flex justify-center mb-4">
              {feature.icon}
            </div>
            <h3 className="text-lg font-semibold text-primary-600 dark:text-accent-blue mb-2 drop-shadow-glow">
              {feature.title}
            </h3>
            <p className="text-slate-600 dark:text-gray-50 text-sm">
              {feature.description}
            </p>
          </div>
        ))}
      </div>

      {/* Stats Section */}
      <div className="bg-blue-50 dark:bg-dark-card rounded-2xl p-8 text-center shadow-glass animate-fadeInUp">
        <h2 className="text-3xl font-bold text-primary-600 dark:text-accent-blue mb-8 drop-shadow-glow">Trusted by Smart Shoppers</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="text-3xl font-bold text-primary-600 dark:text-accent-blue mb-2">50K+</div>
            <div className="text-slate-600 dark:text-gray-50">Products Analyzed</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary-600 dark:text-accent-blue mb-2">₹2M+</div>
            <div className="text-slate-600 dark:text-gray-50">Money Saved</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary-600 dark:text-accent-blue mb-2">10K+</div>
            <div className="text-slate-600 dark:text-gray-50">Happy Users</div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center bg-gradient-accent rounded-2xl p-12 text-white shadow-glow animate-fadeInUp">
        <ShoppingBag className="h-16 w-16 mx-auto mb-6 opacity-90" />
        <h2 className="text-3xl font-bold mb-4">
          {user ? 'Continue Your Smart Shopping Journey' : 'Ready to Shop Smarter?'}
        </h2>
        <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
          {user 
            ? 'Access your wishlist, price alerts, and personalized recommendations.'
            : 'Join thousands of users who save money and time with our intelligent shopping platform.'
          }
        </p>
        <div className="flex justify-center space-x-4">
          <button
            onClick={() => document.getElementById('search-input')?.focus()}
            className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 dark:hover:bg-dark-card transition-colors shadow-glass backdrop-blur-xs"
          >
            Start Searching
          </button>
          {user ? (
            <Link
              to="/dashboard"
              className="bg-white/20 backdrop-blur-lg border border-white/30 text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/30 transition-all"
            >
              View Dashboard
            </Link>
          ) : (
            <Link
              to="/register"
              className="bg-white/20 backdrop-blur-lg border border-white/30 text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/30 transition-all"
            >
              Join Now
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}

export default Home
