import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const metadata = { title: "Admin Dashboard" };

export default function AdminDashboardPage() {
  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
              Admin Dashboard ⚙️
            </h1>
            <p className="text-muted-foreground mt-1">Platform overview, user management, and analytics.</p>
          </div>
          <Badge className="bg-amber-500/15 text-amber-400 border-amber-500/20 px-3 py-1">
            Phase 5 — Portal coming soon
          </Badge>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total Users", value: "1,203", color: "gradient-text" },
            { label: "Companies", value: "80", color: "text-cyan-400" },
            { label: "Mentors Pending", value: "12", color: "text-amber-400" },
            { label: "Active Jobs", value: "347", color: "text-green-400" },
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
              <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                Pending Verifications
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {[
                { name: "TechCorp India", type: "Company", status: "Pending" },
                { name: "Dr. Amit Verma", type: "Mentor", status: "Pending" },
                { name: "InnoStartup Pvt.", type: "Company", status: "Pending" },
              ].map(({ name, type, status }) => (
                <div key={name} className="flex items-center justify-between p-3 rounded-xl bg-white/3">
                  <div>
                    <p className="text-sm font-medium">{name}</p>
                    <p className="text-xs text-muted-foreground">{type}</p>
                  </div>
                  <div className="flex gap-2">
                    <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs cursor-pointer">Verify</Badge>
                    <Badge className="bg-red-500/15 text-red-400 border-red-500/20 text-xs cursor-pointer">Reject</Badge>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="glass border-border/50">
            <CardHeader>
              <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                Platform Health
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {[
                { service: "PostgreSQL", status: "Online", color: "text-green-400" },
                { service: "Redis", status: "Online", color: "text-green-400" },
                { service: "Qdrant", status: "Online", color: "text-green-400" },
                { service: "Celery Workers", status: "2 active", color: "text-cyan-400" },
                { service: "FastAPI", status: "Online", color: "text-green-400" },
              ].map(({ service, status, color }) => (
                <div key={service} className="flex items-center justify-between p-2 rounded-lg">
                  <span className="text-sm">{service}</span>
                  <span className={`text-xs font-medium ${color}`}>● {status}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
