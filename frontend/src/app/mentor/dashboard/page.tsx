import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export const metadata = { title: "Mentor Dashboard" };

export default function MentorDashboardPage() {
  return (
    <div className="min-h-screen dot-grid p-6 md:p-10">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
              Mentor Dashboard 👨‍🏫
            </h1>
            <p className="text-muted-foreground mt-1">Guide students and manage mentorship sessions.</p>
          </div>
          <Badge className="bg-green-500/15 text-green-400 border-green-500/20 px-3 py-1">
            Phase 5 — Portal coming soon
          </Badge>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Active Mentees", value: "4", color: "gradient-text" },
            { label: "Pending Requests", value: "7", color: "text-amber-400" },
            { label: "Sessions This Month", value: "12", color: "text-cyan-400" },
            { label: "Avg. Rating", value: "4.8", color: "text-green-400" },
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
                Mentorship Requests
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {["Arjun Singh", "Meera Nair", "Karan Mehta"].map((name, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-xl bg-white/3">
                  <div>
                    <p className="text-sm font-medium">{name}</p>
                    <p className="text-xs text-muted-foreground">Backend • CGPA {(8.9 - i * 0.4).toFixed(1)}</p>
                  </div>
                  <div className="flex gap-2">
                    <Badge className="bg-green-500/15 text-green-400 border-green-500/20 text-xs cursor-pointer">Accept</Badge>
                    <Badge className="bg-red-500/15 text-red-400 border-red-500/20 text-xs cursor-pointer">Decline</Badge>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          <Card className="glass border-border/50">
            <CardHeader>
              <CardTitle className="text-base" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                Upcoming Sessions
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {[
                { name: "Riya Kapoor", time: "Today 4:00 PM", topic: "Resume Review" },
                { name: "Dev Patel", time: "Tomorrow 11:00 AM", topic: "Mock Interview" },
              ].map(({ name, time, topic }) => (
                <div key={name} className="p-3 rounded-xl bg-white/3">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-medium">{name}</p>
                    <p className="text-xs text-muted-foreground">{time}</p>
                  </div>
                  <Badge className="bg-primary/15 text-primary border-primary/25 text-xs">{topic}</Badge>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
