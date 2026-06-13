"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Badge } from "@/components/ui/badge";

export function StudentSidebar() {
  const [isExpanded, setIsExpanded] = useState(false);
  const pathname = usePathname();

  const isActive = (path: string) => pathname === path;

  const navItems = [
    { 
      section: "Main",
      items: [
        { icon: "🏠", label: "Dashboard", path: "/student/dashboard" },
        { icon: "👤", label: "Profile", path: "/student/profile" },
      ]
    },
    {
      section: "Opportunities",
      items: [
        { icon: "💼", label: "Jobs", path: "/student/jobs" },
        { icon: "🎓", label: "Internships", path: "/student/internships" },
        { icon: "👨‍🏫", label: "Mentors", path: "/student/mentors" },
      ]
    },
    {
      section: "Learning",
      items: [
        { icon: "📚", label: "Courses", path: "/student/courses" },
        { icon: "👥", label: "Study Groups", path: "/student/study-groups" },
        { icon: "🗺️", label: "Career Roadmap", path: "/student/roadmap" },
      ]
    },
    {
      section: "My Activity",
      items: [
        { icon: "📄", label: "Resume", path: "/student/resume" },
        { icon: "📝", label: "Applications", path: "/student/applications" },
        { icon: "🔖", label: "Saved", path: "/student/saved" },
      ]
    },
    {
      section: "Settings",
      items: [
        { icon: "⚙️", label: "Settings", path: "/student/settings" },
        { icon: "🔔", label: "Notifications", path: "/student/notifications" },
        { icon: "❓", label: "Help & Support", path: "/student/help" },
      ]
    }
  ];

  return (
    <>
      {/* Trigger Bar - Always visible on left edge */}
      <div
        className="fixed left-0 top-0 h-full w-2 bg-gradient-to-r from-purple-500/20 to-transparent hover:from-purple-500/40 transition-all z-40 cursor-pointer"
        onMouseEnter={() => setIsExpanded(true)}
      />

      {/* Sidebar */}
      <div
        className={`fixed left-0 top-0 h-full bg-black/95 backdrop-blur-xl border-r border-border/50 transition-all duration-300 z-50 ${
          isExpanded ? "w-72" : "w-0"
        } overflow-hidden`}
        onMouseLeave={() => setIsExpanded(false)}
      >
        {/* Header */}
        <div className="p-6 border-b border-border/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-xl">
              🎓
            </div>
            <div>
              <h2 className="text-lg font-bold" style={{ fontFamily: "Space Grotesk, sans-serif" }}>
                SkillBridge
              </h2>
              <p className="text-xs text-muted-foreground">Student Portal</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="p-4 overflow-y-auto h-[calc(100vh-120px)]">
          {navItems.map((section, sectionIdx) => (
            <div key={sectionIdx} className="mb-6">
              <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2 px-3">
                {section.section}
              </p>
              <div className="space-y-1">
                {section.items.map((item, itemIdx) => (
                  <Link key={itemIdx} href={item.path}>
                    <div
                      className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all cursor-pointer ${
                        isActive(item.path)
                          ? "bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 text-white"
                          : "hover:bg-white/5 text-muted-foreground hover:text-white"
                      }`}
                    >
                      <span className="text-xl">{item.icon}</span>
                      <span className="text-sm font-medium">{item.label}</span>
                      {isActive(item.path) && (
                        <div className="ml-auto w-1.5 h-1.5 rounded-full bg-purple-500" />
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-border/50 bg-black/50">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>💡 Tip:</span>
            <span>Hover left edge to open menu</span>
          </div>
        </div>
      </div>

      {/* Overlay for mobile */}
      {isExpanded && (
        <div
          className="fixed inset-0 bg-black/50 z-40 md:hidden"
          onClick={() => setIsExpanded(false)}
        />
      )}
    </>
  );
}
