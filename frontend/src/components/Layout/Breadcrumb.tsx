import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

interface BreadcrumbItem {
  label: string;
  path: string;
  isActive?: boolean;
}

const Breadcrumb: React.FC = () => {
  const location = useLocation();
  const { isAuthenticated } = useAuth();
  
  // Define the breadcrumb mapping for different routes
  const getBreadcrumbs = (): BreadcrumbItem[] => {
    const pathSegments = location.pathname.split('/').filter(Boolean);
    const breadcrumbs: BreadcrumbItem[] = [];
    
    // Always start with Home - route to dashboard if authenticated, landing page if not
    const homePath = isAuthenticated ? '/dashboard' : '/';
    breadcrumbs.push({
      label: 'Home',
      path: homePath,
      isActive: location.pathname === homePath
    });

    if (pathSegments.length === 0) {
      return breadcrumbs;
    }

    let currentPath = '';
    
    pathSegments.forEach((segment, index) => {
      currentPath += `/${segment}`;
      
      // Map route segments to readable labels
      let label = segment.charAt(0).toUpperCase() + segment.slice(1);
      
      // Special mappings for better readability
      const labelMappings: Record<string, string> = {
        'dashboard': 'Dashboard',
        'cards': 'My Cards',
        'add': 'Add Card',
        'compare': 'Compare Cards',
        'edit': 'Edit Card',
        'transactions': 'Transactions',
        'rewards': 'Rewards',
        'recommendations': 'Recommendations',
        'profile': 'Profile',
        'settings': 'Settings',
        'login': 'Login',
        'register': 'Register',
        'about': 'About'
      };
      
      if (labelMappings[segment]) {
        label = labelMappings[segment];
      }
      
      // Handle dynamic segments (like card IDs)
      if (segment.match(/^\d+$/)) {
        label = 'Card Details';
      }
      
      breadcrumbs.push({
        label,
        path: currentPath,
        isActive: index === pathSegments.length - 1
      });
    });
    
    return breadcrumbs;
  };

  const breadcrumbs = getBreadcrumbs();

  // Don't show breadcrumb on home page or dashboard (for authenticated users)
  if (location.pathname === '/' || (isAuthenticated && location.pathname === '/dashboard')) {
    return null;
  }

  return (
    <nav className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 sm:px-6 py-3">
      <div className="w-full">
        <ol className="flex items-center space-x-1 sm:space-x-2 text-xs sm:text-sm overflow-x-auto">
          {breadcrumbs.map((breadcrumb, index) => (
            <li key={breadcrumb.path} className="flex items-center flex-shrink-0">
              {index > 0 && (
                <ChevronRight className="h-3 w-3 sm:h-4 sm:w-4 text-gray-400 dark:text-gray-500 mx-1 sm:mx-2 flex-shrink-0" />
              )}
              
              {breadcrumb.isActive ? (
                <span className="text-primary-600 dark:text-primary-400 font-medium truncate">
                  {index === 0 ? (
                    <Home className="h-3 w-3 sm:h-4 sm:w-4" />
                  ) : (
                    breadcrumb.label
                  )}
                </span>
              ) : (
                <Link
                  to={breadcrumb.path}
                  className="text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors flex items-center truncate"
                >
                  {index === 0 ? (
                    <Home className="h-3 w-3 sm:h-4 sm:w-4" />
                  ) : (
                    breadcrumb.label
                  )}
                </Link>
              )}
            </li>
          ))}
        </ol>
      </div>
    </nav>
  );
};

export default Breadcrumb; 