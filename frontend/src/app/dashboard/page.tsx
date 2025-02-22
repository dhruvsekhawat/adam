'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Screen from '@/components/Screen';
import Card from '@/components/Card';
import { logout, getUserInfo, processEmails, queryAssistant, analyzeWritingStyle } from '@/utils/api';

interface UserInfo {
  email: string;
  full_name: string;
  is_active: boolean;
}

interface WritingStyle {
  tone?: string;
  common_phrases?: string[];
  greeting_style?: string;
  sign_off_style?: string;
  vocabulary_preferences?: string[];
}

export default function DashboardPage() {
  const router = useRouter();
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [writingStyle, setWritingStyle] = useState<WritingStyle | null>(null);

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const info = await getUserInfo();
        if (!info) {
          router.push('/login');
          return;
        }
        setUserInfo(info);
        // Fetch writing style analysis when user info is loaded
        const style = await analyzeWritingStyle();
        setWritingStyle(style);
      } catch (error) {
        console.error('Error fetching user info:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    fetchUserInfo();
  }, [router]);

  const handleProcessEmails = async () => {
    setProcessing(true);
    try {
      await processEmails(100);
      // You might want to show a success message here
    } catch (error) {
      console.error('Error processing emails:', error);
    } finally {
      setProcessing(false);
    }
  };

  const handleQuery = async () => {
    if (!query.trim()) return;
    
    try {
      const result = await queryAssistant(query);
      setResponse(result?.response || 'No response from assistant');
    } catch (error) {
      console.error('Error querying assistant:', error);
      setResponse('Error getting response from assistant');
    }
  };

  if (loading) {
    return (
      <Screen>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-4">Loading...</h2>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mx-auto"></div>
          </div>
        </div>
      </Screen>
    );
  }

  return (
    <Screen>
      <div className="min-h-screen bg-primary">
        <div className="container mx-auto px-6 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold">Dashboard</h1>
            <button
              onClick={logout}
              className="px-4 py-2 border-2 border-black rounded-lg hover:bg-black hover:text-white transition-colors"
            >
              Logout
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* User Info Card */}
            <Card variant="small" className="p-6 bg-white shadow-lg">
              <h3 className="text-xl font-semibold mb-2">Welcome, {userInfo?.full_name}!</h3>
              <div className="text-gray-600">
                <p className="mb-2">Email: {userInfo?.email}</p>
                <p className="mb-2">Status: {userInfo?.is_active ? 'Active' : 'Inactive'}</p>
              </div>
            </Card>

            {/* Email Processing Card */}
            <Card variant="small" className="p-6 bg-white shadow-lg">
              <h3 className="text-xl font-semibold mb-4">Email Processing</h3>
              <button
                onClick={handleProcessEmails}
                disabled={processing}
                className="w-full px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors disabled:bg-gray-400"
              >
                {processing ? 'Processing...' : 'Process Recent Emails'}
              </button>
            </Card>
          </div>

          {/* Assistant Query Card */}
          <Card variant="large" className="p-6 bg-white shadow-lg mb-6">
            <h3 className="text-xl font-semibold mb-4">Ask Assistant</h3>
            <div className="space-y-4">
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask me anything about your emails..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
                rows={4}
              />
              <button
                onClick={handleQuery}
                className="px-6 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
              >
                Ask
              </button>
              {response && (
                <div className="mt-4 p-4 bg-gray-100 rounded-lg">
                  <p className="whitespace-pre-wrap">{response}</p>
                </div>
              )}
            </div>
          </Card>

          {/* Writing Style Analysis Card */}
          {writingStyle && (
            <Card variant="large" className="p-6 bg-white shadow-lg">
              <h3 className="text-xl font-semibold mb-4">Your Writing Style Analysis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-semibold mb-2">Tone</h4>
                  <p className="text-gray-600">{writingStyle.tone || 'Not enough data'}</p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Common Phrases</h4>
                  <ul className="list-disc list-inside text-gray-600">
                    {writingStyle.common_phrases?.map((phrase, index) => (
                      <li key={index}>{phrase}</li>
                    )) || 'Not enough data'}
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Greeting Style</h4>
                  <p className="text-gray-600">{writingStyle.greeting_style || 'Not enough data'}</p>
                </div>
                <div>
                  <h4 className="font-semibold mb-2">Sign-off Style</h4>
                  <p className="text-gray-600">{writingStyle.sign_off_style || 'Not enough data'}</p>
                </div>
              </div>
            </Card>
          )}
        </div>
      </div>
    </Screen>
  );
} 