"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuth } from "@/lib/auth-context";
import { apiClient } from "@/lib/api";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useEffect, useState } from "react";
import type { 
  JobRecommendation, 
  PlacementReadinessScore,
  SkillGapAnalysis,
  CareerRole,
  RecommendationsResponse
} from "@/types/career";

// Placeholder stat card
function DashStat({ label, value, sub, color }: { label: string; value: string; sub: string; color: string }) {
  return (
    <Card className="glass border-border/50">
      <CardContent className="p-5">
        <p className="text-xs text-muted-foreground mb-1">{label}</p>
        <p className={`text-3xl font-bold mb-1 ${color}`} style={{ fontFamily: "Space Grotesk, sans-serif" }}>{value}</p>
        <p className="text-xs text-muted-foreground">{sub}</p>
      </CardContent>
    </Card>
  );
}

export default function StudentDashboardPage() {
  const { logout, user } = useAuth();
  const router = useRouter();
  
  // State for various data
  const [latestResume, setLatestResume] = useState<any>(null);
  const [placementReadiness, setPlacementReadiness] = useState<PlacementReadinessScore | null>(null);
  const [jobRecommendations, setJobRecommendations] = useState<JobRecommendation[]>([]);
  const [skillGap, setSkillGap] = useState<SkillGapAnalysis | null>(null);
  const [careerRoles, setCareerRoles] = useState<CareerRole[]>([]);
  const [loading, setLoading] = useState(true);
  const [statsLoading, setStatsLoading] = useState(true);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // Fetch all dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        // Fetch latest resume
        try {
          const resumeData = await apiClient.getMyResumes(token) as { resumes: any[], total: number };
          if (resumeData.resumes && resumeData.resumes.length > 0) {
            setLatestResume(resumeData.resumes[0]);
          }
        } catch (error) {
          console.error('Failed to fetch resume:', error);
        }

        // Fetch placement readiness
        try {
          const readinessData = await apiClient.getPlacementReadiness(token) as PlacementReadinessScore;
          console.log('Placement readiness data:', readinessData);
          setPlacementReadiness(readinessData);
        } catch (error) {
          console.error('Failed to fetch placement readiness:', error);
        }

        // Fetch career roles first
        try {
          const rolesData = await apiClient.getCareerRoles(token) as { roles: CareerRole[], total: number };
          console.log('Career roles data:', rolesData);
          setCareerRoles(rolesData.roles);

          // If we have roles, fetch skill gap for first role
          if (rolesData.roles.length > 0) {
            try {
              const gapData = await apiClient.analyzeSkillGap(token, rolesData.roles[0].id) as SkillGapAnalysis;
              console.log('Skill gap data:', gapData);
              setSkillGap(gapData);
            } catch (error) {
              console.error('Failed to fetch skill gap:', error);
            }
          }
        } catch (error) {
          console.error('Failed to fetch career roles:', error);
        }

        // Fetch job recommendations
        try {
          const jobsData = await apiClient.getJobRecommendations(token, 3) as RecommendationsResponse<JobRecommendation>;
          console.log('Job recommendations data:', jobsData);
          setJobRecommendations(jobsData.recommendations);
        } catch (error) {
          console.error('Failed to fetch job recommendations:', error);
        }

        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  // Fetch stats for cards
  useEffect(() => {
    const fetchStats = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) {
        setStatsLoading(false);
        return;
      }

      try {
        // These are just for displaying counts, can be fetched in background
        setStatsLoading(false);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
        setStatsLoading(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      {/* Header */}
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
              Good morning 👋
            </h1>
            <p className="text-muted-foreground mt-1">Here&apos;s your career snapshot for today.</p>
          </div>
          <div className="flex items-center gap-3">
            <Badge className="bg-primary/15 text-primary border-primary/25 px-3 py-1">
              {user?.role || 'Student'}
            </Badge>
            <Link href="/student/profile">
              <Button 
                variant="outline"
                className="border-border/60 hover:border-primary/40 hover:bg-primary/5"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Profile
              </Button>
            </Link>
            <Button 
              variant="outline" 
              onClick={handleLogout}
              className="border-border/60 hover:border-red-500/40 hover:bg-red-500/5 hover:text-red-500"
            >
              Logout
            </Button>
          </div>
        </div>

        {/* Placement readiness */}
        {loading ? (
          <Skeleton className="h-32 rounded-xl mb-6" />
        ) : placementReadiness ? (
          <Card className="glass border-border/50 mb-6">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <p className="text-sm text-muted-foreground">Placement Readiness Score</p>
                  <p className="text-4xl font-bold gradient-text mt-1" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                    {placementReadiness.overall_score} / 100
                  </p>
                </div>
                <div className="text-right">
                  <Link href="/student/roadmap">
                    <Button className="mb-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0">
                      🗺️ View Career Roadmap
                    </Button>
                  </Link>
                  <div className="text-sm text-muted-foreground">
                    <p>🎯 Status: {placementReadiness.readiness_level}</p>
                    {skillGap && (
                      <p className="mt-1">📍 {skillGap.analysis.skills_missing} skills missing</p>
                    )}
                  </div>
                </div>
              </div>
              <Progress value={placementReadiness.overall_score} className="h-2" />
              <p className="text-xs text-muted-foreground mt-2">{placementReadiness.message}</p>
            </CardContent>
          </Card>
        ) : (
          <Card className="glass border-border/50 mb-6">
            <CardContent className="p-6">
              <p className="text-sm text-muted-foreground">Loading placement readiness...</p>
            </CardContent>
          </Card>
        )}

        {/* Resume Score Widget */}
        {latestResume && latestResume.score !== null && (
          <Card className="glass border-border/50 mb-6">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="text-sm text-muted-foreground mb-1">Resume Score</p>
                  <div className="flex items-baseline gap-2">
                    <p className="text-3xl font-bold gradient-text" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                      {latestResume.score}
                      <span className="text-lg text-muted-foreground">/100</span>
                    </p>
                    <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">
                      {latestResume.skills_extracted?.length || 0} skills extracted
                    </Badge>
                  </div>
                </div>
                <Link href={`/student/resume/${latestResume.id}`}>
                  <Button size="sm" variant="outline">
                    View Analysis
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Stats row */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <Link href="/student/resume">
            <div className="cursor-pointer hover:scale-105 transition-transform">
              <DashStat 
                label="Resume Score" 
                value={latestResume?.score?.toString() || "—"} 
                sub={latestResume ? "Upload new" : "Upload resume"} 
                color="gradient-text" 
              />
            </div>
          </Link>
          <DashStat 
            label="Skill Coverage" 
            value={skillGap ? `${skillGap.analysis.coverage_percentage}%` : "—"} 
            sub={skillGap ? `${skillGap.analysis.skills_matched} skills matched` : "Analyzing..."} 
            color="text-cyan-400" 
          />
          <DashStat 
            label="Readiness" 
            value={placementReadiness ? `${placementReadiness.overall_score}` : "—"} 
            sub={placementReadiness?.readiness_level || "Loading..."} 
            color="text-green-400" 
          />
          <DashStat 
            label="Job Matches" 
            value={jobRecommendations.length.toString()} 
            sub="Personalized for you" 
            color="text-amber-400" 
          />
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-6">
          <Link href="/student/jobs">
            <Card className="glass border-border/50 hover:border-primary/40 transition-all cursor-pointer hover:scale-105">
              <CardContent className="p-4 text-center">
                <div className="text-2xl mb-1">💼</div>
                <p className="text-sm font-medium">Jobs</p>
              </CardContent>
            </Card>
          </Link>
          <Link href="/student/internships">
            <Card className="glass border-border/50 hover:border-primary/40 transition-all cursor-pointer hover:scale-105">
              <CardContent className="p-4 text-center">
                <div className="text-2xl mb-1">🎓</div>
                <p className="text-sm font-medium">Internships</p>
              </CardContent>
            </Card>
          </Link>
          <Link href="/student/mentors">
            <Card className="glass border-border/50 hover:border-primary/40 transition-all cursor-pointer hover:scale-105">
              <CardContent className="p-4 text-center">
                <div className="text-2xl mb-1">👨‍🏫</div>
                <p className="text-sm font-medium">Mentors</p>
              </CardContent>
            </Card>
          </Link>
          <Link href="/student/courses">
            <Card className="glass border-border/50 hover:border-primary/40 transition-all cursor-pointer hover:scale-105">
              <CardContent className="p-4 text-center">
                <div className="text-2xl mb-1">📚</div>
                <p className="text-sm font-medium">Courses</p>
              </CardContent>
            </Card>
          </Link>
          <Link href="/student/study-groups">
            <Card className="glass border-border/50 hover:border-primary/40 transition-all cursor-pointer hover:scale-105">
              <CardContent className="p-4 text-center">
                <div className="text-2xl mb-1">👥</div>
                <p className="text-sm font-medium">Study Groups</p>
              </CardContent>
            </Card>
          </Link>
        </div>

        {/* Content grid */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Top job recommendations */}
          <Card className="glass border-border/50 lg:col-span-2">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                  🎯 Top Job Matches
                </CardTitle>
                <Link href="/student/jobs">
                  <Button variant="ghost" size="sm" className="text-xs">
                    View All →
                  </Button>
                </Link>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              {loading ? (
                <>
                  <Skeleton className="h-16 rounded-xl" />
                  <Skeleton className="h-16 rounded-xl" />
                  <Skeleton className="h-16 rounded-xl" />
                </>
              ) : jobRecommendations.length > 0 ? (
                jobRecommendations.map((job) => (
                  <div key={job.id} className="flex items-center justify-between p-3 rounded-xl bg-white/3 hover:bg-white/6 transition-colors">
                    <div className="flex-1">
                      <p className="text-sm font-medium">{job.title}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        📍 {job.location} • {job.is_remote ? 'Remote' : 'On-site'}
                      </p>
                      {job.salary_range && (
                        <p className="text-xs text-muted-foreground mt-0.5">💰 {job.salary_range}</p>
                      )}
                    </div>
                    <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">
                      {job.match_percentage}% match
                    </Badge>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <p className="text-sm">No job recommendations yet</p>
                  <p className="text-xs mt-2">Complete your profile to get personalized matches</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Skill gap */}
          <Card className="glass border-border/50">
            <CardHeader>
              <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                📊 Skill Gap Analysis
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {loading ? (
                <>
                  <Skeleton className="h-10 rounded" />
                  <Skeleton className="h-10 rounded" />
                  <Skeleton className="h-10 rounded" />
                </>
              ) : skillGap && skillGap.missing_skills.length > 0 ? (
                <>
                  {skillGap.missing_skills.slice(0, 4).map((skill) => (
                    <div key={skill.name}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-medium">{skill.name}</span>
                        <Badge
                          className={`text-xs ${
                            skill.importance === "essential" 
                              ? "bg-red-500/15 text-red-400 border-red-500/20"
                              : skill.importance === "important"
                              ? "bg-amber-500/15 text-amber-400 border-amber-500/20"
                              : "bg-blue-500/15 text-blue-400 border-blue-500/20"
                          }`}
                        >
                          {skill.importance}
                        </Badge>
                      </div>
                      <Progress value={0} className="h-1.5" />
                    </div>
                  ))}
                  {skillGap.matched_skills.length > 0 && (
                    <div className="pt-2 border-t border-border/50">
                      <p className="text-xs text-muted-foreground mb-2">✅ Skills you have:</p>
                      <div className="flex flex-wrap gap-1">
                        {skillGap.matched_skills.slice(0, 3).map((skill) => (
                          <Badge key={skill.name} className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">
                            {skill.name}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-center py-6 text-muted-foreground">
                  <p className="text-xs">Add skills to see your gap analysis</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
