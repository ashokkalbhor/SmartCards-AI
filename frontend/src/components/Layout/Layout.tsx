import React from 'react';
import Header from './Header';
import Footer from './Footer';
import Breadcrumb from './Breadcrumb';
import { useAuth } from '../../hooks/useAuth';
import usePageAnalytics from '../../hooks/usePageAnalytics';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  usePageAnalytics();

  return (
    <div className="h-screen bg-gray-50 dark:bg-gray-900 flex flex-col overflow-hidden">
      {isAuthenticated && <Header />}
      {isAuthenticated && <Breadcrumb />}
      <main className="flex-1 min-h-0 overflow-y-auto">
        {children}
      </main>
      {isAuthenticated && <Footer />}
    </div>
  );
};

export default Layout; 