import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuth } from './useAuth';
import { analyticsAPI } from '../services/api';

/**
 * Tracks time spent on each page and sends a page_duration event to the backend
 * on every route change. Only fires for authenticated users. Fails silently.
 */
const usePageAnalytics = () => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  const startTimeRef = useRef<number>(Date.now());
  const pathRef = useRef<string>(location.pathname);

  useEffect(() => {
    startTimeRef.current = Date.now();
    pathRef.current = location.pathname;

    return () => {
      if (!isAuthenticated) return;
      const duration = Math.round((Date.now() - startTimeRef.current) / 1000);
      if (duration < 1) return; // ignore sub-second visits
      analyticsAPI.ingestEvent(pathRef.current, duration).catch(() => {});
    };
  }, [location.pathname, isAuthenticated]);
};

export default usePageAnalytics;
