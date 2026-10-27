import { useQuery } from '@tanstack/react-query';
import { getDashboardSummary } from '../api/dashboard';
import { getTickets } from '../api/tickets';
import { Loading } from '../components/feedback/Loading';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { 
  Ticket as TicketIcon, 
  Clock, 
  CheckCircle2, 
  AlertCircle,
  FolderOpen
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import type { Ticket, TicketPriority, TicketStatus } from '../types/domain';

interface TicketListProps {
  data: { items: Ticket[] } | undefined;
  isLoading: boolean;
  isError: boolean;
  emptyMessage: string;
}

function TicketList({ data, isLoading, isError, emptyMessage }: TicketListProps) {
  const navigate = useNavigate();

  if (isLoading) return <div className="py-4 text-center text-muted-foreground">Loading...</div>;
  if (isError) return <div className="py-4 text-center text-destructive">Failed to load tickets.</div>;
  if (!data || data.items.length === 0) return <div className="py-4 text-center text-muted-foreground">{emptyMessage}</div>;

  const getStatusBadge = (s: TicketStatus) => {
    switch(s) {
      case 'open': return <Badge variant="secondary">Open</Badge>;
      case 'in_progress': return <Badge variant="default">In Progress</Badge>;
      case 'waiting_customer': return <Badge variant="warning">Waiting for Customer</Badge>;
      case 'resolved': return <Badge variant="success">Resolved</Badge>;
      case 'closed': return <Badge variant="outline">Closed</Badge>;
      default: return <Badge>{s}</Badge>;
    }
  };

  const getPriorityBadge = (p: TicketPriority) => {
    switch(p) {
      case 'urgent': return <Badge variant="destructive">Urgent</Badge>;
      case 'high': return <Badge variant="warning">High</Badge>;
      case 'medium': return <Badge variant="secondary">Medium</Badge>;
      case 'low': return <Badge variant="outline">Low</Badge>;
      default: return <Badge>{p}</Badge>;
    }
  };

  return (
    <div className="space-y-2">
      {data.items.map((ticket: Ticket) => (
        <div 
          key={ticket.id} 
          className="flex flex-col sm:flex-row sm:items-center justify-between p-3 border rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
          onClick={() => navigate(`/tickets/${ticket.id}`)}
        >
          <div className="mb-2 sm:mb-0 truncate pr-4">
            <span className="font-medium block truncate">{ticket.title}</span>
            <span className="text-xs text-muted-foreground">#{ticket.id} • {ticket.category}</span>
          </div>
          <div className="flex gap-2 shrink-0">
            {getPriorityBadge(ticket.priority)}
            {getStatusBadge(ticket.status)}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function DashboardPage() {
  const { user } = useAuth();
  
  const { data: summary, isLoading: summaryLoading, error: summaryError } = useQuery({
    queryKey: ['dashboardSummary'],
    queryFn: getDashboardSummary,
  });

  const { data: recentTickets, isLoading: recentLoading, isError: recentError } = useQuery({
    queryKey: ['tickets', 'recent'],
    queryFn: () => getTickets({ page: 1, page_size: 5 }),
  });

  const { data: urgentTickets, isLoading: urgentLoading, isError: urgentError } = useQuery({
    queryKey: ['tickets', 'urgent'],
    queryFn: () => getTickets({ page: 1, page_size: 5, priority: 'urgent' }),
  });

  if (summaryLoading) return <Loading />;
  
  if (summaryError || !summary) {
    return (
      <div className="flex h-[50vh] items-center justify-center">
        <div className="text-center text-destructive">
          <AlertCircle className="mx-auto h-10 w-10 mb-4 opacity-50" />
          <p>Failed to load dashboard summary.</p>
        </div>
      </div>
    );
  }

  const statCards = [
    { title: 'Total Tickets', value: summary.total_tickets, icon: TicketIcon, color: 'text-blue-500' },
    { title: 'Open', value: summary.open_tickets, icon: FolderOpen, color: 'text-yellow-500' },
    { title: 'In Progress', value: summary.in_progress_tickets, icon: Clock, color: 'text-primary' },
    { title: 'Resolved / Closed', value: summary.resolved_tickets + summary.closed_tickets, icon: CheckCircle2, color: 'text-green-500' },
  ];

  if (user?.role !== 'customer') {
    statCards.push(
      { title: 'Urgent', value: summary.urgent_tickets, icon: AlertCircle, color: 'text-destructive' },
      { title: 'Assigned to Me', value: summary.my_assigned_tickets, icon: TicketIcon, color: 'text-purple-500' }
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome back, {user?.name}. Here is what's happening today.
          </p>
        </div>
        <Link to="/tickets/new">
          <Button>Create Ticket</Button>
        </Link>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <Card key={stat.title}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                {stat.title}
              </CardTitle>
              <stat.icon className={`h-4 w-4 ${stat.color}`} />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Recent Tickets</CardTitle>
            <Link to="/tickets" className="text-sm text-primary hover:underline">View all</Link>
          </CardHeader>
          <CardContent>
            <TicketList 
              data={recentTickets} 
              isLoading={recentLoading} 
              isError={recentError} 
              emptyMessage="No recent tickets found." 
            />
          </CardContent>
        </Card>

        <div className="col-span-4 lg:col-span-3 space-y-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Urgent Tickets</CardTitle>
            </CardHeader>
            <CardContent>
              <TicketList 
                data={urgentTickets} 
                isLoading={urgentLoading} 
                isError={urgentError} 
                emptyMessage="No urgent tickets found." 
              />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-2">
              {user?.role === 'agent' && (
                <Link to="/tickets?assigned_to_me=true">
                  <Button variant="outline" className="w-full justify-start">My Assigned Tickets</Button>
                </Link>
              )}
              {user?.role === 'admin' && (
                <Link to="/users">
                  <Button variant="outline" className="w-full justify-start">Manage Users</Button>
                </Link>
              )}
              <Link to="/profile">
                <Button variant="outline" className="w-full justify-start">My Profile</Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
