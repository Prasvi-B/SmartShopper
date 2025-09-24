import React from 'react';
import { Link } from 'react-router-dom';
import { AlertCircle, Home, ArrowLeft } from 'lucide-react';

const ErrorPage = ({ 
  title = "Something went wrong", 
  message = "We encountered an unexpected error. Please try again later.",
  showBackButton = true,
  showHomeButton = true 
}) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-red-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="relative w-full max-w-md">
        <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8 text-center shadow-2xl">
          {/* Error Icon */}
          <div className="inline-flex items-center justify-center w-16 h-16 bg-red-500/20 border border-red-500/30 rounded-full mb-6">
            <AlertCircle className="w-8 h-8 text-red-400" />
          </div>

          {/* Error Message */}
          <h1 className="text-2xl font-bold text-white mb-4">{title}</h1>
          <p className="text-gray-300 mb-8">{message}</p>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {showBackButton && (
              <button
                onClick={() => window.history.back()}
                className="flex items-center justify-center space-x-2 px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg text-white transition-all"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Go Back</span>
              </button>
            )}
            
            {showHomeButton && (
              <Link
                to="/"
                className="flex items-center justify-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 rounded-lg text-white font-medium transition-all"
              >
                <Home className="w-4 h-4" />
                <span>Go Home</span>
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// 404 Not Found Page
export const NotFoundPage = () => (
  <ErrorPage
    title="Page Not Found"
    message="The page you're looking for doesn't exist or has been moved."
  />
);

// Generic Error Boundary Component
export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorPage
          title="Application Error"
          message="Something went wrong while loading the application. Please refresh the page or try again later."
          showBackButton={false}
        />
      );
    }

    return this.props.children;
  }
}

export default ErrorPage;