"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import { apiClient } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import Link from "next/link";

interface ResumeDetail {
  id: string;
  original_filename: string;
  file_url: string;
  status: string;
  score: number | null;
  uploaded_at: string;
  skills_extracted: string[];
  parsed_data: {
    name?: string;
    email?: string;
    phone?: string;
    skills?: string[];
    education?: Array<{
      degree: string;
      institution: string;
      year: string;
    }>;
    experience?: Array<{
      title: string;
      company: string;
      duration: string;
    }>;
    experience_years?: number;
  };
}

export default function ResumeDetailPage() {
  const { token } = useAuth();
  const router = useRouter();
  const params = useParams();
  const resumeId = params.id as string;

  const [resume, setResume] = useState<ResumeDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) {
      router.push('/login');
      return;
    }
    fetchResumeDetail();
  }, [token, resumeId, router]);

  const fetchResumeDetail = async () => {
    if (!token) return;

    try {
      const data = await apiClient.getResumeById(token, resumeId);
      setResume(data);
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to load resume');
    } finally {
      setIsLoading(false);
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

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Improvement';
  };

  if (!token) return null;

  if (isLoading) {
    return (
      <div className="min-h-screen dot-grid flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading resume...</p>
        </div>
      </div>
    );
  }

  if (error || !resume) {
    return (
      <div className="min-h-screen dot-grid flex items-center justify-center">
        <Card className="glass border-border/50 max-w-md">
          <CardContent className="p-6 text-center">
            <p className="text-red-400 mb-4">{error || 'Resume not found'}</p>
            <Link href="/student/resume">
              <Button variant="outline">Back to Resumes</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
            <Link href="/student/dashboard" className="hover:text-primary">Dashboard</Link>
            <span>/</span>
            <Link href="/student/resume" className="hover:text-primary">Resume</Link>
            <span>/</span>
            <span>Analysis</span>
          </div>
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                Resume Analysis
              </h1>
              <p className="text-muted-foreground mt-1">{resume.original_filename}</p>
            </div>
            <Badge className={getStatusColor(resume.status)}>
              {resume.status}
            </Badge>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Resume Score */}
            {resume.score !== null && (
              <Card className="glass border-border/50">
                <CardHeader>
                  <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                    Resume Score
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className={`text-5xl font-bold ${getScoreColor(resume.score)}`} style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                        {resume.score}
                        <span className="text-2xl text-muted-foreground">/100</span>
                      </div>
                      <p className="text-sm text-muted-foreground mt-1">
                        {getScoreLabel(resume.score)}
                      </p>
                    </div>
                    <div className="text-right text-sm text-muted-foreground">
                      <p>📊 Based on:</p>
                      <p>Skills, Experience & Format</p>
                    </div>
                  </div>
                  <Progress value={resume.score} className="h-2" />
                </CardContent>
              </Card>
            )}

            {/* Extracted Skills */}
            {resume.skills_extracted && resume.skills_extracted.length > 0 && (
              <Card className="glass border-border/50">
                <CardHeader>
                  <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                    Extracted Skills ({resume.skills_extracted.length})
                    {resume.parsed_data?.primary_domain && (
                      <Badge className="ml-2 bg-primary/20 text-primary border-primary/30 text-xs">
                        Primary: {resume.parsed_data.primary_domain}
                      </Badge>
                    )}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {/* Group by categories if available */}
                  {resume.parsed_data?.skill_categories && Object.keys(resume.parsed_data.skill_categories).length > 0 ? (
                    <div className="space-y-4">
                      {Object.entries(resume.parsed_data.skill_categories).map(([category, skills]: [string, any]) => (
                        <div key={category}>
                          <h4 className="text-sm font-medium text-muted-foreground mb-2">
                            {category} ({Array.isArray(skills) ? skills.length : 0})
                          </h4>
                          <div className="flex flex-wrap gap-2">
                            {Array.isArray(skills) && skills.map((skill: string, idx: number) => {
                              const proficiency = resume.parsed_data?.skill_proficiencies?.[skill];
                              const level = proficiency?.level || 'intermediate';
                              const confidence = proficiency?.confidence || 0;
                              
                              const levelColors = {
                                beginner: 'bg-blue-500/15 text-blue-400 border-blue-500/25',
                                intermediate: 'bg-green-500/15 text-green-400 border-green-500/25',
                                advanced: 'bg-purple-500/15 text-purple-400 border-purple-500/25',
                                expert: 'bg-amber-500/15 text-amber-400 border-amber-500/25',
                              };
                              
                              return (
                                <div key={idx} className="relative group">
                                  <Badge
                                    className={`${levelColors[level as keyof typeof levelColors] || 'bg-primary/15 text-primary border-primary/25'} px-3 py-1`}
                                  >
                                    {skill}
                                    {proficiency && (
                                      <span className="ml-1 text-xs opacity-70">
                                        ({level})
                                      </span>
                                    )}
                                  </Badge>
                                  {confidence > 0 && (
                                    <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-black/90 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-10">
                                      Confidence: {(confidence * 100).toFixed(0)}%
                                    </div>
                                  )}
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    // Fallback: show all skills without categories
                    <div className="flex flex-wrap gap-2">
                      {resume.skills_extracted.map((skill, idx) => {
                        const proficiency = resume.parsed_data?.skill_proficiencies?.[skill];
                        const level = proficiency?.level || 'intermediate';
                        const confidence = proficiency?.confidence || 0;
                        
                        const levelColors = {
                          beginner: 'bg-blue-500/15 text-blue-400 border-blue-500/25',
                          intermediate: 'bg-green-500/15 text-green-400 border-green-500/25',
                          advanced: 'bg-purple-500/15 text-purple-400 border-purple-500/25',
                          expert: 'bg-amber-500/15 text-amber-400 border-amber-500/25',
                        };
                        
                        return (
                          <div key={idx} className="relative group">
                            <Badge
                              className={`${levelColors[level as keyof typeof levelColors] || 'bg-primary/15 text-primary border-primary/25'} px-3 py-1`}
                            >
                              {skill}
                              {proficiency && (
                                <span className="ml-1 text-xs opacity-70">
                                  ({level})
                                </span>
                              )}
                            </Badge>
                            {confidence > 0 && (
                              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2 py-1 bg-black/90 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-10">
                                Confidence: {(confidence * 100).toFixed(0)}%
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                  <p className="text-xs text-muted-foreground mt-4">
                    These skills have been automatically added to your profile
                  </p>
                </CardContent>
              </Card>
            )}

            {/* Education */}
            {resume.parsed_data?.education && resume.parsed_data.education.length > 0 && (
              <Card className="glass border-border/50">
                <CardHeader>
                  <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                    Education
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {resume.parsed_data.education.map((edu, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-white/3">
                      <p className="font-medium">{edu.degree}</p>
                      <p className="text-sm text-muted-foreground">{edu.institution}</p>
                      {edu.year && (
                        <p className="text-xs text-muted-foreground mt-1">{edu.year}</p>
                      )}
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Experience */}
            {resume.parsed_data?.experience && resume.parsed_data.experience.length > 0 && (
              <Card className="glass border-border/50">
                <CardHeader>
                  <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                    Experience
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {resume.parsed_data.experience.map((exp, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-white/3">
                      <p className="font-medium">{exp.title}</p>
                      <p className="text-sm text-muted-foreground">{exp.company}</p>
                      {exp.duration && (
                        <p className="text-xs text-muted-foreground mt-1">{exp.duration}</p>
                      )}
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Projects */}
            {resume.parsed_data?.projects && resume.parsed_data.projects.length > 0 && (
              <Card className="glass border-border/50">
                <CardHeader>
                  <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                    Projects ({resume.parsed_data.projects.length})
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {resume.parsed_data.projects.map((project, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-white/3 border border-border/20">
                      <p className="font-medium text-sm">{project.title}</p>
                      {project.description && (
                        <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                          {project.description}
                        </p>
                      )}
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Contact Info */}
            {(resume.parsed_data?.name || resume.parsed_data?.email || resume.parsed_data?.phone) && (
              <Card className="glass border-border/50">
                <CardHeader>
                  <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                    Contact Information
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  {resume.parsed_data.name && (
                    <div>
                      <p className="text-muted-foreground">Name</p>
                      <p className="font-medium">{resume.parsed_data.name}</p>
                    </div>
                  )}
                  {resume.parsed_data.email && (
                    <div>
                      <p className="text-muted-foreground">Email</p>
                      <p className="font-medium">{resume.parsed_data.email}</p>
                    </div>
                  )}
                  {resume.parsed_data.phone && (
                    <div>
                      <p className="text-muted-foreground">Phone</p>
                      <p className="font-medium">{resume.parsed_data.phone}</p>
                    </div>
                  )}
                  {resume.parsed_data.experience_years !== undefined && (
                    <div>
                      <p className="text-muted-foreground">Experience</p>
                      <p className="font-medium">{resume.parsed_data.experience_years} years</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Actions */}
            <Card className="glass border-border/50">
              <CardHeader>
                <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                  Actions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button
                  variant="outline"
                  className="w-full justify-start"
                  onClick={() => window.open(`http://localhost:8000/${resume.file_url}`, '_blank')}
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Download PDF
                </Button>
                
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => router.push('/student/profile')}
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  View Profile
                </Button>

                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => router.push('/student/resume')}
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                  Back to Resumes
                </Button>
              </CardContent>
            </Card>

            {/* Upload Info */}
            <Card className="glass border-border/50">
              <CardHeader>
                <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                  Upload Details
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <div>
                  <p className="text-muted-foreground">Uploaded</p>
                  <p className="font-medium">
                    {new Date(resume.uploaded_at).toLocaleString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
                <div>
                  <p className="text-muted-foreground">Status</p>
                  <p className="font-medium capitalize">{resume.status}</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
