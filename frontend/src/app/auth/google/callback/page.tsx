"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { apiClient } from "@/lib/api";
import { parseGoogleCallback, GOOGLE_OAUTH_CONFIG } from "@/lib/google-oauth";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export default function GoogleCallbackPage() {
  const [error, setError] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const searchParams = useSearchParams();
  const { login } = useAuth();
  const hasFetched = React.useRef(false);

  useEffect(() => {
    const handleCallback = async () => {
      try {
        if (hasFetched.current) return;
        
        // Get code and state from URL
        const code = searchParams.get('code');
        const state = searchParams.get('state'); // role passed in state
        const errorParam = searchParams.get('error');

        if (errorParam) {
          setError(`Google OAuth error: ${errorParam}`);
          setIsLoading(false);
          return;
        }

        if (!code) {
          setError('No authorization code received from Google');
          setIsLoading(false);
          return;
        }

        hasFetched.current = true;
        const role = (state as 'student' | 'mentor' | 'company') || 'student';

        console.log('Google OAuth callback:', { code, role });

        // Exchange code for tokens
        const authData = await apiClient.googleOAuth({
          code,
          redirect_uri: GOOGLE_OAUTH_CONFIG.redirectUri,
          role,
        });

        console.log('Google OAuth successful:', authData);

        // Store tokens and user data
        login(authData);

        // Redirect based on role
        switch (authData.role) {
          case 'student':
            router.push('/student/dashboard');
            break;
          case 'mentor':
            router.push('/mentor/dashboard');
            break;
          case 'company':
            router.push('/company/dashboard');
            break;
          default:
            router.push('/');
        }
      } catch (err) {
        console.error('Google OAuth error:', err);
        setError(err instanceof Error ? err.message : 'Authentication failed');
        setIsLoading(false);
        hasFetched.current = false; // Reset on error so user can retry if needed
      }
    };

    handleCallback();
  }, [searchParams, login, router]);

  return (
    <div className="min-h-screen dot-grid flex items-center justify-center p-6">
      <Card className="glass border-border/50 w-full max-w-md">
        <CardHeader className="pb-4">
          <h1 className="text-2xl font-bold text-center">
            {isLoading ? 'Authenticating...' : 'Authentication Failed'}
          </h1>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              <div className="h-2 bg-primary/20 rounded-full overflow-hidden">
                <div className="h-full bg-primary/60 rounded-full animate-pulse w-3/4"></div>
              </div>
              <p className="text-sm text-muted-foreground text-center">
                Completing sign in with Google...
              </p>
            </div>
          ) : error ? (
            <div className="space-y-4">
              <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                {error}
              </div>
              <a
                href="/login"
                className="block w-full text-center py-2 px-4 bg-primary text-white rounded-md hover:bg-primary/90 transition-colors"
              >
                Back to Login
              </a>
            </div>
          ) : null}
        </CardContent>
      </Card>
    </div>
  );
}
