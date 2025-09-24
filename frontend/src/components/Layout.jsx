import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Search, ShoppingCart, TrendingUp, Star, User, LogIn, UserPlus } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const Layout = ({ children }) => {
  const [darkMode, setDarkMode] = React.useState(false);
  const { user, logout } = useAuth();
  const location = useLocation();

  // Don't show navigation on login/register pages
  const isAuthPage = location.pathname === '/login' || location.pathname === '/register';

  return (
    <div className={
      `${darkMode ? 'dark' : ''} min-h-screen font-sans bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-dark-bg dark:via-dark-surface dark:to-dark-card transition-all duration-500`
    }>
      {/* Background Effects */}
      <div className="fixed inset-0 bg-gradient-glow pointer-events-none opacity-30"></div>
      
      {/* Navigation */}
      {!isAuthPage && (
        <nav className="relative bg-white/70 dark:bg-dark-card/70 backdrop-blur-lg shadow-glass border-b border-white/20 dark:border-slate-700/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link to="/" className="flex items-center animate-slideInLeft">
                <ShoppingCart className="h-8 w-8 text-primary-600 dark:text-accent-blue animate-float" />
                <span className="ml-3 text-2xl font-bold bg-gradient-accent bg-clip-text text-transparent">
                  SmartShopper
                </span>
              </Link>
              
              <div className="flex items-center space-x-4">
                {/* User Authentication Section */}
                {user ? (
                  <div className="flex items-center space-x-4">
                    <Link
                      to="/dashboard"
                      className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-glass backdrop-blur-lg border border-white/20 dark:border-slate-700/50 text-primary-600 dark:text-white shadow-glass hover:shadow-glow transition-all duration-300 hover:scale-105"
                    >
                      <User className="h-4 w-4" />
                      <span>{user.username}</span>
                    </Link>
                    <button
                      onClick={logout}
                      className="px-4 py-2 rounded-xl bg-gradient-glass backdrop-blur-lg border border-white/20 dark:border-slate-700/50 text-red-600 dark:text-red-400 shadow-glass hover:shadow-glow transition-all duration-300 hover:scale-105"
                    >
                      Logout
                    </button>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Link
                      to="/login"
                      className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-glass backdrop-blur-lg border border-white/20 dark:border-slate-700/50 text-primary-600 dark:text-white shadow-glass hover:shadow-glow transition-all duration-300 hover:scale-105"
                    >
                      <LogIn className="h-4 w-4" />
                      <span>Login</span>
                    </Link>
                    <Link
                      to="/register"
                      className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-glass hover:shadow-glow transition-all duration-300 hover:scale-105"
                    >
                      <UserPlus className="h-4 w-4" />
                      <span>Register</span>
                    </Link>
                  </div>
                )}
                
                {/* Dark Mode Toggle */}
                <button
                  className="px-4 py-2 rounded-xl bg-gradient-glass backdrop-blur-lg border border-white/20 dark:border-slate-700/50 text-primary-600 dark:text-white shadow-glass hover:shadow-glow transition-all duration-300 hover:scale-105 focus:outline-none animate-fadeInUp"
                  onClick={() => setDarkMode((d) => !d)}
                  aria-label="Toggle dark mode"
                >
                  <span className="text-lg">{darkMode ? '🌙' : '☀️'}</span>
                </button>
              </div>
            </div>
          </div>
        </nav>
      )}

      {/* Main Content */}
      <main className="relative max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 min-h-[calc(100vh-200px)]">
        {children}
      </main>

      {/* Footer */}
      <footer className="relative bg-white/70 dark:bg-dark-card/70 backdrop-blur-lg border-t border-white/20 dark:border-slate-700/50 mt-12 shadow-glass-lg">
        <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center">
                <ShoppingCart className="h-8 w-8 text-primary-600 dark:text-accent-blue" />
                <span className="ml-3 text-xl font-bold bg-gradient-accent bg-clip-text text-transparent">
                  SmartShopper
                </span>
              </div>
              <p className="mt-4 text-slate-600 dark:text-slate-300 max-w-md">
                Making smart shopping decisions with AI-powered price comparison and review analysis.
              </p>
            </div>
            <div>
              <h3 className="text-sm font-semibold bg-gradient-accent bg-clip-text text-transparent tracking-wider uppercase">Features</h3>
              <ul className="mt-4 space-y-3">
                <li className="flex items-center text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-accent-blue transition-colors">
                  <Search className="h-4 w-4 mr-2 text-primary-500" />
                  Price Comparison
                </li>
                <li className="flex items-center text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-accent-blue transition-colors">
                  <Star className="h-4 w-4 mr-2 text-amber-500" />
                  Review Analysis
                </li>
                <li className="flex items-center text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-accent-blue transition-colors">
                  <TrendingUp className="h-4 w-4 mr-2 text-emerald-500" />
                  Price Alerts
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold bg-gradient-accent bg-clip-text text-transparent tracking-wider uppercase">Support</h3>
              <ul className="mt-4 space-y-3">
                <li>
                  <a href="#" className="text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-accent-blue transition-colors">About</a>
                </li>
                <li>
                  <a href="#" className="text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-accent-blue transition-colors">Contact</a>
                </li>
                <li>
                  <a href="#" className="text-slate-600 dark:text-slate-300 hover:text-primary-600 dark:hover:text-accent-blue transition-colors">Privacy</a>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-slate-700">
            <p className="text-center text-slate-400 dark:text-gray-50">
              © 2024 SmartShopper. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout