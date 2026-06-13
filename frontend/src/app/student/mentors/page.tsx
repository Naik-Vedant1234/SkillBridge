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
import type { MentorRecommendation, RecommendationsResponse } from "@/types/career";

const ITEMS_PER_PAGE = 15;

export default function MentorsPage() {
  const { addToast } = useToast();
  const [mentors, setMentors] = useState<MentorRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [savedMentors, setSavedMentors] = useState<Set<string>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  
  const { filters, updateFilters, resetFilters, isLoaded } = useFilterPreferences({
    key: 'mentors',
    defaultFilters: {
      search: "",
      domain: "all",
      minExperience: 0,
    },
  });

  useEffect(() => {
    fetchMentors();
    loadSaved();
  }, []);

  useEffect(() => {
    if (isLoaded) setCurrentPage(1);
  }, [filters, isLoaded]);

  const fetchMentors = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setLoading(true);
    try {
      const data = await apiClient.getMentorRecommendations(token, 50) as RecommendationsResponse<MentorRecommendation>;
      setMentors(data.recommendations);
    } catch (error) {
      console.error('Failed to fetch mentors:', error);
      addToast('Failed to load mentors', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadSaved = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      const data = await apiClient.getMyBookmarks(token, 'mentor') as any;
      setSavedMentors(new Set(data.bookmarks.map((b: any) => b.target_id)));
    } catch (error) {
      console.error('Failed to load saved mentors:', error);
    }
  };

  const handleSave = async (mentorId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      if (savedMentors.has(mentorId)) {
        await apiClient.removeBookmark(token, 'mentor', mentorId);
        setSavedMentors(prev => {
          const newSet = new Set(prev);
          newSet.delete(mentorId);
          return newSet;
        });
        addToast('Removed from saved', 'info');
      } else {
        await apiClient.bookmarkItem(token, 'mentor', mentorId);
        setSavedMentors(prev => new Set(prev).add(mentorId));
        addToast('Mentor saved successfully!', 'success');
      }
    } catch (error: any) {
      addToast(error.message || 'Failed to save', 'error');
    }
  };

  const filteredMentors = mentors.filter(mentor => {
    if (filters.search && !mentor.name.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    if (filters.domain !== "all" && mentor.domain !== filters.domain) {
      return false;
    }
    if (mentor.experience < filters.minExperience) {
      return false;
    }
    return true;
  });

  const domains = Array.from(new Set(mentors.map(m => m.domain)));
  
  const totalPages = Math.ceil(filteredMentors.length / ITEMS_PER_PAGE);
  const paginatedMentors = filteredMentors.slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE);

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                👨‍🏫 Find Your Mentor
              </h1>
              <p className="text-muted-foreground mt-1">
                {filteredMentors.length} experienced mentors available
              </p>
            </div>
            <Link href="/student/dashboard">
              <Button variant="outline">← Back to Dashboard</Button>
            </Link>
          </div>

          {/* Filters */}
          <Card className="glass border-border/50">
            <CardContent className="p-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Search</label>
                  <input
                    type="text"
                    placeholder="Mentor name..."
                    value={filters.search}
                    onChange={(e) => updateFilters({ search: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  />
                </div>

                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">Domain</label>
                  <select
                    value={filters.domain}
                    onChange={(e) => updateFilters({ domain: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Domains</option>
                    {domains.map(domain => (
                      <option key={domain} value={domain}>{domain}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-xs text-muted-foreground mb-2 block">
                    Min Experience: {filters.minExperience} years
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="20"
                    step="1"
                    value={filters.minExperience}
                    onChange={(e) => updateFilters({ minExperience: parseInt(e.target.value) })}
                    className="w-full"
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Mentor Grid */}
        {loading ? (
          <div className="grid md:grid-cols-3 gap-4">
            {[1, 2, 3, 4, 5, 6].map(i => <Skeleton key={i} className="h-80 rounded-xl" />)}
          </div>
        ) : filteredMentors.length > 0 ? (
          <>
            <div className="grid md:grid-cols-3 gap-4">
              {paginatedMentors.map((mentor) => (
              <Card key={mentor.id} className="glass border-border/50 hover:border-primary/40 transition-colors">
                <CardContent className="p-6">
                  {/* Profile Header */}
                  <div className="flex flex-col items-center text-center mb-4">
                    <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-3xl mb-3">
                      {mentor.name.charAt(0)}
                    </div>
                    <h3 className="text-lg font-bold mb-1" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                      {mentor.name}
                    </h3>
                    <div className="flex items-center gap-2 mb-2">
                      <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">
                        {mentor.match_percentage}% match
                      </Badge>
                      {mentor.is_verified && (
                        <Badge className="bg-blue-500/15 text-blue-400 border-blue-500/20 text-xs">
                          ✓ Verified
                        </Badge>
                      )}
                    </div>
                  </div>

                  {/* Details */}
                  <div className="space-y-3 mb-4">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Domain:</span>
                      <span className="font-medium">{mentor.domain}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Experience:</span>
                      <span className="font-medium">{mentor.experience} years</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">Capacity:</span>
                      <span className="font-medium">{mentor.max_mentees} mentees</span>
                    </div>
                  </div>

                  {/* Bio */}
                  <p className="text-xs text-muted-foreground mb-4 line-clamp-3">
                    {mentor.bio}
                  </p>

                  {/* Actions */}
                  <div className="flex flex-col gap-2">
                    <Button className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0">
                      Request Mentorship
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="w-full"
                      onClick={() => handleSave(mentor.id)}
                    >
                      {savedMentors.has(mentor.id) ? '★ Saved' : 'Save for Later'}
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
            totalItems={filteredMentors.length}
          />
        </>
        ) : (
          <Card className="glass border-border/50">
            <CardContent className="p-12 text-center">
              <p className="text-lg text-muted-foreground">No mentors found</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
