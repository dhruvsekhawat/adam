'use client';

import React from 'react';
import Screen from '@/components/Screen';
import Card from '@/components/Card';
import GoogleLoginButton from '@/components/GoogleLoginButton';

export default function LoginPage() {
  return (
    <Screen>
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card variant="small" className="p-8 bg-white shadow-lg">
          <div className="space-y-6">
            <div className="text-center">
              <h1 className="text-2xl font-bold">Welcome Back</h1>
              <p className="text-gray-600 mt-2">Sign in to continue to MyBox</p>
            </div>
            
            <GoogleLoginButton />
            
            <div className="text-center text-sm text-gray-600">
              <p>By continuing, you agree to our</p>
              <div className="space-x-1">
                <a href="/terms" className="underline hover:text-black">Terms of Service</a>
                <span>and</span>
                <a href="/privacy" className="underline hover:text-black">Privacy Policy</a>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </Screen>
  );
} 