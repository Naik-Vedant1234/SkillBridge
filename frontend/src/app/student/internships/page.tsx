"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Pagination } from "@/components/ui/pagination";
import { useAuth } from "@/lib/auth-context";
import { apiClient } from "@/lib/api";
import { useToast } from "@/components/ui/toast";
import { useFilterPreferences } from "@/hooks/useFilterPreferences";
import Link from "next/link";
import { useEffect, useState } from "react";
import type { InternshipRecommendation, RecommendationsResponse } from "@/types/career";

const ITEMS_PER_PAGE = 12;

export default function InternshipsPage() {
  const { addToast } = useToast();
  const [internships, setInternships] = useState<InternshipRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [applyingTo, setApplyingTo] = useState<string | null>(null);
  const [savedInternships, setSavedInternships] = useState<Set<string>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  
  const { filters, updateFilters, resetFilters, isLoaded } = useFilterPreferences({
    key: 'internships',
    defaultFilters: {
      search: "",
      duration: "all",
      minStipend: 0,
      remote: "all",
    },
  });

  useEffect(() => {
    fetchInternships();
    loadSaved();
  }, []);

  // Reset to page 1 when filters change
  useEffect(() => {
    if (isLoaded) {
      setCurrentPage(1);
    }
  }, [filters, isLoaded]);

  const fetchInternships = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setLoading(true);
    try {
      const data = await apiClient.getInternshipRecommendations(token, 50) as RecommendationsResponse<InternshipRecommendation>;
      setInternships(data.recommendations);
    } catch (error) {
      console.error('Failed to fetch internships:', error);
      addToast('Failed to load internships', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadSaved = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      const data = await apiClient.getMyBookmarks(token, 'internship') as any;
      setSavedInternships(new Set(data.bookmarks.map((b: any) => b.target_id)));
    } catch (error) {
      console.error('Failed to load saved internships:', error);
    }
  };

  const handleApply = async (id: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    setApplyingTo(id);
    try {
      await apiClient.applyToInternship(token, id);
      addToast('Application submitted!', 'success');
    } catch (error: any) {
      addToast(error.message || 'Failed to apply', 'error');
    } finally {
      setApplyingTo(null);
    }
  };

  const handleSave = async (id: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      if (savedInternships.has(id)) {
        await apiClient.removeBookmark(token, 'internship', id);
        setSavedInternships(prev => {
          const newSet = new Set(prev);
          newSet.delete(id);
          return newSet;
        });
        addToast('Removed from saved', 'info');
      } else {
        await apiClient.bookmarkItem(token, 'internship', id);
        setSavedInternships(prev => new Set(prev).add(id));
        addToast('Saved successfully!', 'success');
      }
    } catch (error: any) {
      addToast(error.message || 'Failed', 'error');
    }
  };

  const filteredInternships = internships.filter(internship => {
    if (filters.search && !internship.title.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    if (filters.duration !== "all" && !internship.duration.includes(filters.duration)) {
      return false;
    }
    if (internship.stipend < filters.minStipend) {
      return false;
    }
    if (filters.remote !== "all") {
      if (filters.remote === "yes" && !internship.is_remote) return false;
      if (filters.remote === "no" && internship.is_remote) return false;
    }
    return true;
  });

  // Pagination
  const totalPages = Math.ceil(filteredInternships.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedInternships = filteredInternships.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                🎓 Internship Opportunities
              </h1>
              <p className="text-muted-foreground mt-1">
                {filteredInternships.length} internships available
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
                    placeholder="Internship title..."
                    value={filters.search}
                    onChange={(e) => updateFilters({ search: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  />
                </div>

                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Duration</label>
                  <select
                    value={filters.duration}
                    onChange={(e) => updateFilters({ duration: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Durations</option>
                    <option value="2">2 months</option>
                    <option value="3">3 months</option>
                    <option value="6">6 months</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Remote</label>
                  <select
                    value={filters.remote}
                    onChange={(e) => updateFilters({ remote: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Options</option>
                    <option value="yes">Remote</option>
                    <option value="no">On-site</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">
                    Min Stipend: ₹{filters.minStipend.toLocaleString()}
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="50000"
                    step="5000"
                    value={filters.minStipend}
                    onChange={(e) => updateFilters({ minStipend: parseInt(e.target.value) })}
                    className="w-full"
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Internship Listings */}
        {loading ? (
          <div className="grid md:grid-cols-2 gap-4">
            {[1, 2, 3, 4].map(i => <Skeleton key={i} className="h-64 rounded-xl" />)}
          </div>
        ) : filteredInternships.length > 0 ? (
          <>
            <div className="grid md:grid-cols-2 gap-4">
              {paginatedInternships.map((internship) => (
              <Card key={internship.id} className="glass border-border/50 hover:border-primary/40 transition-colors">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold mb-1" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                        {internship.title}
                      </h3>
                      <div className="flex items-center gap-2 mb-2">
                        <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">
                          {internship.match_percentage}% match
                        </Badge>
                        {internship.is_remote && (
                          <Badge className="bg-blue-500/15 text-blue-400 border-blue-500/20 text-xs">
                            Remote
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>

                  <p className="text-sm text-muted-foreground mb-4">
                    {internship.description}
                  </p>

                  {/* Details Grid */}
                  <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
                    <div>
                      <span className="text-muted-foreground">Duration:</span>
                      <p className="font-medium">{internship.duration}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Stipend:</span>
                      <p className="font-medium">₹{internship.stipend.toLocaleString()}/mo</p>
                    </div>
                    <div className="col-span-2">
                      <span className="text-muted-foreground">Location:</span>
                      <p className="font-medium">{internship.location}</p>
                    </div>
                  </div>

                  {/* Skills */}
                  {internship.requirements && internship.requirements.length > 0 && (
                    <div className="mb-4">
                      <p className="text-xs text-muted-foreground mb-2">Required:</p>
                      <div className="flex flex-wrap gap-1">
                        {internship.requirements.slice(0, 4).map((skill, idx) => (
                          <Badge key={idx} className="bg-primary/15 text-primary border-primary/25 text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="flex gap-2">
                    <Button 
                      className="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0"
                      onClick={() => handleApply(internship.id)}
                      disabled={applyingTo === internship.id}
                    >
                      {applyingTo === internship.id ? 'Applying...' : 'Apply'}
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => handleSave(internship.id)}
                    >
                      {savedInternships.has(internship.id) ? '★' : 'Save'}
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
            totalItems={filteredInternships.length}
          />
        </>
        ) : (
          <Card className="glass border-border/50">
            <CardContent className="p-12 text-center">
              <p className="text-lg text-muted-foreground">No internships found</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
