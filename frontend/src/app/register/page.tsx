"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

const ROLES = [
  { value: "student", label: "Student", emoji: "🎓", desc: "Find jobs, mentors & roadmaps" },
  { value: "company", label: "Company", emoji: "🏢", desc: "Post jobs & discover talent" },
  { value: "mentor", label: "Mentor", emoji: "👨‍🏫", desc: "Guide the next generation" },
] as const;

function RegisterForm() {
  const searchParams = useSearchParams();
  const defaultRole = searchParams.get("role") ?? "student";

  return (
    <div className="min-h-screen dot-grid flex items-center justify-center p-6">
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-[500px] h-[400px] bg-primary/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative w-full max-w-lg">
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2">
            <div className="w-8 h-8 gradient-brand rounded-lg glow" />
            <span className="font-bold text-xl">
              SkillBridge<span className="gradient-text"> AI</span>
            </span>
          </Link>
        </div>

        <Card className="glass border-border/50">
          <CardHeader className="pb-4">
            <h1 className="text-2xl font-bold text-center">Create your account</h1>
            <p className="text-sm text-muted-foreground text-center mt-1">
              Join SkillBridge AI — it&apos;s free
            </p>
          </CardHeader>

          <CardContent className="space-y-5">
            {/* Role selector */}
            <div className="space-y-2">
              <Label>I am a...</Label>
              <div className="grid grid-cols-3 gap-2">
                {ROLES.map((role) => (
                  <label
                    key={role.value}
                    htmlFor={`role-${role.value}`}
                    className={`cursor-pointer rounded-xl border p-3 text-center transition-all hover:border-primary/50 hover:bg-primary/5 ${
                      defaultRole === role.value
                        ? "border-primary/60 bg-primary/10"
                        : "border-border/50"
                    }`}
                  >
                    <input
                      type="radio"
                      id={`role-${role.value}`}
                      name="role"
                      value={role.value}
                      defaultChecked={defaultRole === role.value}
                      className="sr-only"
                    />
                    <div className="text-2xl mb-1">{role.emoji}</div>
                    <div className="text-xs font-semibold">{role.label}</div>
                    <div className="text-xs text-muted-foreground mt-0.5 hidden sm:block">{role.desc}</div>
                  </label>
                ))}
              </div>
            </div>

            {/* Google OAuth */}
            <Button
              variant="outline"
              className="w-full border-border/60 hover:border-primary/40 hover:bg-primary/5"
              id="btn-google-register"
            >
              <svg className="w-4 h-4 mr-2" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
              </svg>
              Continue with Google
            </Button>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-border/50" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-card px-2 text-muted-foreground">or</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-2">
                <Label htmlFor="name">Full name</Label>
                <Input id="name" placeholder="Jane Doe" className="bg-white/5 border-border/50 focus:border-primary/60" />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input id="email" type="email" placeholder="jane@uni.edu" className="bg-white/5 border-border/50 focus:border-primary/60" />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" placeholder="Min. 8 characters" className="bg-white/5 border-border/50 focus:border-primary/60" />
            </div>

            <Button className="w-full gradient-brand glow border-0 text-white" id="btn-register-submit">
              Create account →
            </Button>

            <p className="text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <Link href="/login" className="text-primary hover:underline font-medium">
                Sign in
              </Link>
            </p>
          </CardContent>
        </Card>

        <p className="text-center text-xs text-muted-foreground mt-4">
          By registering you agree to our{" "}
          <span className="text-primary/70 hover:text-primary cursor-pointer">Terms</span> and{" "}
          <span className="text-primary/70 hover:text-primary cursor-pointer">Privacy Policy</span>.
        </p>
      </div>
    </div>
  );
}

export default function RegisterPage() {
  return (
    <Suspense>
      <RegisterForm />
    </Suspense>
  );
}
