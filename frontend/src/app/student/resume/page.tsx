"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { apiClient } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

interface Resume {
  id: string;
  original_filename: string;
  status: string;
  score: number | null;
  uploaded_at: string;
  skills_extracted: string[];
}

export default function ResumePage() {
  const { token, user } = useAuth();
  const router = useRouter();
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!token) {
      router.push('/login');
      return;
    }
    fetchResumes();
  }, [token, router]);

  const fetchResumes = async () => {
    if (!token) return;
    
    try {
      const data = await apiClient.getMyResumes(token);
      // Backend returns { resumes: [...], total: n }
      setResumes(data.resumes || []);
    } catch (error) {
      console.error('Failed to fetch resumes:', error);
      setResumes([]); // Set empty array on error
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !token) return;

    // Validate file
    if (file.type !== 'application/pdf') {
      setUploadError('Please upload a PDF file');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setUploadError('File size must be less than 10MB');
      return;
    }

    setIsUploading(true);
    setUploadError("");

    try {
      await apiClient.uploadResume(token, file);
      // Wait briefly for processing, then refresh
      setTimeout(async () => {
        await fetchResumes();
        setIsUploading(false);
      }, 1000);
      setUploadError("");
    } catch (error) {
      setUploadError(error instanceof Error ? error.message : 'Upload failed');
      setIsUploading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'parsed':
        return 'bg-green-500/15 text-green-400 border-green-500/20';
      case 'processing':
        return 'bg-yellow-500/15 text-yellow-400 border-yellow-500/20';
      case 'failed':
        return 'bg-red-500/15 text-red-400 border-red-500/20';
      default:
        return 'bg-blue-500/15 text-blue-400 border-blue-500/20';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (!token) return null;

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
            <Link href="/student/dashboard" className="hover:text-primary">Dashboard</Link>
            <span>/</span>
            <span>Resume</span>
          </div>
          <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
            My Resumes 📄
          </h1>
          <p className="text-muted-foreground mt-1">
            Upload your resume for AI-powered analysis and profile building
          </p>
        </div>

        {/* Upload Section */}
        <Card className="glass border-border/50 mb-6">
          <CardHeader>
            <CardTitle className="text-lg" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
              Upload New Resume
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {uploadError && (
                <div className="p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-md">
                  {uploadError}
                </div>
              )}

              <div className="border-2 border-dashed border-border/50 rounded-xl p-8 text-center hover:border-primary/40 transition-colors">
                <input
                  type="file"
                  id="resume-upload"
                  accept=".pdf"
                  onChange={handleFileUpload}
                  disabled={isUploading}
                  className="hidden"
                />
                <label
                  htmlFor="resume-upload"
                  className="cursor-pointer flex flex-col items-center gap-3"
                >
                  <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                    <svg
                      className="w-8 h-8 text-primary"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                      />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm font-medium">
                      {isUploading ? 'Uploading...' : 'Click to upload or drag and drop'}
                    </p>
                    <p className="text-xs text-muted-foreground mt-1">
                      PDF only, max 10MB
                    </p>
                  </div>
                </label>
              </div>

              <div className="text-xs text-muted-foreground space-y-1">
                <p>✓ AI will extract your skills, experience, and education</p>
                <p>✓ Your profile will be automatically updated</p>
                <p>✓ Get a resume score and improvement suggestions</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Resumes List */}
        <Card className="glass border-border/50">
          <CardHeader>
            <CardTitle className="text-lg" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
              Your Resumes ({resumes.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="text-center py-8 text-muted-foreground">
                Loading resumes...
              </div>
            ) : resumes.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <p>No resumes uploaded yet</p>
                <p className="text-sm mt-1">Upload your first resume to get started</p>
              </div>
            ) : (
              <div className="space-y-3">
                {resumes.map((resume) => (
                  <Link
                    key={resume.id}
                    href={`/student/resume/${resume.id}`}
                    className="block p-4 rounded-xl bg-white/3 hover:bg-white/6 transition-colors border border-border/30"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-medium truncate">
                            {resume.original_filename}
                          </h3>
                          <Badge className={`text-xs ${getStatusColor(resume.status)}`}>
                            {resume.status}
                          </Badge>
                        </div>
                        
                        <div className="flex items-center gap-4 text-xs text-muted-foreground">
                          <span>📅 {formatDate(resume.uploaded_at)}</span>
                          {resume.score !== null && (
                            <span>⭐ Score: {resume.score}/100</span>
                          )}
                          {resume.skills_extracted && resume.skills_extracted.length > 0 && (
                            <span>🎯 {resume.skills_extracted.length} skills</span>
                          )}
                        </div>

                        {resume.skills_extracted && resume.skills_extracted.length > 0 && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {resume.skills_extracted.slice(0, 5).map((skill, idx) => (
                              <Badge
                                key={idx}
                                className="bg-primary/10 text-primary border-primary/20 text-xs"
                              >
                                {skill}
                              </Badge>
                            ))}
                            {resume.skills_extracted.length > 5 && (
                              <Badge className="bg-muted text-muted-foreground text-xs">
                                +{resume.skills_extracted.length - 5} more
                              </Badge>
                            )}
                          </div>
                        )}
                      </div>

                      <svg
                        className="w-5 h-5 text-muted-foreground flex-shrink-0"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 5l7 7-7 7"
                        />
                      </svg>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
