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
  const [latestResume, setLatestResume] = useState<any>(null);

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // Fetch latest resume
  useEffect(() => {
    const fetchLatestResume = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) return;

      try {
        const data = await apiClient.getMyResumes(token) as { resumes: any[], total: number };
        // Backend returns { resumes: [...], total: n }
        if (data.resumes && data.resumes.length > 0) {
          setLatestResume(data.resumes[0]); // Most recent resume
        }
      } catch (error) {
        console.error('Failed to fetch resume:', error);
      }
    };

    fetchLatestResume();
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
        <Card className="glass border-border/50 mb-6">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-3">
              <div>
                <p className="text-sm text-muted-foreground">Placement Readiness Score</p>
                <p className="text-4xl font-bold gradient-text mt-1" style={{ fontFamily: "Space Grotesk, sans-serif" }}>72 / 100</p>
              </div>
              <div className="text-right text-sm text-muted-foreground">
                <p>🎯 Target role: Backend Engineer</p>
                <p className="mt-1">📍 3 skills missing</p>
              </div>
            </div>
            <Progress value={72} className="h-2" />
            <p className="text-xs text-muted-foreground mt-2">Add Docker & System Design to reach 85+</p>
          </CardContent>
        </Card>

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
              <DashStat label="Resume Score" value={latestResume?.score?.toString() || "—"} sub={latestResume ? "Upload new" : "Upload resume"} color="gradient-text" />
            </div>
          </Link>
          <DashStat label="Job Matches" value="24" sub="Updated today" color="text-cyan-400" />
          <DashStat label="Internships" value="18" sub="3 new this week" color="text-green-400" />
          <DashStat label="Mentor Matches" value="7" sub="Available now" color="text-amber-400" />
        </div>

        {/* Content grid */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Top job recommendations */}
          <Card className="glass border-border/50 lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                🎯 Top Job Matches
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {["Backend Engineer — Google", "Python Developer — Flipkart", "API Engineer — Razorpay"].map((job, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/3 hover:bg-white/6 transition-colors">
                  <div>
                    <p className="text-sm font-medium">{job}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">📍 Remote • Full-time</p>
                  </div>
                  <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">
                    {88 - i * 4}% match
                  </Badge>
                </div>
              ))}
              <Skeleton className="h-12 rounded-xl opacity-30" />
            </CardContent>
          </Card>

          {/* Skill gap */}
          <Card className="glass border-border/50">
            <CardHeader>
              <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                📊 Skill Gap
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {[
                { skill: "Docker", pct: 0, tag: "Missing" },
                { skill: "System Design", pct: 0, tag: "Missing" },
                { skill: "FastAPI", pct: 75, tag: "In progress" },
                { skill: "PostgreSQL", pct: 90, tag: "Strong" },
              ].map(({ skill, pct, tag }) => (
                <div key={skill}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium">{skill}</span>
                    <Badge
                      className={`text-xs ${
                        tag === "Missing" ? "bg-red-500/15 text-red-400 border-red-500/20"
                        : tag === "In progress" ? "bg-amber-500/15 text-amber-400 border-amber-500/20"
                        : "bg-green-500/15 text-green-400 border-green-500/20"
                      }`}
                    >
                      {tag}
                    </Badge>
                  </div>
                  <Progress value={pct} className="h-1.5" />
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
