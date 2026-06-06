import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const metadata = { title: "Company Dashboard" };

export default function CompanyDashboardPage() {
  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
              Company Dashboard 🏢
            </h1>
            <p className="text-muted-foreground mt-1">Manage your job postings and find top talent.</p>
          </div>
          <Badge className="bg-cyan-500/15 text-cyan-400 border-cyan-500/20 px-3 py-1">
            Phase 5 — Portal coming soon
          </Badge>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Active Jobs", value: "8", color: "gradient-text" },
            { label: "Applications", value: "142", color: "text-cyan-400" },
            { label: "Shortlisted", value: "23", color: "text-green-400" },
            { label: "Hired", value: "5", color: "text-amber-400" },
          ].map(({ label, value, color }) => (
            <Card key={label} className="glass border-border/50">
              <CardContent className="p-5">
                <p className="text-xs text-muted-foreground mb-1">{label}</p>
                <p className={`text-3xl font-bold ${color}`} style={{ fontFamily: "Space Grotesk, sans-serif" }}>{value}</p>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          <Card className="glass border-border/50">
            <CardHeader>
              <CardTitle className="text-base flex items-center justify-between" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                Active Job Postings
                <Button size="sm" className="gradient-brand border-0 text-white text-xs">+ Post Job</Button>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {["Backend Engineer", "Frontend Engineer", "ML Engineer"].map((title, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/3">
                  <div>
                    <p className="text-sm font-medium">{title}</p>
                    <p className="text-xs text-muted-foreground">{[28, 19, 35][i]} applicants</p>
                  </div>
                  <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs">Active</Badge>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="glass border-border/50">
            <CardHeader>
              <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                Recent Applications
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {["Priya Sharma", "Rahul Kumar", "Ananya Patel"].map((name, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/3">
                  <div>
                    <p className="text-sm font-medium">{name}</p>
                    <p className="text-xs text-muted-foreground">Backend Engineer • CGPA {(8.5 - i * 0.3).toFixed(1)}</p>
                  </div>
                  <Badge className="bg-amber-500/15 text-amber-400 border-amber-500/20 text-xs">Pending</Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
