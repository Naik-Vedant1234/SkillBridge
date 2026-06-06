import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

function StatCard({ value, label }: { value: string; label: string }) {
  return (
    <div className="glass rounded-2xl p-6 text-center hover-lift">
      <p className="text-3xl font-bold gradient-text mb-1">{value}</p>
      <p className="text-sm text-muted-foreground">{label}</p>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <Card className="glass border-border/50 hover-lift group">
      <CardContent className="p-6">
        <div className="text-3xl mb-4">{icon}</div>
        <h3 className="text-lg font-semibold mb-2">{title}</h3>
        <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
      </CardContent>
    </Card>
  );
}

function PortalCard({ emoji, role, description, href, color }: {
  emoji: string; role: string; description: string; href: string; color: string;
}) {
  return (
    <Link href={href} className="block h-full">
      <Card className="glass border-border/50 hover-lift cursor-pointer h-full">
        <CardContent className="p-8 flex flex-col items-center text-center gap-4">
          <div className="w-16 h-16 rounded-2xl flex items-center justify-center text-2xl" style={{ background: color }}>
            {emoji}
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-2">{role}</h3>
            <p className="text-sm text-muted-foreground">{description}</p>
          </div>
          <span className="mt-auto text-sm border border-border/50 rounded-lg px-4 py-1.5 hover:border-primary/50 hover:bg-primary/10 transition-colors">
            Get Started →
          </span>
        </CardContent>
      </Card>
    </Link>
  );
}

function StepCard({ step, title, description }: { step: string; title: string; description: string }) {
  return (
    <div className="flex gap-5 items-start">
      <div className="gradient-brand w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm shrink-0 glow">
        {step}
      </div>
      <div>
        <h4 className="font-semibold mb-1">{title}</h4>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
    </div>
  );
}

