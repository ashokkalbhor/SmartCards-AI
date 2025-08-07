// Breadcrumb Test Utility
// This file helps test breadcrumb navigation for all routes

export const testRoutes = [
  // Public routes
  { path: '/', expected: [] },
  { path: '/about', expected: ['Home', 'About'] },
  { path: '/privacy-policy', expected: ['Home', 'Privacy Policy'] },
  { path: '/terms-of-service', expected: ['Home', 'Terms Of Service'] },
  { path: '/login', expected: ['Home', 'Login'] },
  { path: '/register', expected: ['Home', 'Register'] },
  
  // Protected routes
  { path: '/dashboard', expected: [] }, // Should not show breadcrumb
  { path: '/cards', expected: ['Home', 'My Cards'] },
  { path: '/cards/add', expected: ['Home', 'My Cards', 'Add Card'] },
  { path: '/cards/compare', expected: ['Home', 'My Cards', 'Compare Cards'] },
  { path: '/cards/123', expected: ['Home', 'My Cards', 'Card Details'] },
  { path: '/cards/123/edit', expected: ['Home', 'My Cards', 'Card Details', 'Edit Card'] },
  { path: '/card/123', expected: ['Home', 'Card Details', 'Card Details'] },
  { path: '/all-cards', expected: ['Home', 'All Cards'] },
  { path: '/transactions', expected: ['Home', 'Transactions'] },
  { path: '/rewards', expected: ['Home', 'Rewards'] },
  { path: '/recommendations', expected: ['Home', 'Recommendations'] },
  { path: '/profile', expected: ['Home', 'Profile'] },
  { path: '/settings', expected: ['Home', 'Settings'] },
  { path: '/community/123', expected: ['Home', 'Community', 'Card Details'] },
  { path: '/community/post/456', expected: ['Home', 'Community', 'Post Details', 'Post Details'] },
  { path: '/admin', expected: ['Home', 'Admin Dashboard'] },
];

export const testBreadcrumbNavigation = (pathname: string, isAuthenticated: boolean = true) => {
  const pathSegments = pathname.split('/').filter(Boolean);
  const breadcrumbs: string[] = [];
  
  // Always start with Home
  breadcrumbs.push('Home');
  
  if (pathSegments.length === 0) {
    return breadcrumbs;
  }
  
  pathSegments.forEach((segment, index) => {
    // Map route segments to readable labels
    let label = segment.charAt(0).toUpperCase() + segment.slice(1);
    
    // Special mappings
    const labelMappings: Record<string, string> = {
      'dashboard': 'Dashboard',
      'cards': 'My Cards',
      'card': 'Card Details',
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
      'about': 'About',
      'all-cards': 'All Cards',
      'community': 'Community',
      'post': 'Post Details',
      'admin': 'Admin Dashboard',
      'privacy-policy': 'Privacy Policy',
      'terms-of-service': 'Terms Of Service'
    };
    
    if (labelMappings[segment]) {
      label = labelMappings[segment];
    }
    
    // Handle dynamic segments
    if (segment.match(/^\d+$/)) {
      const previousSegment = index > 0 ? pathSegments[index - 1] : '';
      const nextSegment = index < pathSegments.length - 1 ? pathSegments[index + 1] : '';
      
      if (previousSegment === 'card' || previousSegment === 'cards') {
        label = 'Card Details';
      } else if (previousSegment === 'community' && nextSegment === 'post') {
        label = 'Post Details';
      } else if (previousSegment === 'post') {
        label = 'Post Details';
      } else {
        label = 'Details';
      }
    }
    
    breadcrumbs.push(label);
  });
  
  return breadcrumbs;
};

export const validateBreadcrumbPaths = (pathname: string) => {
  const pathSegments = pathname.split('/').filter(Boolean);
  const paths: string[] = [];
  
  let currentPath = '';
  pathSegments.forEach((segment) => {
    currentPath += `/${segment}`;
    paths.push(currentPath);
  });
  
  return paths;
}; 