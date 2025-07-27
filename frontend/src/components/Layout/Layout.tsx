import React from 'react';
import Header from './Header';
import Footer from './Footer';
import Breadcrumb from './Breadcrumb';
import { useAuth } from '../../hooks/useAuth';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col">
      {isAuthenticated && <Header />}
      {isAuthenticated && <Breadcrumb />}
      <main className="flex-1">
        {children}
      </main>
      {isAuthenticated && <Footer />}
    </div>
  );
};

export default Layout; 