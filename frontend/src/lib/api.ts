/**
 * API Client for SkillBridge Backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface RegisterRequest {
  email: string;
  password: string;
  role: 'student' | 'mentor' | 'company';
  name: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  role: string;
}

export interface GoogleOAuthRequest {
  code: string;
  redirect_uri: string;
  role: 'student' | 'mentor' | 'company' | 'login';
}

export interface ApiError {
  detail: string | { msg: string; type: string }[];
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    console.log('API Request:', { url, method: options.method || 'GET', body: options.body });
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, config);
      
      console.log('API Response:', { status: response.status, ok: response.ok });
      
      if (!response.ok) {
        let errorMessage = 'An error occurred';
        try {
          const errorData: ApiError = await response.json();
          errorMessage = typeof errorData.detail === 'string' 
            ? errorData.detail 
            : JSON.stringify(errorData.detail);
          console.error('API Error Details:', { status: response.status, error: errorData });
        } catch (e) {
          errorMessage = `HTTP ${response.status}: ${response.statusText}`;
          console.error('Failed to parse error response:', e);
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log('API Success:', data);
      return data;
    } catch (error) {
      console.error('Fetch Error:', error);
      throw error;
    }
  }

  async register(data: RegisterRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async login(data: LoginRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async googleOAuth(data: GoogleOAuthRequest): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/google', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    return this.request<AuthResponse>('/auth/refresh', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${refreshToken}`,
      },
    });
  }

  async getCurrentUser(token: string) {
    return this.request('/users/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getStudentProfile(token: string) {
    return this.request('/students/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async uploadResume(token: string, file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseURL}/resumes/upload`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Upload failed');
    }

    return response.json();
  }

  async getMyResumes(token: string) {
    return this.request('/resumes/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getResumeById(token: string, id: string) {
    return this.request(`/resumes/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  // ============================================================
  // RECOMMENDATION ENDPOINTS
  // ============================================================

  async getJobRecommendations(token: string, limit: number = 10) {
    return this.request(`/recommendations/jobs?limit=${limit}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getInternshipRecommendations(token: string, limit: number = 10) {
    return this.request(`/recommendations/internships?limit=${limit}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getMentorRecommendations(token: string, limit: number = 10) {
    return this.request(`/recommendations/mentors?limit=${limit}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getCourseRecommendations(token: string, limit: number = 10, targetSkills?: string[]) {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (targetSkills && targetSkills.length > 0) {
      targetSkills.forEach(skill => params.append('target_skills', skill));
    }
    return this.request(`/recommendations/courses?${params.toString()}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getStudyGroupRecommendations(token: string, limit: number = 10) {
    return this.request(`/recommendations/study-groups?limit=${limit}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  // ============================================================
  // CAREER INTELLIGENCE ENDPOINTS
  // ============================================================

  async getCareerRoles(token: string) {
    return this.request('/career/roles', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async analyzeSkillGap(token: string, roleId: string) {
    return this.request('/career/skill-gap', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ role_id: roleId }),
    });
  }

  async getPlacementReadiness(token: string) {
    return this.request('/career/readiness', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async generateCareerRoadmap(token: string, roleId: string, months: number = 4, jobDescription?: string) {
    const body: any = { role_id: roleId, months };
    if (jobDescription) {
      body.job_description = jobDescription;
    }
    
    return this.request('/career/roadmap', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(body),
    });
  }

  // ============================================================
  // APPLICATION ENDPOINTS
  // ============================================================

  async applyToJob(token: string, jobId: string, coverLetter?: string) {
    return this.request('/applications/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        target_type: 'job',
        target_id: jobId,
        cover_letter: coverLetter,
      }),
    });
  }

  async applyToInternship(token: string, internshipId: string, coverLetter?: string) {
    return this.request('/applications/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        target_type: 'internship',
        target_id: internshipId,
        cover_letter: coverLetter,
      }),
    });
  }

  async getMyApplications(token: string, targetType?: string) {
    const params = targetType ? `?target_type=${targetType}` : '';
    return this.request(`/applications/me${params}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async withdrawApplication(token: string, applicationId: string) {
    return this.request(`/applications/${applicationId}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ status: 'withdrawn' }),
    });
  }

  // ============================================================
  // BOOKMARK ENDPOINTS
  // ============================================================

  async bookmarkItem(token: string, targetType: string, targetId: string) {
    return this.request('/bookmarks/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        target_type: targetType,
        target_id: targetId,
      }),
    });
  }

  async getMyBookmarks(token: string, targetType?: string) {
    const params = targetType ? `?target_type=${targetType}` : '';
    return this.request(`/bookmarks/me${params}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async removeBookmark(token: string, targetType: string, targetId: string) {
    return this.request(`/bookmarks/by-target/${targetType}/${targetId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async checkBookmark(token: string, targetType: string, targetId: string) {
    return this.request(`/bookmarks/check/${targetType}/${targetId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }
}

export const apiClient = new ApiClient();