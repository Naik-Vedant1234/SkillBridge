/**
 * Google OAuth Configuration and Utilities
 */

export const GOOGLE_OAUTH_CONFIG = {
  clientId: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || '',
  redirectUri: process.env.NEXT_PUBLIC_GOOGLE_REDIRECT_URI || 'http://localhost:3000/auth/google/callback',
  scope: 'openid email profile',
  responseType: 'code',
  authEndpoint: 'https://accounts.google.com/o/oauth2/v2/auth',
};

/**
 * Generate Google OAuth authorization URL
 */
export function getGoogleOAuthURL(role: 'student' | 'mentor' | 'company' | 'login' = 'student'): string {
  const params = new URLSearchParams({
    client_id: GOOGLE_OAUTH_CONFIG.clientId,
    redirect_uri: GOOGLE_OAUTH_CONFIG.redirectUri,
    response_type: GOOGLE_OAUTH_CONFIG.responseType,
    scope: GOOGLE_OAUTH_CONFIG.scope,
    state: role, // Pass role in state parameter
    access_type: 'offline',
    prompt: 'consent',
  });

  return `${GOOGLE_OAUTH_CONFIG.authEndpoint}?${params.toString()}`;
}

/**
 * Parse authorization code from URL callback
 */
export function parseGoogleCallback(url: string): { code: string | null; state: string | null; error: string | null } {
  const urlParams = new URLSearchParams(new URL(url).search);
  
  return {
    code: urlParams.get('code'),
    state: urlParams.get('state'),
    error: urlParams.get('error'),
  };
}
