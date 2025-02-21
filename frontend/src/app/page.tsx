"use client";

import { useEffect, useState } from "react";

interface HealthStatus {
  status: string;
  version: string;
  environment: string;
  service: string;
}

export default function Home() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
        if (!response.ok) {
          throw new Error(`Failed to fetch health status: ${response.statusText}`);
        }
        const data = await response.json();
        setHealth(data);
        setError(null);
      } catch (err) {
        console.error('Health check error:', err);
        setError(err instanceof Error ? err.message : "Failed to connect to backend");
        setHealth(null);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
    // Poll health status every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-2xl mx-auto space-y-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Welcome to Adam AI
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Your AI-powered executive assistant
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
                System Status
              </h2>
              {loading && (
                <div className="animate-pulse text-gray-400 dark:text-gray-500">
                  Checking status...
                </div>
              )}
            </div>
            
            {error && (
              <div className="bg-red-50 dark:bg-red-900/50 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-200 p-4 rounded-lg mb-4">
                <p className="flex items-center">
                  <span className="mr-2">⚠️</span>
                  {error}
                </p>
              </div>
            )}
            
            {health && (
              <div className="space-y-4">
                <div className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
                  <span className="text-gray-600 dark:text-gray-400">Status</span>
                  <span className="font-medium text-green-600 dark:text-green-400 flex items-center">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    {health.status}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
                  <span className="text-gray-600 dark:text-gray-400">Service</span>
                  <span className="font-medium text-gray-900 dark:text-white">
                    {health.service}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700">
                  <span className="text-gray-600 dark:text-gray-400">Version</span>
                  <span className="font-medium text-gray-900 dark:text-white">
                    {health.version}
                  </span>
                </div>
                <div className="flex items-center justify-between py-2">
                  <span className="text-gray-600 dark:text-gray-400">Environment</span>
                  <span className="font-medium text-gray-900 dark:text-white">
                    {health.environment}
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
