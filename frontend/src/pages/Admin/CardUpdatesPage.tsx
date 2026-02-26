import React from 'react';
import { CardUpdateAdmin } from '../../components/admin/CardUpdateAdmin';

/**
 * Admin page for managing automated card data updates
 */
const CardUpdatesPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-background-primary">
      <CardUpdateAdmin />
    </div>
  );
};

export default CardUpdatesPage;
