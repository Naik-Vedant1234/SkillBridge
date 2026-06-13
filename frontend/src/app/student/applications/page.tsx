"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { apiClient } from "@/lib/api";
import { useToast } from "@/components/ui/toast";
import Link from "next/link";
import { useEffect, useState } from "react";

interface Application {
  id: string;
  target_type: string;
  target_id: string;
  target: {
    title: string;
    company_id: string | null;
  };
  status: string;
  cover_letter: string | null;
  applied_at: string;
  updated_at: string;
}

export default function ApplicationsPage() {
  const { addToast } = useToast();
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [withdrawing, setWithdrawing] = useState<string | null>(null);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    setLoading(true);
    try {
      const data = await apiClient.getMyApplications(token) as any;
      setApplications(data.applications);
    } catch (error) {
      console.error('Failed to fetch applications:', error);
      addToast('Failed to load applications', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleWithdraw = async (appId: string) => {
    const token = localStorage.getItem('access_token');
    if (!token) return;

    if (!confirm('Are you sure you want to withdraw this application?')) return;

    setWithdrawing(appId);
    try {
      await apiClient.withdrawApplication(token, appId);
      addToast('Application withdrawn', 'info');
      // Refresh applications
      await fetchApplications();
    } catch (error: any) {
      addToast(error.message || 'Failed to withdraw', 'error');
    } finally {
      setWithdrawing(null);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'bg-amber-500/15 text-amber-400 border-amber-500/20';
      case 'reviewing': return 'bg-blue-500/15 text-blue-400 border-blue-500/20';
      case 'accepted': return 'bg-green-500/15 text-green-400 border-green-500/20';
      case 'rejected': return 'bg-red-500/15 text-red-400 border-red-500/20';
      case 'withdrawn': return 'bg-gray-500/15 text-gray-400 border-gray-500/20';
      default: return 'bg-gray-500/15 text-gray-400 border-gray-500/20';
    }
  };

  const stats = {
    total: applications.length,
    pending: applications.filter(a => a.status === 'pending').length,
    reviewing: applications.filter(a => a.status === 'reviewing').length,
    accepted: applications.filter(a => a.status === 'accepted').length,
  };

  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                📝 My Applications
              </h1>
              <p className="text-muted-foreground mt-1">
                Track all your job and internship applications
              </p>
            </div>
            <Link href="/student/dashboard">
              <Button variant="outline">← Back to Dashboard</Button>
            </Link>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <Card className="glass border-border/50">
            <CardContent className="p-4">
              <p className="text-xs text-muted-foreground mb-1">Total</p>
              <p className="text-2xl font-bold gradient-text">{stats.total}</p>
            </CardContent>
          </Card>
          <Card className="glass border-border/50">
            <CardContent className="p-4">
              <p className="text-xs text-muted-foreground mb-1">Pending</p>
              <p className="text-2xl font-bold text-amber-400">{stats.pending}</p>
            </CardContent>
          </Card>
          <Card className="glass border-border/50">
            <CardContent className="p-4">
              <p className="text-xs text-muted-foreground mb-1">Reviewing</p>
              <p className="text-2xl font-bold text-blue-400">{stats.reviewing}</p>
            </CardContent>
          </Card>
          <Card className="glass border-border/50">
            <CardContent className="p-4">
              <p className="text-xs text-muted-foreground mb-1">Accepted</p>
              <p className="text-2xl font-bold text-green-400">{stats.accepted}</p>
            </CardContent>
          </Card>
        </div>

        {/* Applications List */}
        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map(i => <Skeleton key={i} className="h-32 rounded-xl" />)}
          </div>
        ) : applications.length > 0 ? (
          <div className="space-y-4">
            {applications.map((app) => (
              <Card key={app.id} className="glass border-border/50">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <Badge className="bg-primary/15 text-primary border-primary/25 text-xs">
                          {app.target_type}
                        </Badge>
                        <Badge className={getStatusColor(app.status)}>
                          {app.status}
                        </Badge>
                      </div>
                      <h3 className="text-lg font-bold mb-1" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                        {app.target.title}
                      </h3>
                      <p className="text-xs text-muted-foreground">
                        Applied on {new Date(app.applied_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex flex-col gap-2">
                      {app.status !== 'withdrawn' && (
                        <Button 
                          size="sm" 
                          variant="ghost" 
                          className="text-red-400 hover:text-red-300"
                          onClick={() => handleWithdraw(app.id)}
                          disabled={withdrawing === app.id}
                        >
                          {withdrawing === app.id ? 'Withdrawing...' : 'Withdraw'}
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="glass border-border/50">
            <CardContent className="p-12 text-center">
              <div className="text-4xl mb-4">📝</div>
              <p className="text-lg font-medium mb-2">No applications yet</p>
              <p className="text-sm text-muted-foreground mb-4">
                Start applying to jobs and internships
              </p>
              <div className="flex gap-2 justify-center">
                <Link href="/student/jobs">
                  <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 border-0">
                    Browse Jobs
                  </Button>
                </Link>
                <Link href="/student/internships">
                  <Button variant="outline">Browse Internships</Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
