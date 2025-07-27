import React from 'react';
import { Link } from 'react-router-dom';
import { CreditCard } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="mt-auto px-6 py-8 bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <CreditCard className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold">UNGI SmartCards AI</span>
          </div>
          <div className="flex items-center space-x-6">
            <Link
              to="/about"
              className="text-gray-400 hover:text-white transition-colors text-sm"
            >
              About Us
            </Link>
            <a
              href="#"
              className="text-gray-400 hover:text-white transition-colors text-sm"
            >
              Privacy Policy
            </a>
            <a
              href="#"
              className="text-gray-400 hover:text-white transition-colors text-sm"
            >
              Terms of Service
            </a>
            <div className="text-gray-400 text-sm">
              © 2024 UNGI SmartCards AI. Every swipe, Optimized.
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 