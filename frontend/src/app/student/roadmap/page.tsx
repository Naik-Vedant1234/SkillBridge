"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuth } from "@/lib/auth-context";
import { apiClient } from "@/lib/api";
import Link from "next/link";
import { useEffect, useState } from "react";
import type { CareerRoadmap, CareerRole } from "@/types/career";

export default function CareerRoadmapPage() {
  const { user } = useAuth();
  const [roadmap, setRoadmap] = useState<CareerRoadmap | null>(null);
  const [careerRoles, setCareerRoles] = useState<CareerRole[]>([]);
  const [selectedRole, setSelectedRole] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [months, setMonths] = useState(4);
  const [customMonths, setCustomMonths] = useState<string>('');
  const [useCustomTimeline, setUseCustomTimeline] = useState(false);
  const [jobDescription, setJobDescription] = useState<string>('');
  const [showJobInput, setShowJobInput] = useState(false);

  // Fetch career roles on mount
  useEffect(() => {
    const fetchRoles = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) return;

      try {
        const data = await apiClient.getCareerRoles(token) as { roles: CareerRole[], total: number };
        setCareerRoles(data.roles);
        if (data.roles.length > 0) {
          setSelectedRole(data.roles[0].id);
          // Auto-generate roadmap for first role
          generateRoadmap(data.roles[0].id, 4);
        }
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch roles:', error);
        setLoading(false);
      }
    };

    fetchRoles();
  }, []);

  const generateRoadmap = async (roleId: string, timelineMonths: number, jobDesc?: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setGenerating(true);
    try {
      const data = await apiClient.generateCareerRoadmap(
        token, 
        roleId, 
        timelineMonths,
        jobDesc
      ) as CareerRoadmap;
      console.log('Roadmap data:', data);
      setRoadmap(data);
    } catch (error) {
      console.error('Failed to generate roadmap:', error);
    } finally {
      setGenerating(false);
    }
  };

  const handleRoleChange = (roleId: string) => {
    setSelectedRole(roleId);
    generateRoadmap(roleId, months);
  };

  const handleMonthsChange = (newMonths: number) => {
    setMonths(newMonths);
    setUseCustomTimeline(false);
    setCustomMonths('');
    if (selectedRole) {
      generateRoadmap(selectedRole, newMonths);
    }
  };

  const handleCustomMonthsApply = () => {
    const monthsValue = parseInt(customMonths);
    if (monthsValue > 0 && monthsValue <= 36 && selectedRole) {
      setMonths(monthsValue);
      generateRoadmap(selectedRole, monthsValue);
    }
  };

  const handleGenerateWithJobDesc = () => {
    if (selectedRole && jobDescription.trim()) {
      generateRoadmap(selectedRole, months, jobDescription.trim());
    }
  };

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                🗺️ Career Roadmap
              </h1>
              <p className="text-muted-foreground mt-1">Your personalized learning path powered by AI</p>
            </div>
            <Link href="/student/dashboard">
              <Button variant="outline">
                ← Back to Dashboard
              </Button>
            </Link>
          </div>

          {/* Controls */}
          <div className="space-y-4">
            <div className="flex flex-wrap gap-4">
              {/* Role Selector */}
              <Card className="glass border-border/50 flex-1 min-w-[300px]">
                <CardContent className="p-4">
                  <label className="text-xs text-muted-foreground mb-2 block">Target Career Role</label>
                  <select 
                    value={selectedRole || ''}
                    onChange={(e) => handleRoleChange(e.target.value)}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                    disabled={loading}
                  >
                    {careerRoles.map((role) => (
                      <option key={role.id} value={role.id}>
                        {role.title} - {role.domain}
                      </option>
                    ))}
                  </select>
                </CardContent>
              </Card>

              {/* Timeline Selector */}
              <Card className="glass border-border/50 w-[280px]">
                <CardContent className="p-4">
                  <label className="text-xs text-muted-foreground mb-2 block">Timeline</label>
                  <div className="space-y-2">
                    <select 
                      value={useCustomTimeline ? 'custom' : months}
                      onChange={(e) => {
                        if (e.target.value === 'custom') {
                          setUseCustomTimeline(true);
                        } else {
                          handleMonthsChange(Number(e.target.value));
                        }
                      }}
                      className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                      disabled={generating}
                    >
                      <option value={3}>3 months</option>
                      <option value={4}>4 months</option>
                      <option value={6}>6 months</option>
                      <option value={12}>12 months</option>
                      <option value="custom">Custom...</option>
                    </select>
                    
                    {useCustomTimeline && (
                      <div className="flex gap-2">
                        <input
                          type="number"
                          min="1"
                          max="36"
                          value={customMonths}
                          onChange={(e) => setCustomMonths(e.target.value)}
                          placeholder="Enter months (1-36)"
                          className="flex-1 bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                        />
                        <Button 
                          size="sm" 
                          onClick={handleCustomMonthsApply}
                          disabled={!customMonths || generating}
                          className="bg-primary/20 hover:bg-primary/30"
                        >
                          Apply
                        </Button>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Job Description Toggle */}
              <Card className="glass border-border/50 w-[200px]">
                <CardContent className="p-4">
                  <label className="text-xs text-muted-foreground mb-2 block">Options</label>
                  <Button 
                    variant="outline"
                    className="w-full text-xs"
                    onClick={() => setShowJobInput(!showJobInput)}
                  >
                    {showJobInput ? '📋 Hide Job Details' : '📋 Paste Job Description'}
                  </Button>
                </CardContent>
              </Card>
            </div>

            {/* Job Description Input */}
            {showJobInput && (
              <Card className="glass border-border/50">
                <CardContent className="p-4">
                  <label className="text-xs text-muted-foreground mb-2 block">
                    Job Description (Optional - Helps personalize your roadmap)
                  </label>
                  <textarea
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    placeholder="Paste the job description here to get a roadmap tailored to specific job requirements..."
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm min-h-[120px] resize-y"
                    disabled={generating}
                  />
                  <div className="flex items-center justify-between mt-3">
                    <p className="text-xs text-muted-foreground">
                      {jobDescription.length > 0 ? `${jobDescription.length} characters` : 'AI will analyze requirements and skills needed'}
                    </p>
                    <div className="flex gap-2">
                      <Button 
                        size="sm"
                        variant="outline"
                        onClick={() => {
                          setJobDescription('');
                          setShowJobInput(false);
                        }}
                      >
                        Clear
                      </Button>
                      <Button 
                        size="sm"
                        onClick={handleGenerateWithJobDesc}
                        disabled={!jobDescription.trim() || generating}
                        className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0"
                      >
                        {generating ? 'Generating...' : 'Generate Roadmap'}
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Roadmap Overview */}
        {loading || generating ? (
          <div className="space-y-4">
            <Skeleton className="h-32 rounded-xl" />
            <Skeleton className="h-64 rounded-xl" />
          </div>
        ) : roadmap ? (
          <>
            {/* Stats Card */}
            <Card className="glass border-border/50 mb-6">
              <CardContent className="p-6">
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  <div>
                    <p className="text-xs text-muted-foreground mb-1">Target Role</p>
                    <p className="text-lg font-bold">{roadmap.role.title}</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground mb-1">Timeline</p>
                    <p className="text-lg font-bold">{roadmap.timeline_months} months</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground mb-1">Current Coverage</p>
                    <p className="text-lg font-bold gradient-text">{roadmap.skill_coverage}%</p>
                  </div>
                  <div>
                    <p className="text-xs text-muted-foreground mb-1">Milestones</p>
                    <p className="text-lg font-bold">{roadmap.roadmap.length} months</p>
                  </div>
                </div>
                <Progress value={roadmap.skill_coverage} className="h-2 mt-4" />
              </CardContent>
            </Card>

            {/* Monthly Milestones */}
            <div className="space-y-6">
              {roadmap.roadmap.map((milestone, index) => (
                <Card key={milestone.month} className="glass border-border/50 overflow-hidden">
                  {/* Month Header */}
                  <div className={`h-2 ${
                    index === 0 ? 'bg-green-500' : 
                    index < roadmap.roadmap.length / 2 ? 'bg-blue-500' : 
                    'bg-purple-500'
                  }`} />
                  
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="text-lg" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                          {milestone.title}
                        </CardTitle>
                        <p className="text-sm text-muted-foreground mt-1">{milestone.focus}</p>
                      </div>
                      <Badge className="bg-primary/15 text-primary border-primary/25">
                        Month {milestone.month}
                      </Badge>
                    </div>
                  </CardHeader>

                  <CardContent className="space-y-4">
                    {/* Skills to Learn */}
                    {milestone.skills_to_learn.length > 0 && (
                      <div>
                        <p className="text-xs font-medium text-muted-foreground mb-2">📚 Skills to Learn</p>
                        <div className="flex flex-wrap gap-2">
                          {milestone.skills_to_learn.map((skill) => (
                            <Badge key={skill} className="bg-blue-500/15 text-blue-400 border-blue-500/20">
                              {skill}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Tasks */}
                    {milestone.tasks.length > 0 && (
                      <div>
                        <p className="text-xs font-medium text-muted-foreground mb-2">✅ Tasks</p>
                        <ul className="space-y-2">
                          {milestone.tasks.map((task, taskIndex) => (
                            <li key={taskIndex} className="flex items-start gap-2 text-sm">
                              <span className="text-muted-foreground mt-0.5">•</span>
                              <span>{task}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Projects */}
                    {milestone.projects.length > 0 && (
                      <div>
                        <p className="text-xs font-medium text-muted-foreground mb-2">🚀 Projects</p>
                        <div className="space-y-2">
                          {milestone.projects.map((project) => (
                            <div key={project} className="p-3 rounded-lg bg-white/3 border border-border/30">
                              <p className="text-sm font-medium">{project}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* AI Insights */}
                    {milestone.ai_insights && (
                      <div className="mt-4 p-4 rounded-lg bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/20">
                        <p className="text-xs font-medium text-purple-400 mb-2">🤖 AI Insights</p>
                        <p className="text-sm text-muted-foreground">{milestone.ai_insights}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Resources Section */}
            <div className="grid md:grid-cols-2 gap-6 mt-8">
              {/* Suggested Projects */}
              {roadmap.resources.projects.length > 0 && (
                <Card className="glass border-border/50">
                  <CardHeader>
                    <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                      🎯 Suggested Projects
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {roadmap.resources.projects.map((project, index) => (
                      <div key={index} className="p-3 rounded-lg bg-white/3 hover:bg-white/6 transition-colors">
                        <div className="flex items-center justify-between mb-1">
                          <p className="text-sm font-medium">{project.title}</p>
                          <Badge className={`text-xs ${
                            project.difficulty === 'beginner' ? 'bg-green-500/15 text-green-400 border-green-500/20' :
                            project.difficulty === 'intermediate' ? 'bg-amber-500/15 text-amber-400 border-amber-500/20' :
                            'bg-red-500/15 text-red-400 border-red-500/20'
                          }`}>
                            {project.difficulty}
                          </Badge>
                        </div>
                        <p className="text-xs text-muted-foreground">{project.description}</p>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              )}

              {/* Recommended Certifications */}
              {roadmap.resources.certifications.length > 0 && (
                <Card className="glass border-border/50">
                  <CardHeader>
                    <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                      🏆 Recommended Certifications
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {roadmap.resources.certifications.map((cert, index) => (
                      <div key={index} className="p-3 rounded-lg bg-white/3 hover:bg-white/6 transition-colors">
                        <p className="text-sm font-medium">{cert.name}</p>
                        <p className="text-xs text-muted-foreground mt-1">Provider: {cert.provider}</p>
                      </div>
                    ))}
                  </CardContent>
                </Card>
              )}
            </div>
          </>
        ) : (
          <Card className="glass border-border/50">
            <CardContent className="p-12 text-center">
              <p className="text-muted-foreground">Select a career role to generate your personalized roadmap</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
