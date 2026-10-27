import { NavLink } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { 
  LayoutDashboard, 
  Ticket as TicketIcon, 
  Users, 
  User as UserIcon,
  LogOut
} from 'lucide-react';
import { cn } from '../ui/Button';

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export function Sidebar({ isOpen, setIsOpen }: SidebarProps) {
  const { user, logout } = useAuth();

  if (!user) return null;

  const links = [
    { name: 'Dashboard', to: '/dashboard', icon: LayoutDashboard },
    { name: 'Tickets', to: '/tickets', icon: TicketIcon },
    // Only show Users link to admins
    ...(user.role === 'admin' ? [{ name: 'Users', to: '/users', icon: Users }] : []),
    { name: 'Profile', to: '/profile', icon: UserIcon },
  ];

  const handleLinkClick = () => {
    // on mobile, close sidebar after clicking a link
    if (window.innerWidth < 1024) {
      setIsOpen(false);
    }
  };

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 z-20 bg-background/80 backdrop-blur-sm lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar sidebar */}
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-30 w-64 flex-col border-r bg-card transition-transform duration-300 ease-in-out lg:static lg:flex lg:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex h-16 items-center px-6 border-b">
          <TicketIcon className="h-6 w-6 text-primary mr-2" />
          <span className="text-lg font-bold tracking-tight">HelpDesk</span>
        </div>

        <nav className="flex-1 space-y-1 px-4 py-6 overflow-y-auto">
          {links.map((link) => (
            <NavLink
              key={link.name}
              to={link.to}
              onClick={handleLinkClick}
              className={({ isActive }) =>
                cn(
                  "flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )
              }
            >
              <link.icon className="mr-3 h-5 w-5" />
              {link.name}
            </NavLink>
          ))}
        </nav>

        <div className="border-t p-4">
          <div className="flex items-center px-3 py-2 mb-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/20 text-primary">
              <span className="text-sm font-bold uppercase">{user.name.charAt(0)}</span>
            </div>
            <div className="ml-3 flex flex-col">
              <span className="text-sm font-medium leading-none">{user.name}</span>
              <span className="text-xs text-muted-foreground mt-1 truncate max-w-[140px]">{user.role}</span>
            </div>
          </div>
          <button
            onClick={() => logout()}
            className="flex w-full items-center rounded-md px-3 py-2 text-sm font-medium text-destructive transition-colors hover:bg-destructive/10"
          >
            <LogOut className="mr-3 h-5 w-5" />
            Sign Out
          </button>
        </div>
      </aside>
    </>
  );
}
