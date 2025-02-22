import { cookies } from 'next/headers';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const loginWithGoogle = () => {
    window.location.href = `${API_URL}/auth/login/google`;
};

export const handleAuthCallback = async (token: string) => {
    try {
        // Store the token in a cookie with proper attributes
        document.cookie = `token=${token}; path=/; max-age=${30 * 24 * 60 * 60}; SameSite=Strict`;
    } catch (error) {
        throw error;
    }
};

export const logout = () => {
    // Remove the token cookie
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT';
    window.location.href = '/';
};

export const getAuthToken = (): string | null => {
    if (typeof window === 'undefined') {
        return null;
    }
    const token = document.cookie.split('; ').find(row => row.startsWith('token='));
    return token ? token.split('=')[1] : null;
};

export const isAuthenticated = (): boolean => {
    return !!getAuthToken();
};

// Function to decode JWT token
export const decodeToken = (token: string): any => {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (e) {
        return null;
    }
};

// Function to get user info from token
export const getUserInfo = async () => {
    const token = getAuthToken();
    if (!token) return null;
    
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch user info');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching user info:', error);
        return null;
    }
};

// Assistant API endpoints
export const processEmails = async (maxEmails: number = 100) => {
    const token = getAuthToken();
    if (!token) return null;
    
    try {
        const response = await fetch(`${API_URL}/assistant/process-emails`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ max_emails: maxEmails })
        });
        
        if (!response.ok) {
            throw new Error('Failed to process emails');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error processing emails:', error);
        return null;
    }
};

export const queryAssistant = async (query: string, timeWindowDays?: number, sourceType?: string) => {
    const token = getAuthToken();
    if (!token) return null;
    
    try {
        const response = await fetch(`${API_URL}/assistant/query`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query,
                time_window_days: timeWindowDays,
                source_type: sourceType
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to query assistant');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error querying assistant:', error);
        return null;
    }
};

export const analyzeWritingStyle = async () => {
    const token = getAuthToken();
    if (!token) return null;
    
    try {
        const response = await fetch(`${API_URL}/assistant/analyze-style`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to analyze writing style');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error analyzing writing style:', error);
        return null;
    }
}; 