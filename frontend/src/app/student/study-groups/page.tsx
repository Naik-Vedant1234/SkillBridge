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
import type { StudyGroupRecommendation, RecommendationsResponse } from "@/types/career";

const ITEMS_PER_PAGE = 15;

export default function StudyGroupsPage() {
  const { addToast } = useToast();
  const [groups, setGroups] = useState<StudyGroupRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [savedGroups, setSavedGroups] = useState<Set<string>>(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  
  const { filters, updateFilters, resetFilters, isLoaded } = useFilterPreferences({
    key: 'study_groups',
    defaultFilters: {
      search: "",
      domain: "all",
      level: "all",
    },
  });

  useEffect(() => {
    fetchGroups();
    loadSaved();
  }, []);

  useEffect(() => {
    if (isLoaded) setCurrentPage(1);
  }, [filters, isLoaded]);

  const fetchGroups = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setLoading(true);
    try {
      const data = await apiClient.getStudyGroupRecommendations(token, 50) as RecommendationsResponse<StudyGroupRecommendation>;
      setGroups(data.recommendations);
    } catch (error) {
      console.error('Failed to fetch study groups:', error);
      addToast('Failed to load study groups', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadSaved = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      const data = await apiClient.getMyBookmarks(token, 'study_group') as any;
      setSavedGroups(new Set(data.bookmarks.map((b: any) => b.target_id)));
    } catch (error) {
      console.error('Failed to load saved groups:', error);
    }
  };

  const handleSave = async (groupId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    try {
      if (savedGroups.has(groupId)) {
        await apiClient.removeBookmark(token, 'study_group', groupId);
        setSavedGroups(prev => {
          const newSet = new Set(prev);
          newSet.delete(groupId);
          return newSet;
        });
        addToast('Removed from saved', 'info');
      } else {
        await apiClient.bookmarkItem(token, 'study_group', groupId);
        setSavedGroups(prev => new Set(prev).add(groupId));
        addToast('Study group saved!', 'success');
      }
    } catch (error: any) {
      addToast(error.message || 'Failed to save', 'error');
    }
  };

  const filteredGroups = groups.filter(group => {
    if (filters.search && !group.name.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    if (filters.domain !== "all" && group.domain !== filters.domain) {
      return false;
    }
    if (filters.level !== "all" && group.skill_level !== filters.level) {
      return false;
    }
    return true;
  });

  const domains = Array.from(new Set(groups.map(g => g.domain)));
  
  const totalPages = Math.ceil(filteredGroups.length / ITEMS_PER_PAGE);
  const paginatedGroups = filteredGroups.slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE);

  const getLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
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
                👥 Study Groups
              </h1>
              <p className="text-muted-foreground mt-1">
                {filteredGroups.length} active study groups to join
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
                    placeholder="Group name..."
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
                  <label className="text-xs text-muted-foreground mb-2 block">Skill Level</label>
                  <select
                    value={filters.level}
                    onChange={(e) => updateFilters({ level: e.target.value })}
                    className="w-full bg-background border border-border/60 rounded-lg px-3 py-2 text-sm"
                  >
                    <option value="all">All Levels</option>
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Study Groups Grid */}
        {loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3, 4, 5, 6].map(i => <Skeleton key={i} className="h-64 rounded-xl" />)}
          </div>
        ) : filteredGroups.length > 0 ? (
          <>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {paginatedGroups.map((group) => (
              <Card key={group.id} className="glass border-border/50 hover:border-primary/40 transition-colors">
                <CardContent className="p-6">
                  {/* Header */}
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <Badge className={getLevelColor(group.skill_level)}>
                        {group.skill_level}
                      </Badge>
                      <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">
                        {group.match_percentage}% match
                      </Badge>
                    </div>
                    <h3 className="text-lg font-bold mb-1" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                      {group.name}
                    </h3>
                    <p className="text-xs text-muted-foreground">
                      {group.domain}
                    </p>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                    {group.description}
                  </p>

                  {/* Stats */}
                  <div className="grid grid-cols-2 gap-3 mb-4 text-sm">
                    <div>
                      <span className="text-muted-foreground block text-xs">Members</span>
                      <p className="font-medium">{group.current_members || 0} / {group.max_members}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground block text-xs">Status</span>
                      <p className="font-medium">
                        {group.is_active ? (
                          <span className="text-green-400">Active</span>
                        ) : (
                          <span className="text-red-400">Inactive</span>
                        )}
                      </p>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="mb-4">
                    <div className="w-full bg-muted/30 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all"
                        style={{ width: `${((group.current_members || 0) / group.max_members) * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col gap-2">
                    <Button 
                      className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0"
                      disabled={(group.current_members || 0) >= group.max_members}
                    >
                      {(group.current_members || 0) >= group.max_members ? 'Full' : 'Join Group'}
                    </Button>
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="w-full"
                      onClick={() => handleSave(group.id)}
                    >
                      {savedGroups.has(group.id) ? '★ Saved' : 'Save for Later'}
                    </Button>
                  </div>

                  {/* Match Score */}
                  <div className="mt-4 pt-4 border-t border-border/50 text-center">
                    <span className="text-xs text-muted-foreground">
                      Match Score: {group.score}
                    </span>
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
            totalItems={filteredGroups.length}
          />
        </>
        ) : (
          <Card className="glass border-border/50">
            <CardContent className="p-12 text-center">
              <p className="text-lg text-muted-foreground">No study groups found</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
