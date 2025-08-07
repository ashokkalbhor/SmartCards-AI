import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RecoilRoot } from 'recoil';
import { motion, AnimatePresence } from 'framer-motion';

// Components
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import LoadingSpinner from './components/UI/LoadingSpinner';

// Pages
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import LoginPage from './pages/Auth/LoginPage';
import RegisterPage from './pages/Auth/RegisterPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import CardsPage from './pages/Cards/CardsPage';
import AddCardPage from './pages/Cards/AddCardPage';
import CardDetailPage from './pages/Cards/CardDetailPage';
import EditCardPage from './pages/Cards/EditCardPage';
import CardComparisonPage from './pages/Cards/CardComparisonPage';
import AllCardsPage from './pages/Cards/AllCardsPage';
import TransactionsPage from './pages/Transactions/TransactionsPage';
import RewardsPage from './pages/Rewards/RewardsPage';
import RecommendationsPage from './pages/Recommendations/RecommendationsPage';
import ProfilePage from './pages/Profile/ProfilePage';
import SettingsPage from './pages/Settings/SettingsPage';
import CommunityPage from './pages/Community/CommunityPage';
import PostDetailPage from './pages/Community/PostDetailPage';
import AdminDashboardPage from './pages/Admin/AdminDashboardPage';
import PrivacyPolicyPage from './pages/PrivacyPolicyPage';
import TermsOfServicePage from './pages/TermsOfServicePage';

// Hooks
import { useAuth } from './hooks/useAuth';
import { useTheme } from './hooks/useTheme';

// Styles
import './styles/globals.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

function AppContent() {
  const { isAuthenticated, isLoading } = useAuth();
  const { theme } = useTheme();

  // Apply theme to document
  React.useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background-primary flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <Router>
      <AnimatePresence mode="wait">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />
          <Route path="/terms-of-service" element={<TermsOfServicePage />} />
          <Route path="/login" element={
            isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />
          } />
          <Route path="/register" element={
            isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />
          } />

          {/* Protected Routes */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Layout>
                <DashboardPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/cards" element={
            <ProtectedRoute>
              <Layout>
                <CardsPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/cards/add" element={
            <ProtectedRoute>
              <Layout>
                <AddCardPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/cards/compare" element={
            <ProtectedRoute>
              <Layout>
                <CardComparisonPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/cards/:id" element={
            <ProtectedRoute>
              <Layout>
                <CardDetailPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/cards/:id/edit" element={
            <ProtectedRoute>
              <Layout>
                <EditCardPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/card/:cardId" element={
            <ProtectedRoute>
              <Layout>
                <CardDetailPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/all-cards" element={
            <ProtectedRoute>
              <Layout>
                <AllCardsPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/transactions" element={
            <ProtectedRoute>
              <Layout>
                <TransactionsPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/rewards" element={
            <ProtectedRoute>
              <Layout>
                <RewardsPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/recommendations" element={
            <ProtectedRoute>
              <Layout>
                <RecommendationsPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/profile" element={
            <ProtectedRoute>
              <Layout>
                <ProfilePage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/settings" element={
            <ProtectedRoute>
              <Layout>
                <SettingsPage />
              </Layout>
            </ProtectedRoute>
          } />

          {/* Community Routes */}
          <Route path="/community/:cardId" element={
            <ProtectedRoute>
              <Layout>
                <CommunityPage />
              </Layout>
            </ProtectedRoute>
          } />

          <Route path="/community/post/:postId" element={
            <ProtectedRoute>
              <Layout>
                <PostDetailPage />
              </Layout>
            </ProtectedRoute>
          } />

          {/* Admin Routes */}
          <Route path="/admin" element={
            <ProtectedRoute>
              <Layout>
                <AdminDashboardPage />
              </Layout>
            </ProtectedRoute>
          } />

          {/* 404 Route */}
          <Route path="*" element={
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="min-h-screen bg-background-primary flex items-center justify-center"
              {...({} as any)}
            >
              <div className="text-center">
                <h1 className="text-6xl font-bold text-text-primary mb-4">404</h1>
                <p className="text-text-secondary text-xl mb-8">Page not found</p>
                <button
                  onClick={() => window.history.back()}
                  className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg transition-colors"
                >
                  Go Back
                </button>
              </div>
            </motion.div>
          } />
        </Routes>
      </AnimatePresence>
    </Router>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RecoilRoot>
        <AppContent />
      </RecoilRoot>
    </QueryClientProvider>
  );
}

export default App; 