import React, { useEffect, useState } from 'react';
import { adminAPI } from '../../services/api';
import Layout from '../../components/Layout/Layout';

interface DAUEntry {
  day: string;
  dau: number;
}

const AdminAnalyticsPage: React.FC = () => {
  const [dau, setDau] = useState<DAUEntry[]>([]);
  const [mau, setMau] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      setLoading(true);
      setError(null);
      try {
        const dauData = await adminAPI.getDAU();
        const mauData = await adminAPI.getMAU();
        setDau(dauData);
        setMau(mauData.mau);
      } catch (err: any) {
        setError(err?.message || 'Failed to fetch analytics');
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  return (
    <Layout>
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Admin Analytics</h1>
        {loading ? (
          <p>Loading analytics...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : (
          <>
            <div className="mb-6">
              <h2 className="text-xl font-semibold">Monthly Active Users (MAU)</h2>
              <p className="text-lg">{mau}</p>
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-2">Daily Active Users (DAU) - Last 30 Days</h2>
              <table className="min-w-full border">
                <thead>
                  <tr>
                    <th className="border px-2 py-1">Date</th>
                    <th className="border px-2 py-1">DAU</th>
                  </tr>
                </thead>
                <tbody>
                  {dau.map((entry) => (
                    <tr key={entry.day}>
                      <td className="border px-2 py-1">{entry.day}</td>
                      <td className="border px-2 py-1">{entry.dau}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </Layout>
  );
};

export default AdminAnalyticsPage;
