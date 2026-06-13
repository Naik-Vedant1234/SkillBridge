"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Pagination } from "@/components/ui/pagination";
import { apiClient } from "@/lib/api";
import { useToast } from "@/components/ui/toast";
import { useFilterPreferences } from "@/hooks/useFilterPreferences";
import Link from "next/link";
import { useEffect, useState } from "react";
import type { CourseRecommendation, RecommendationsResponse } from "@/types/career";

const ITEMS_PER_PAGE = 12;

export default function CoursesPage() {
  const { addToast } = useToast();
  const [courses, setCourses] = useState<CourseRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [savedCourses, setSavedCourses] = useState<Set<string>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  
  const { filters, updateFilters, resetFilters, isLoaded } = useFilterPreferences({
    key: 'courses',
    defaultFilters: {
      search: "",
      difficulty: "all",
      provider: "all",
      isFree: "all",
    },
  });

  useEffect(() => {
    fetchCourses();
    loadSaved();
  }, []);

  useEffect(() => {
    if (isLoaded) setCurrentPage(1);
  }, [filters, isLoaded]);

  const fetchCourses = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setLoading(true);
    try {
      const data = await apiClient.getCourseRecommendations(token, 50) as RecommendationsResponse<CourseRecommendation>;
      setCourses(data.recommendations);
    } catch (error) {
      console.error('Failed to fetch courses:', error);
      addToast('Failed to load courses', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadSaved = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      const data = await apiClient.getMyBookmarks(token, 'course') as any;
      setSavedCourses(new Set(data.bookmarks.map((b: any) => b.target_id)));
    } catch (error) {
      console.error('Failed to load saved courses:', error);
    }
  };

  const handleSave = async (courseId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      if (savedCourses.has(courseId)) {
        await apiClient.removeBookmark(token, 'course', courseId);
        setSavedCourses(prev => {
          const newSet = new Set(prev);
          newSet.delete(courseId);
          return newSet;
        });
        addToast('Course removed from saved', 'info');
      } else {
        await apiClient.bookmarkItem(token, 'course', courseId);
        setSavedCourses(prev => new Set(prev).add(courseId));
        addToast('Course saved successfully!', 'success');
      }
    } catch (error: any) {
      addToast(error.message || 'Failed to save', 'error');
    }
  };

  const filteredCourses = courses.filter(course => {
    if (filters.search && !course.title.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    if (filters.difficulty !== "all" && course.difficulty !== filters.difficulty) {
      return false;
    }
    if (filters.provider !== "all" && course.provider !== filters.provider) {
      return false;
    }
    if (filters.isFree !== "all") {
      if (filters.isFree === "yes" && !course.is_free) return false;
      if (filters.isFree === "no" && course.is_free) return false;
    }
    return true;
  });

  const providers = Array.from(new Set(courses.map(c => c.provider)));
  
  // Pagination
  const totalPages = Math.ceil(filteredCourses.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedCourses = filteredCourses.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'beginner': return 'bg-green-500/15 text-green-400 border-green-500/20';
      case 'intermediate': return 'bg-amber-500/15 text-amber-400 border-amber-500/20';
      case 'advanced': return 'bg-red-500/15 text-red-400 border-red-500/20';
      default: return 'bg-gray-500/15 text-gray-400 border-gray-500/20';
    }
  };

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                📚 Course Recommendations
              </h1>
              <p className="text-muted-foreground mt-1">
                {filteredCourses.length} courses to boost your skills
              </p>
            </div>
            <Link href="/student/dashboard">
              <Button variant="outline">← Back to Dashboard</Button>
            </Link>
          </div>

          {/* Filters */}
          <Card className="glass border-border/50">
            <CardContent className="p-4">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Search</label>
                  <input
                    type="text"
                    placeholder="Course title..."
                    value={filters.search}
                    onChange={(e) => updateFilters({ search: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  />
                </div>

                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Difficulty</label>
                  <select
                    value={filters.difficulty}
                    onChange={(e) => updateFilters({ difficulty: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Levels</option>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Provider</label>
                  <select
                    value={filters.provider}
                    onChange={(e) => updateFilters({ provider: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Providers</option>
                    {providers.map(provider => (
                      <option key={provider} value={provider}>{provider}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Price</label>
                  <select
                    value={filters.isFree}
                    onChange={(e) => updateFilters({ isFree: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Courses</option>
                    <option value="yes">Free Only</option>
                    <option value="no">Paid Only</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Course Grid */}
        {loading ? (
          <div className="grid md:grid-cols-2 gap-4">
            {[1, 2, 3, 4].map(i => <Skeleton key={i} className="h-72 rounded-xl" />)}
          </div>
        ) : filteredCourses.length > 0 ? (
          <>
            <div className="grid md:grid-cols-2 gap-4">
              {paginatedCourses.map((course) => (
              <Card key={course.id} className="glass border-border/50 hover:border-primary/40 transition-colors">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge className={getDifficultyColor(course.difficulty)}>
                          {course.difficulty}
                        </Badge>
                        <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">
                          {course.match_percentage}% match
                        </Badge>
                        {course.is_free && (
                          <Badge className="bg-blue-500/15 text-blue-400 border-blue-500/20 text-xs">
                            Free
                          </Badge>
                        )}
                      </div>
                      <h3 className="text-lg font-bold mb-1" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                        {course.title}
                      </h3>
                      <p className="text-xs text-muted-foreground mb-3">
                        by {course.provider} • {course.duration}
                      </p>
                    </div>
                  </div>

                  <p className="text-sm text-muted-foreground mb-4">
                    {course.description}
                  </p>

                  {/* Skills Covered */}
                  {course.skills_covered && course.skills_covered.length > 0 && (
                    <div className="mb-4">
                      <p className="text-xs text-muted-foreground mb-2">Skills you'll learn:</p>
                      <div className="flex flex-wrap gap-1">
                        {course.skills_covered.slice(0, 5).map((skill, idx) => (
                          <Badge key={idx} className="bg-primary/15 text-primary border-primary/25 text-xs">
                            {skill}
                          </Badge>
                        ))}
                        {course.skills_covered.length > 5 && (
                          <Badge className="bg-muted/50 text-muted-foreground border-muted text-xs">
                            +{course.skills_covered.length - 5} more
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Match Info */}
                  <div className="flex items-center justify-between text-xs text-muted-foreground mb-4 pb-4 border-b border-border/50">
                    <span>Skill Gap Match: {course.skill_gap_match}%</span>
                    <span>Score: {course.score}</span>
                  </div>

                  <div className="flex gap-2">
                    <Button className="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0">
                      Enroll Now
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => handleSave(course.id)}
                    >
                      {savedCourses.has(course.id) ? '★ Saved' : 'Save'}
                    </Button>
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
            totalItems={filteredCourses.length}
          />
        </>
        ) : (
          <Card className="glass border-border/50">
            <CardContent className="p-12 text-center">
              <p className="text-lg text-muted-foreground">No courses found</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
