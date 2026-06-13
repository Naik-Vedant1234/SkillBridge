import { StudentSidebar } from "@/components/StudentSidebar";
import { ToastProvider } from "@/components/ui/toast";

export default function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ToastProvider>
      <div className="relative">
        <StudentSidebar />
        <div className="min-h-screen">
          {children}
        </div>
      </div>
    </ToastProvider>
  );
}
