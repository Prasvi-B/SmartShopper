import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

// Protected Route Component - requires authentication
const ProtectedRoute = ({ children, redirectTo = '/login' }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  // Show loading state while authentication is being verified
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8">
          <div className="flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
            <p className="text-white text-lg">Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!user) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  return children;
};

// Public Route Component - redirects authenticated users
const PublicRoute = ({ children, redirectTo = '/' }) => {
  const { user, loading } = useAuth();

  // Show loading state while authentication is being verified
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8">
          <div className="flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
            <p className="text-white text-lg">Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  // Redirect authenticated users away from public routes (like login/register)
  if (user) {
    return <Navigate to={redirectTo} replace />;
  }

  return children;
};

// Role-based Route Component - requires specific role
const RoleBasedRoute = ({ children, requiredRole, fallback = '/unauthorized' }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8">
          <div className="flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
            <p className="text-white text-lg">Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Check if user has required role
  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to={fallback} replace />;
  }

  return children;
};

// Admin Route Component - requires admin role
const AdminRoute = ({ children }) => {
  return (
    <RoleBasedRoute requiredRole="admin" fallback="/unauthorized">
      {children}
    </RoleBasedRoute>
  );
};

export { ProtectedRoute, PublicRoute, RoleBasedRoute, AdminRoute };
export default ProtectedRoute;