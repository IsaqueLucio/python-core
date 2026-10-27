import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getTickets } from '../api/tickets';
import { Loading } from '../components/feedback/Loading';
import { useAuth } from '../contexts/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Select } from '../components/ui/Select';
import { Badge } from '../components/ui/Badge';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '../components/ui/Table';
import type { TicketPriority, TicketStatus } from '../types/domain';

export default function TicketsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  
  const [page, setPage] = useState(1);
  const [searchInput, setSearchInput] = useState('');
  
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    priority: '',
    category: '',
    assignedToMe: false
  });

  // Debounce search and reset page together
  useEffect(() => {
    const timer = setTimeout(() => {
      setFilters(f => {
        if (f.search !== searchInput) {
          setPage(1);
          return { ...f, search: searchInput };
        }
        return f;
      });
    }, 500);
    return () => clearTimeout(timer);
  }, [searchInput]);

  const updateFilter = (key: keyof typeof filters, value: string | boolean) => {
    setFilters(f => ({ ...f, [key]: value }));
    setPage(1);
  };

  const { data, isLoading, isError } = useQuery({
    queryKey: ['tickets', page, filters],
    queryFn: () => getTickets({
      page,
      page_size: 10,
      search: filters.search || undefined,
      status: filters.status || undefined,
      priority: filters.priority || undefined,
      category: filters.category || undefined,
      assigned_to_me: filters.assignedToMe ? true : undefined
    })
  });

  const clearFilters = () => {
    setSearchInput('');
    setFilters({ search: '', status: '', priority: '', category: '', assignedToMe: false });
    setPage(1);
  };

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

  const formatDate = (isoStr: string) => {
    return new Intl.DateTimeFormat("en-US", {
      dateStyle: "medium",
      timeStyle: "short"
    }).format(new Date(isoStr));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Tickets</h1>
          <p className="text-muted-foreground">
            Manage and view support tickets.
          </p>
        </div>
        <Link to="/tickets/new">
          <Button>Create Ticket</Button>
        </Link>
      </div>

      <Card className="p-4">
        <div className="flex flex-col sm:flex-row flex-wrap gap-4 mb-4">
          <Input
            placeholder="Search tickets..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            className="sm:w-64"
          />
          <Select 
            value={filters.status}
            onChange={(e) => updateFilter('status', e.target.value)}
            className="sm:w-40"
          >
            <option value="">All Statuses</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="waiting_customer">Waiting for Customer</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </Select>
          <Select 
            value={filters.priority}
            onChange={(e) => updateFilter('priority', e.target.value)}
            className="sm:w-32"
          >
            <option value="">All Priorities</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </Select>
          <Select 
            value={filters.category}
            onChange={(e) => updateFilter('category', e.target.value)}
            className="sm:w-36"
          >
            <option value="">All Categories</option>
            <option value="hardware">Hardware</option>
            <option value="software">Software</option>
            <option value="network">Network</option>
            <option value="access">Access</option>
            <option value="other">Other</option>
          </Select>
          
          {user?.role !== 'customer' && (
            <label className="flex items-center space-x-2 text-sm font-medium">
              <input 
                type="checkbox" 
                checked={filters.assignedToMe}
                onChange={(e) => updateFilter('assignedToMe', e.target.checked)}
                className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span>Assigned to Me</span>
            </label>
          )}

          {(filters.search || filters.status || filters.priority || filters.category || filters.assignedToMe) && (
            <Button variant="ghost" onClick={clearFilters}>Clear Filters</Button>
          )}
        </div>

        {isLoading ? (
          <div className="py-12"><Loading /></div>
        ) : isError ? (
          <div className="py-12 text-center text-destructive">Failed to load tickets.</div>
        ) : !data || data.items.length === 0 ? (
          <div className="py-12 text-center text-muted-foreground">No tickets found.</div>
        ) : (
          <>
            {/* Desktop Table View */}
            <div className="hidden md:block">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>ID</TableHead>
                    <TableHead>Title</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Priority</TableHead>
                    <TableHead>Created</TableHead>
                    <TableHead>Assigned To</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {data.items.map((ticket) => (
                    <TableRow 
                      key={ticket.id} 
                      className="cursor-pointer hover:bg-muted/50"
                      onClick={() => navigate(`/tickets/${ticket.id}`)}
                    >
                      <TableCell className="font-medium">#{ticket.id}</TableCell>
                      <TableCell>{ticket.title}</TableCell>
                      <TableCell>{getStatusBadge(ticket.status)}</TableCell>
                      <TableCell>{getPriorityBadge(ticket.priority)}</TableCell>
                      <TableCell>{formatDate(ticket.created_at)}</TableCell>
                      <TableCell>{ticket.assigned_to ? ticket.assigned_to.name : 'Unassigned'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>

            {/* Mobile Card View */}
            <div className="grid gap-4 md:hidden">
              {data.items.map((ticket) => (
                <div 
                  key={ticket.id} 
                  className="rounded-lg border p-4 shadow-sm cursor-pointer hover:bg-muted/50"
                  onClick={() => navigate(`/tickets/${ticket.id}`)}
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-medium">#{ticket.id}</span>
                    <div className="flex gap-1">
                      {getPriorityBadge(ticket.priority)}
                      {getStatusBadge(ticket.status)}
                    </div>
                  </div>
                  <h3 className="font-semibold mb-1 line-clamp-1">{ticket.title}</h3>
                  <div className="text-xs text-muted-foreground mt-2 flex justify-between">
                    <span>{formatDate(ticket.created_at)}</span>
                    <span>{ticket.assigned_to ? ticket.assigned_to.name : 'Unassigned'}</span>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between mt-4">
              <span className="text-sm text-muted-foreground">
                Showing {data.items.length} of {data.total} results
              </span>
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  size="sm" 
                  disabled={page <= 1}
                  onClick={() => setPage(p => p - 1)}
                >
                  Previous
                </Button>
                <Button 
                  variant="outline" 
                  size="sm" 
                  disabled={page >= data.total_pages}
                  onClick={() => setPage(p => p + 1)}
                >
                  Next
                </Button>
              </div>
            </div>
          </>
        )}
      </Card>
    </div>
  );
}
