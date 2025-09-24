import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import Layout from './components/Layout'
import { ProtectedRoute, PublicRoute } from './components/ProtectedRoute'
import { ErrorBoundary, NotFoundPage } from './pages/ErrorPage'
import Home from './pages/Home'
import Results from './pages/Results'
import ProductDetails from './pages/ProductDetails'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import UserDashboard from './pages/UserDashboard'

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<Results />} />
            <Route path="/product/:id" element={<ProductDetails />} />
            
            {/* Public routes - redirect if authenticated */}
            <Route 
              path="/login" 
              element={
                <PublicRoute>
                  <LoginPage />
                </PublicRoute>
              } 
            />
            <Route 
              path="/register" 
              element={
                <PublicRoute>
                  <RegisterPage />
                </PublicRoute>
              } 
            />
            
            {/* Protected routes - require authentication */}
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <UserDashboard />
                </ProtectedRoute>
              } 
            />
            
            {/* Unauthorized page */}
            <Route 
              path="/unauthorized" 
              element={
                <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
                  <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-8 text-center">
                    <h1 className="text-2xl font-bold text-white mb-4">Unauthorized</h1>
                    <p className="text-gray-300">You don't have permission to access this page.</p>
                  </div>
                </div>
              } 
            />
            
            {/* 404 Not Found - catch all */}
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Layout>
      </AuthProvider>
    </ErrorBoundary>
  )
}

export default App
