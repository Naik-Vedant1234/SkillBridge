"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Pagination } from "@/components/ui/pagination";
import { useAuth } from "@/lib/auth-context";
import { apiClient } from "@/lib/api";
import { useToast } from "@/components/ui/toast";
import { useFilterPreferences } from "@/hooks/useFilterPreferences";
import Link from "next/link";
import { useEffect, useState } from "react";
import type { JobRecommendation, RecommendationsResponse } from "@/types/career";

const ITEMS_PER_PAGE = 12;

export default function JobsPage() {
  const { user } = useAuth();
  const { addToast } = useToast();
  const [jobs, setJobs] = useState<JobRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [applyingTo, setApplyingTo] = useState<string | null>(null);
  const [savedJobs, setSavedJobs] = useState<Set<string>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  
  const { filters, updateFilters, resetFilters, isLoaded } = useFilterPreferences({
    key: 'jobs',
    defaultFilters: {
      search: "",
      location: "all",
      remote: "all",
      minMatch: 0,
    },
  });

  useEffect(() => {
    fetchJobs();
    loadSavedJobs();
  }, []);

  const fetchJobs = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setLoading(true);
    try {
      const data = await apiClient.getJobRecommendations(token, 50) as RecommendationsResponse<JobRecommendation>;
      setJobs(data.recommendations);
    } catch (error) {
      console.error('Failed to fetch jobs:', error);
      addToast('Failed to load jobs', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadSavedJobs = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
      const data = await apiClient.getMyBookmarks(token, 'job') as any;
      const saved = new Set(data.bookmarks.map((b: any) => b.target_id));
      setSavedJobs(saved);
    } catch (error) {
      console.error('Failed to load saved jobs:', error);
    }
  };

  const handleApply = async (jobId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setApplyingTo(jobId);
    try {
      await apiClient.applyToJob(token, jobId);
      addToast('Application submitted successfully!', 'success');
    } catch (error: any) {
      const message = error.message || 'Failed to apply';
      addToast(message, 'error');
    } finally {
      setApplyingTo(null);
    }
  };

  const handleSave = async (jobId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    try {
      if (savedJobs.has(jobId)) {
        await apiClient.removeBookmark(token, 'job', jobId);
        setSavedJobs(prev => {
          const newSet = new Set(prev);
          newSet.delete(jobId);
          return newSet;
        });
        addToast('Job removed from saved', 'info');
      } else {
        await apiClient.bookmarkItem(token, 'job', jobId);
        setSavedJobs(prev => new Set(prev).add(jobId));
        addToast('Job saved successfully!', 'success');
      }
    } catch (error: any) {
      const message = error.message || 'Failed to save';
      addToast(message, 'error');
    }
  };

  // Reset to page 1 when filters change
  useEffect(() => {
    if (isLoaded) {
      setCurrentPage(1);
    }
  }, [filters, isLoaded]);

  // Filter jobs based on current filters
  const filteredJobs = jobs.filter(job => {
    // Search filter
    if (filters.search && !job.title.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    
    // Location filter
    if (filters.location !== "all") {
      if (filters.location === "remote" && !job.is_remote) return false;
      if (filters.location === "onsite" && job.is_remote) return false;
    }
    
    // Remote filter
    if (filters.remote !== "all") {
      if (filters.remote === "yes" && !job.is_remote) return false;
      if (filters.remote === "no" && job.is_remote) return false;
    }
    
    // Match percentage filter
    if (job.match_percentage < filters.minMatch) return false;
    
    return true;
  });

  // Pagination calculations
  const totalPages = Math.ceil(filteredJobs.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const paginatedJobs = filteredJobs.slice(startIndex, endIndex);

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                💼 Job Recommendations
              </h1>
              <p className="text-muted-foreground mt-1">
                {filteredJobs.length} personalized matches found
              </p>
            </div>
            <Link href="/student/dashboard">
              <Button variant="outline">
                ← Back to Dashboard
              </Button>
            </Link>
          </div>

          {/* Filters */}
          <Card className="glass border-border/50">
            <CardContent className="p-4">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Search */}
                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Search</label>
                  <input
                    type="text"
                    placeholder="Job title..."
                    value={filters.search}
                    onChange={(e) => updateFilters({ search: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  />
                </div>

                {/* Location Type */}
                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Work Location</label>
                  <select
                    value={filters.location}
                    onChange={(e) => updateFilters({ location: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Locations</option>
                    <option value="remote">Remote Only</option>
                    <option value="onsite">On-site Only</option>
                  </select>
                </div>

                {/* Remote Filter */}
                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Remote Work</label>
                  <select
                    value={filters.remote}
                    onChange={(e) => updateFilters({ remote: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Options</option>
                    <option value="yes">Remote Available</option>
                    <option value="no">No Remote</option>
                  </select>
                </div>

                {/* Min Match */}
                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">
                    Min Match: {filters.minMatch}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="10"
                    value={filters.minMatch}
                    onChange={(e) => updateFilters({ minMatch: parseInt(e.target.value) })}
                    className="w-full"
                  />
                </div>
              </div>

              {/* Active Filters Summary */}
              {(filters.search || filters.location !== "all" || filters.remote !== "all" || filters.minMatch > 0) && (
                <div className="mt-4 flex items-center gap-2 flex-wrap">
                  <span className="text-xs text-muted-foreground">Active filters:</span>
                  {filters.search && (
                    <Badge className="bg-blue-500/15 text-blue-400 border-blue-500/20">
                      Search: {filters.search}
                    </Badge>
                  )}
                  {filters.location !== "all" && (
                    <Badge className="bg-green-500/15 text-green-400 border-green-500/20">
                      Location: {filters.location}
                    </Badge>
                  )}
                  {filters.minMatch > 0 && (
                    <Badge className="bg-purple-500/15 text-purple-400 border-purple-500/20">
                      Match ≥ {filters.minMatch}%
                    </Badge>
                  )}
                  <Button
                    size="sm"
                    variant="ghost"
                    onClick={resetFilters}
                    className="text-xs"
                  >
                    Clear All
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Job Listings */}
        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map(i => (
              <Skeleton key={i} className="h-48 rounded-xl" />
            ))}
          </div>
        ) : filteredJobs.length > 0 ? (
          <>
            <div className="space-y-4">
              {paginatedJobs.map((job) => (
              <Card key={job.id} className="glass border-border/50 hover:border-primary/40 transition-colors">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                          {job.title}
                        </h3>
                        <Badge className="bg-green-500/15 text-green-400 border-green-500/20">
                          {job.match_percentage}% match
                        </Badge>
                      </div>
                      <p className="text-sm text-muted-foreground mb-3">{job.description}</p>
                      
                      {/* Job Details */}
                      <div className="flex flex-wrap gap-x-6 gap-y-2 text-sm">
                        <div className="flex items-center gap-2">
                          <span className="text-muted-foreground">📍</span>
                          <span>{job.location}</span>
                          {job.is_remote && (
                            <Badge className="bg-blue-500/15 text-blue-400 border-blue-500/20 text-xs">
                              Remote
                            </Badge>
                          )}
                        </div>
                        
                        {job.salary_range && (
                          <div className="flex items-center gap-2">
                            <span className="text-muted-foreground">💰</span>
                            <span>{job.salary_range}</span>
                          </div>
                        )}
                        
                        <div className="flex items-center gap-2">
                          <span className="text-muted-foreground">📅</span>
                          <span>{new Date(job.posted_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex flex-col gap-2 ml-4">
                      <Button 
                        className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0"
                        onClick={() => handleApply(job.id)}
                        disabled={applyingTo === job.id}
                      >
                        {applyingTo === job.id ? 'Applying...' : 'Apply Now'}
                      </Button>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => handleSave(job.id)}
                      >
                        {savedJobs.has(job.id) ? '★ Saved' : 'Save'}
                      </Button>
                    </div>
                  </div>

                  {/* Required Skills */}
                  {job.requirements && job.requirements.length > 0 && (
                    <div>
                      <p className="text-xs text-muted-foreground mb-2">Required Skills:</p>
                      <div className="flex flex-wrap gap-2">
                        {job.requirements.map((skill, idx) => (
                          <Badge key={idx} className="bg-primary/15 text-primary border-primary/25 text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Match Details */}
                  <div className="mt-4 pt-4 border-t border-border/50">
                    <div className="flex items-center justify-between text-xs text-muted-foreground">
                      <span>Skill Match: {job.skill_match}%</span>
                      <span>Overall Score: {job.score}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
              ))}
            </div>
            
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
              itemsPerPage={ITEMS_PER_PAGE}
              totalItems={filteredJobs.length}
            />
          </>
        ) : (
          <Card className="glass border-border/50">
            <CardContent className="p-12 text-center">
              <p className="text-lg text-muted-foreground mb-2">No jobs found</p>
              <p className="text-sm text-muted-foreground">
                Try adjusting your filters or check back later for new opportunities
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
