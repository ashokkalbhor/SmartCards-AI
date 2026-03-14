import React from 'react';
import { Link } from 'react-router-dom';
import { CreditCard } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="px-6 py-2 bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between">
          <div className="text-gray-400 text-xs">© 2025 UNGI SmartCards AI. Every swipe, Optimized.</div>
          <div className="flex items-center space-x-4">
            <Link to="/about" className="text-gray-400 hover:text-white transition-colors text-xs">About Us</Link>
            <Link to="/privacy-policy" className="text-gray-400 hover:text-white transition-colors text-xs">Privacy Policy</Link>
            <Link to="/terms-of-service" className="text-gray-400 hover:text-white transition-colors text-xs">Terms of Service</Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 