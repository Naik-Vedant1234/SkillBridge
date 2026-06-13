"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { apiClient } from "@/lib/api";
import { useToast } from "@/components/ui/toast";
import Link from "next/link";
import { useEffect, useState } from "react";

interface BookmarkItem {
  // Common fields
  title?: string;
  name?: string;
  // Job/Internship fields
  location?: string;
  salary_range?: string;
  is_remote?: boolean;
  stipend?: number;
  duration?: string;
  company_id?: string;
  // Mentor fields
  domain?: string;
  experience?: number;
  bio?: string;
  // Course fields
  provider?: string;
  difficulty?: string;
  is_free?: boolean;
  // Study Group fields
  skill_level?: string;
  current_members?: number;
  max_members?: number;
}

interface Bookmark {
  id: string;
  target_type: string;
  target_id: string;
  created_at: string;
  item: BookmarkItem | null;
}

export default function SavedPage() {
  const { addToast } = useToast();
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [loading, setLoading] = useState(true);
  const [removing, setRemoving] = useState<string | null>(null);

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const fetchBookmarks = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setLoading(true);
    try {
      const data = await apiClient.getMyBookmarks(token) as any;
      setBookmarks(data.bookmarks);
    } catch (error) {
      console.error('Failed to fetch bookmarks:', error);
      addToast('Failed to load saved items', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = async (targetType: string, targetId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setRemoving(targetId);
    try {
      await apiClient.removeBookmark(token, targetType, targetId);
      addToast('Removed from saved', 'info');
      await fetchBookmarks();
    } catch (error: any) {
      addToast(error.message || 'Failed to remove', 'error');
    } finally {
      setRemoving(null);
    }
  };

  const getBookmarksByType = (type: string) => {
    return bookmarks.filter(b => b.target_type === type);
  };

  const renderEmptyState = (type: string, emoji: string, title: string, linkHref: string, linkText: string) => (
    <Card className="glass border-border/50">
      <CardContent className="p-12 text-center">
        <div className="text-4xl mb-4">{emoji}</div>
        <p className="text-lg font-medium mb-2">{title}</p>
        <p className="text-sm text-muted-foreground mb-4">
          {type === 'job' && 'Start saving jobs you\'re interested in to review later'}
          {type === 'internship' && 'Bookmark internships to compare and apply later'}
          {type === 'mentor' && 'Save mentor profiles to connect with them later'}
          {type === 'course' && 'Bookmark courses for your learning roadmap'}
          {type === 'study_group' && 'Save groups you want to join'}
        </p>
        <Link href={linkHref}>
          <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0">
            {linkText}
          </Button>
        </Link>
      </CardContent>
    </Card>
  );

  const renderBookmarksList = (type: string) => {
    const items = getBookmarksByType(type);
    
    if (loading) {
      return (
        <div className="space-y-4">
          {[1, 2, 3].map(i => <Skeleton key={i} className="h-32 rounded-xl" />)}
        </div>
      );
    }

    if (items.length === 0) {
      const configs = {
        job: { emoji: '💼', title: 'No saved jobs yet', link: '/student/jobs', linkText: 'Browse Jobs' },
        internship: { emoji: '🎓', title: 'No saved internships', link: '/student/internships', linkText: 'Browse Internships' },
        mentor: { emoji: '👨‍🏫', title: 'No saved mentors', link: '/student/mentors', linkText: 'Find Mentors' },
        course: { emoji: '📚', title: 'No saved courses', link: '/student/courses', linkText: 'Browse Courses' },
        study_group: { emoji: '👥', title: 'No saved study groups', link: '/student/study-groups', linkText: 'Browse Study Groups' },
      };
      const config = configs[type as keyof typeof configs];
      return renderEmptyState(type, config.emoji, config.title, config.link, config.linkText);
    }

    const pageMap: Record<string, string> = {
      job: '/student/jobs',
      internship: '/student/internships',
      mentor: '/student/mentors',
      course: '/student/courses',
      study_group: '/student/study-groups',
    };

    return (
      <div className="space-y-4">
        {items.map((bookmark) => {
          const item = bookmark.item;
          
          return (
            <Card key={bookmark.id} className="glass border-border/50 hover:border-primary/40 transition-colors">
              <CardContent className="p-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge className="bg-primary/15 text-primary border-primary/25 text-xs">
                        {bookmark.target_type.replace('_', ' ')}
                      </Badge>
                    </div>
                    
                    {item ? (
                      <>
                        <h3 className="text-lg font-bold mb-1" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                          {item.title || item.name}
                        </h3>
                        
                        {/* Type-specific details */}
                        {bookmark.target_type === 'job' && (
                          <div className="text-sm text-muted-foreground space-y-1">
                            <p>📍 {item.location} {item.is_remote && '• Remote'}</p>
                            {item.salary_range && <p>💰 {item.salary_range}</p>}
                          </div>
                        )}
                        
                        {bookmark.target_type === 'internship' && (
                          <div className="text-sm text-muted-foreground space-y-1">
                            <p>📍 {item.location}</p>
                            <p>💰 ₹{item.stipend?.toLocaleString()}/mo • {item.duration}</p>
                          </div>
                        )}
                        
                        {bookmark.target_type === 'mentor' && (
                          <div className="text-sm text-muted-foreground space-y-1">
                            <p>🎯 {item.domain}</p>
                            <p>💼 {item.experience} years experience</p>
                            {item.bio && <p className="text-xs line-clamp-2 mt-2">{item.bio}</p>}
                          </div>
                        )}
                        
                        {bookmark.target_type === 'course' && (
                          <div className="text-sm text-muted-foreground space-y-1">
                            <p>by {item.provider}</p>
                            <p>📚 {item.difficulty} • {item.duration}</p>
                            {item.is_free && <Badge className="bg-blue-500/15 text-blue-400 border-blue-500/20 text-xs mt-1">Free</Badge>}
                          </div>
                        )}
                        
                        {bookmark.target_type === 'study_group' && (
                          <div className="text-sm text-muted-foreground space-y-1">
                            <p>🎯 {item.domain}</p>
                            <p>👥 {item.current_members || 0}/{item.max_members} members</p>
                            <Badge className="bg-amber-500/15 text-amber-400 border-amber-500/20 text-xs mt-1">
                              {item.skill_level}
                            </Badge>
                          </div>
                        )}
                        
                        <p className="text-xs text-muted-foreground mt-3">
                          Saved on {new Date(bookmark.created_at).toLocaleDateString()}
                        </p>
                      </>
                    ) : (
                      <p className="text-sm text-muted-foreground">
                        Item details not available
                      </p>
                    )}
                  </div>
                  
                  <div className="flex flex-col gap-2">
                    <Link href={pageMap[bookmark.target_type]}>
                      <Button size="sm" variant="outline">
                        View All
                      </Button>
                    </Link>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="text-red-400 hover:text-red-300"
                      onClick={() => handleRemove(bookmark.target_type, bookmark.target_id)}
                      disabled={removing === bookmark.target_id}
                    >
                      {removing === bookmark.target_id ? 'Removing...' : 'Remove'}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                🔖 Saved Items
              </h1>
              <p className="text-muted-foreground mt-1">
                {bookmarks.length} bookmarked opportunities and resources
              </p>
            </div>
            <Link href="/student/dashboard">
              <Button variant="outline">← Back to Dashboard</Button>
            </Link>
          </div>
        </div>

        <Tabs defaultValue="jobs" className="w-full">
          <TabsList className="grid grid-cols-5 w-full mb-6">
            <TabsTrigger value="jobs">
              Jobs ({getBookmarksByType('job').length})
            </TabsTrigger>
            <TabsTrigger value="internships">
              Internships ({getBookmarksByType('internship').length})
            </TabsTrigger>
            <TabsTrigger value="mentors">
              Mentors ({getBookmarksByType('mentor').length})
            </TabsTrigger>
            <TabsTrigger value="courses">
              Courses ({getBookmarksByType('course').length})
            </TabsTrigger>
            <TabsTrigger value="groups">
              Groups ({getBookmarksByType('study_group').length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="jobs">{renderBookmarksList('job')}</TabsContent>
          <TabsContent value="internships">{renderBookmarksList('internship')}</TabsContent>
          <TabsContent value="mentors">{renderBookmarksList('mentor')}</TabsContent>
          <TabsContent value="courses">{renderBookmarksList('course')}</TabsContent>
          <TabsContent value="groups">{renderBookmarksList('study_group')}</TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