export default function LandingPage() {
  return (
    <div className="min-h-screen dot-grid">
      {/* ── Navbar ── */}
      <nav className="sticky top-0 z-50 glass border-b border-border/50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 gradient-brand rounded-lg glow" />
            <span className="font-bold text-lg">
              SkillBridge<span className="gradient-text"> AI</span>
            </span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm text-muted-foreground">
            <Link href="#features" className="hover:text-foreground transition-colors">Features</Link>
            <Link href="#portals" className="hover:text-foreground transition-colors">Portals</Link>
            <Link href="#how-it-works" className="hover:text-foreground transition-colors">How it works</Link>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors px-3 py-1.5 rounded-lg hover:bg-white/5"
            >
              Sign in
            </Link>
            <Link
              href="/register"
              className="text-sm font-medium text-white gradient-brand glow px-4 py-1.5 rounded-lg transition-opacity hover:opacity-90"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative max-w-7xl mx-auto px-6 pt-24 pb-20 text-center">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-primary/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-20 left-1/4 w-[300px] h-[300px] bg-blue-500/8 rounded-full blur-3xl pointer-events-none" />

        <div className="relative">
          <Badge className="mb-6 bg-primary/15 text-primary border-primary/25 px-4 py-1.5 text-sm">
            ✨ AI-Powered Career Intelligence
          </Badge>
          <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6">
            Launch Your Career
            <br />
            <span className="gradient-text">Smarter, Faster</span>
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
            SkillBridge AI matches students with the right jobs, internships, mentors, and
            learning paths — powered by semantic search, skill gap analysis, and Gemini AI.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/register"
              className="inline-flex items-center justify-center text-base font-medium text-white gradient-brand glow px-8 h-12 rounded-lg transition-opacity hover:opacity-90"
            >
              Start for free →
            </Link>
            <Link
              href="/login"
              className="inline-flex items-center justify-center text-base font-medium border border-border/60 hover:border-primary/50 hover:bg-primary/10 px-8 h-12 rounded-lg transition-colors"
            >
              Sign in
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-20">
          <StatCard value="1,000+" label="Students Placed" />
          <StatCard value="500+" label="Partner Companies" />
          <StatCard value="100+" label="Expert Mentors" />
          <StatCard value="95%" label="Match Accuracy" />
        </div>
      </section>

      {/* ── Features ── */}
      <section id="features" className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-14">
          <Badge className="mb-4 bg-primary/15 text-primary border-primary/25">Features</Badge>
          <h2 className="text-4xl font-bold mb-4">
            Everything you need to <span className="gradient-text">thrive</span>
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            From resume parsing to AI-generated roadmaps — all the tools to turn potential into placement.
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          <FeatureCard icon="🧠" title="AI Resume Analysis" description="Upload your resume and get instant skill extraction, gap analysis, and a placement readiness score powered by SpaCy + Gemini." />
          <FeatureCard icon="🎯" title="Smart Recommendations" description="Hybrid ranking engine combines semantic embeddings, skill matching, interest signals, and activity scores for laser-precise matches." />
          <FeatureCard icon="🗺️" title="Career Roadmaps" description="Get a week-by-week learning roadmap from our knowledge base, refined by Gemini AI, tailored to your exact career goal." />
          <FeatureCard icon="📊" title="Skill Gap Engine" description="Instantly see which skills you're missing for any target role, with importance ratings and recommended resources to close the gap." />
          <FeatureCard icon="👥" title="Mentor Matching" description="Connect with verified industry mentors in your domain. Request sessions, get feedback, and accelerate your growth." />
          <FeatureCard icon="📈" title="Placement Readiness" description="A 0–100 score breaking down your skills, projects, internships, and resume quality — so you know exactly where to improve." />
        </div>
      </section>

      {/* ── Portals ── */}
      <section id="portals" className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center mb-14">
          <Badge className="mb-4 bg-primary/15 text-primary border-primary/25">Portals</Badge>
          <h2 className="text-4xl font-bold mb-4">Built for <span className="gradient-text">everyone</span></h2>
          <p className="text-muted-foreground max-w-xl mx-auto">Four dedicated portals, each designed for its audience.</p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <PortalCard emoji="🎓" role="Student" description="Find jobs, internships, mentors, and build your career roadmap." href="/register?role=student" color="oklch(0.62 0.22 280 / 20%)" />
          <PortalCard emoji="🏢" role="Company" description="Post jobs, discover top candidates, and manage applications." href="/register?role=company" color="oklch(0.70 0.18 200 / 20%)" />
          <PortalCard emoji="👨‍🏫" role="Mentor" description="Guide students, manage mentee requests, and share expertise." href="/register?role=mentor" color="oklch(0.72 0.17 155 / 20%)" />
          <PortalCard emoji="⚙️" role="Admin" description="Oversee the platform, verify users, and monitor analytics." href="/login?role=admin" color="oklch(0.82 0.18 80 / 20%)" />
        </div>
      </section>

      {/* ── How it works ── */}
      <section id="how-it-works" className="max-w-7xl mx-auto px-6 py-20">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          <div>
            <Badge className="mb-4 bg-primary/15 text-primary border-primary/25">How it works</Badge>
            <h2 className="text-4xl font-bold mb-6">
              From resume to<br /><span className="gradient-text">dream offer</span>
            </h2>
            <p className="text-muted-foreground mb-10">
              Our AI pipeline processes your resume, builds a structured profile, generates embeddings,
              and continuously improves recommendations as you interact.
            </p>
            <div className="space-y-7">
              <StepCard step="1" title="Upload your resume" description="PDF parsed by PyMuPDF + SpaCy with skill ontology normalization." />
              <StepCard step="2" title="Build your profile" description="Skills, experience, and goals extracted into a structured profile." />
              <StepCard step="3" title="Get matched" description="Embedding similarity + skill scoring returns top jobs, internships, mentors, and courses." />
              <StepCard step="4" title="Follow your roadmap" description="Gemini AI refines a Knowledge Base roadmap to your exact skill gaps." />
            </div>
          </div>
          <div className="glass rounded-3xl p-8 space-y-3">
            {[
              { icon: "📄", label: "Resume PDF", color: "text-blue-400" },
              { icon: "⚙️", label: "PyMuPDF + SpaCy extraction", color: "text-purple-400" },
              { icon: "🗂️", label: "Skill Ontology normalization", color: "text-violet-400" },
              { icon: "🧱", label: "Profile Builder", color: "text-indigo-400" },
              { icon: "📐", label: "all-MiniLM-L6-v2 embeddings (384-dim)", color: "text-cyan-400" },
              { icon: "🗄️", label: "Qdrant vector storage", color: "text-teal-400" },
              { icon: "🎯", label: "Hybrid Recommender", color: "text-green-400" },
            ].map((item, i) => (
              <div key={i} className="flex items-center gap-4">
                <div className="w-9 h-9 rounded-xl bg-white/5 flex items-center justify-center text-lg shrink-0">{item.icon}</div>
                <p className={`text-sm font-medium flex-1 ${item.color}`}>{item.label}</p>
                {i < 6 && <div className="text-muted-foreground/40 text-xs shrink-0">↓</div>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="glass rounded-3xl p-12 md:p-16 text-center relative overflow-hidden">
          <div className="absolute inset-0 gradient-brand opacity-5 rounded-3xl" />
          <div className="relative">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Ready to <span className="gradient-text">bridge the gap?</span>
            </h2>
            <p className="text-muted-foreground mb-8 text-lg max-w-lg mx-auto">
              Join thousands of students who found their dream careers with SkillBridge AI.
            </p>
            <Link
              href="/register"
              className="inline-flex items-center justify-center text-base font-medium text-white gradient-brand glow px-10 h-12 rounded-lg transition-opacity hover:opacity-90"
            >
              Create your free account →
            </Link>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-border/40 py-10">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 gradient-brand rounded" />
            <span>SkillBridge AI</span>
          </div>
          <p>© {new Date().getFullYear()} SkillBridge AI. Built with FastAPI + Next.js 15.</p>
          <div className="flex gap-6">
            <Link href="/login" className="hover:text-foreground transition-colors">Sign in</Link>
            <Link href="/register" className="hover:text-foreground transition-colors">Register</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
