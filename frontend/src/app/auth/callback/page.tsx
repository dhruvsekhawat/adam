'use client';

import React, { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { handleAuthCallback, getAuthToken } from '@/utils/api';
import Screen from '@/components/Screen';

export default function AuthCallback() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const processAuth = async () => {
      const token = searchParams.get('token');

      if (token) {
        try {
          await handleAuthCallback(token);
          
          // Verify the cookie was set
          const storedToken = getAuthToken();
          
          if (storedToken) {
            window.location.href = '/dashboard';
          } else {
            setError('Failed to store authentication token');
          }
        } catch (error) {
          setError('Failed to process authentication');
        }
      } else {
        window.location.href = '/login';
      }
    };

    processAuth();
  }, [searchParams]);

  if (error) {
    return (
      <Screen>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-4 text-red-600">{error}</h2>
            <button
              onClick={() => window.location.href = '/login'}
              className="px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800"
            >
              Return to Login
            </button>
          </div>
        </div>
      </Screen>
    );
  }

  return (
    <Screen>
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Signing you in...</h2>
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mx-auto"></div>
        </div>
      </div>
    </Screen>
  );
} 