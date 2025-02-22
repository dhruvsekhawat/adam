"use client";

import React from 'react';
import Link from 'next/link';
import { FolderIcon } from 'lucide-react';

export default function Home() {
  return (
    <main className="min-h-screen bg-[#9de3f0]">
      <div className="container mx-auto px-6 py-4">
        {/* Navigation */}
        <nav className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-2">
            <FolderIcon className="h-6 w-6" />
            <span className="text-xl font-semibold">MyBox</span>
          </div>
          
          <div className="flex items-center gap-8">
            <Link href="/" className="hover:text-gray-600">Home</Link>
            <Link href="/how-it-works" className="hover:text-gray-600">How it works</Link>
            <Link href="/faq" className="hover:text-gray-600">FAQ</Link>
            <Link href="/pricing" className="hover:text-gray-600">Pricing</Link>
          </div>

          <Link 
            href="/login"
            className="px-4 py-2 border border-black rounded-lg hover:bg-black hover:text-white transition-colors"
          >
            Log in
          </Link>
        </nav>

        {/* Hero Section */}
        <div className="flex justify-between items-start mb-20">
          <div className="max-w-2xl">
            <h1 className="text-[64px] font-bold leading-tight mb-6">
              Organize your files<br />
              and keep them safe,<br />
              everywhere!
            </h1>
            <p className="text-xl text-gray-700 mb-8 max-w-lg">
              We offer secure storage, ensuring all your data is protected from unauthorized access.
            </p>
            <div className="flex gap-4">
              <button className="px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors">
                Get started
              </button>
              <button className="px-6 py-3 border border-black rounded-lg hover:bg-black hover:text-white transition-colors">
                Request demo
              </button>
            </div>
          </div>
          <div>
            <FolderIcon className="w-[400px] h-[400px] text-black" />
          </div>
        </div>

        {/* Stats Section */}
        <div className="flex gap-6">
          <div className="bg-[#b7bfff] rounded-[32px] p-6 w-[333px]">
            <h3 className="text-xl mb-4">Active users</h3>
            <div className="flex items-center justify-between">
              <span className="text-4xl font-bold">1M+</span>
              <div className="flex -space-x-2">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="w-10 h-10 rounded-full bg-gray-300 border-2 border-white"
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="bg-[#b7bfff] rounded-[32px] p-6 w-[333px]">
            <h3 className="text-xl mb-4">Files stored</h3>
            <div className="flex items-center justify-between">
              <span className="text-4xl font-bold">5TB+</span>
              <FolderIcon className="w-12 h-12 text-gray-700" />
            </div>
          </div>

          <div className="bg-[#b7bfff] rounded-[32px] p-6 w-[333px]">
            <h3 className="text-xl mb-4">Files uploaded</h3>
            <div className="flex items-center justify-between">
              <span className="text-4xl font-bold">6M+</span>
              <div className="w-12 h-12 rounded-full bg-green-400 flex items-center justify-center text-white text-2xl">
                ✓
              </div>
            </div>
          </div>

          {/* Demo Request Button */}
          <div className="flex items-start pt-6">
            <Link
              href="/request-demo"
              className="inline-flex items-center px-6 py-3 border-2 border-black rounded-lg hover:bg-black hover:text-white transition-colors"
            >
              Request free<br />Demo
              <svg
                className="ml-2 w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 8l4 4m0 0l-4 4m4-4H3"
                />
              </svg>
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
