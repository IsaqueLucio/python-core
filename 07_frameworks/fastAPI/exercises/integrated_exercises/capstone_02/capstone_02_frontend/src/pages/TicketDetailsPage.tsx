import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { getApiErrorMessage } from '../api/errors';
import { getTicket, updateTicket, deleteTicket, assignTicket } from '../api/tickets';
import { getTicketComments, createTicketComment } from '../api/comments';
import { Loading } from '../components/feedback/Loading';
import { useToast } from '../components/feedback/ToastContext';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Select } from '../components/ui/Select';
import { Textarea } from '../components/ui/Textarea';
import { Input } from '../components/ui/Input';
import { Label } from '../components/ui/Label';
import { Modal } from '../components/ui/Modal';
import type { Ticket, TicketStatus } from '../types/domain';

const editTicketSchema = z.object({
  title: z.string().min(5, "Title must be at least 5 characters"),
  description: z.string().min(10, "Description must be at least 10 characters"),
  priority: z.enum(['low', 'medium', 'high', 'urgent']),
  category: z.enum(['hardware', 'software', 'network', 'access', 'other']),
});

type EditTicketValues = z.infer<typeof editTicketSchema>;

export default function TicketDetailsPage() {
  const { ticketId } = useParams<{ ticketId: string }>();
  const id = parseInt(ticketId || '0', 10);
  
  const { user } = useAuth();
  const navigate = useNavigate();
  const { success, error } = useToast();
  const queryClient = useQueryClient();

  const [commentText, setCommentText] = useState('');
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  // Queries
  const { data: ticket, isLoading: ticketLoading, isError: ticketError } = useQuery({
    queryKey: ['tickets', id],
    queryFn: () => getTicket(id),
    enabled: !!id
  });

  const { data: comments, isLoading: commentsLoading } = useQuery({
    queryKey: ['tickets', id, 'comments'],
    queryFn: () => getTicketComments(id),
    enabled: !!id
  });

  // Mutations
  const updateMutation = useMutation({
    mutationFn: (data: Partial<Ticket>) => updateTicket(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
      success('Ticket updated successfully');
      setIsEditModalOpen(false);
    },
    onError: (err: unknown) => error(getApiErrorMessage(err))
  });

  const assignMutation = useMutation({
    mutationFn: (agentId: number) => assignTicket(id, agentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
      success('Ticket assigned successfully');
    },
    onError: (err: unknown) => error(getApiErrorMessage(err))
  });

  const deleteMutation = useMutation({
    mutationFn: () => deleteTicket(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
      success('Ticket deleted successfully');
      navigate('/tickets');
    },
    onError: (err: unknown) => error(getApiErrorMessage(err))
  });

  const commentMutation = useMutation({
    mutationFn: (content: string) => createTicketComment(id, content),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tickets', id, 'comments'] });
      success('Comment added successfully');
      setCommentText('');
    },
    onError: (err: unknown) => error(getApiErrorMessage(err))
  });

  const { register, handleSubmit, formState: { errors }, reset } = useForm<EditTicketValues>({
    resolver: zodResolver(editTicketSchema)
  });

  useEffect(() => {
    if (ticket && isEditModalOpen) {
      reset({
        title: ticket.title,
        description: ticket.description,
        priority: ticket.priority,
        category: ticket.category
      });
    }
  }, [ticket, isEditModalOpen, reset]);

  if (ticketLoading) return <Loading />;
  if (ticketError || !ticket) return <div className="text-center py-12 text-destructive">Ticket not found or access denied.</div>;

  const formatDate = (isoStr: string) => {
    return new Intl.DateTimeFormat("en-US", {
      dateStyle: "medium",
      timeStyle: "short"
    }).format(new Date(isoStr));
  };

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    updateMutation.mutate({ status: e.target.value as TicketStatus });
  };

  const handleAssignToMe = () => {
    if (user) assignMutation.mutate(user.id);
  };

  const handleAddComment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;
    commentMutation.mutate(commentText);
  };

  const onEditSubmit = (data: EditTicketValues) => {
    updateMutation.mutate(data);
  };

  // Determine permissions
  // Note: These should match exactly with the backend rules.
  // The UI hides controls if these are false. The backend intercepts if accessed via API directly.
  const isCreator = ticket.created_by.id === user?.id;
  const isAssignedToMe = ticket.assigned_to?.id === user?.id;
  
  const canEditDetails = 
    user?.role === 'admin' || 
    (user?.role === 'agent' && isAssignedToMe) || 
    (user?.role === 'customer' && isCreator && ticket.status === 'open');

  const canChangeStatus = 
    user?.role === 'admin' || 
    (user?.role === 'agent' && isAssignedToMe);

  const canDelete = 
    user?.role === 'admin' || 
    (user?.role === 'customer' && isCreator && ticket.status === 'open');

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">#{ticket.id} {ticket.title}</h1>
          <p className="text-muted-foreground text-sm">
            Created by {ticket.created_by.name} on {formatDate(ticket.created_at)}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => navigate('/tickets')}>Back to List</Button>
          {canEditDetails && (
            <Button variant="secondary" onClick={() => setIsEditModalOpen(true)}>
              Edit Ticket
            </Button>
          )}
          {canDelete && (
            <Button variant="destructive" onClick={() => setIsDeleteModalOpen(true)}>
              Delete Ticket
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Main Content Area */}
        <div className="md:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Description</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="whitespace-pre-wrap">{ticket.description}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Comments</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {commentsLoading ? (
                <div className="py-4 text-center text-muted-foreground">Loading comments...</div>
              ) : comments && comments.length > 0 ? (
                <div className="space-y-4">
                  {comments.map(c => (
                    <div key={c.id} className="border rounded-lg p-4 bg-muted/30">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-semibold">{c.author.name}</span>
                        <span className="text-xs text-muted-foreground">{formatDate(c.created_at)}</span>
                      </div>
                      <p className="text-sm whitespace-pre-wrap">{c.content}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center text-muted-foreground py-4">No comments yet.</div>
              )}

              <form onSubmit={handleAddComment} className="mt-4 pt-4 border-t space-y-3">
                <Textarea 
                  placeholder="Add a comment..." 
                  value={commentText}
                  onChange={(e) => setCommentText(e.target.value)}
                  rows={3}
                />
                <Button 
                  type="submit" 
                  disabled={!commentText.trim() || commentMutation.isPending}
                >
                  {commentMutation.isPending ? 'Posting...' : 'Post Comment'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar Info Area */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-1">
                <span className="text-sm text-muted-foreground font-medium">Status</span>
                {canChangeStatus ? (
                  <Select value={ticket.status} onChange={handleStatusChange} disabled={updateMutation.isPending}>
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="waiting_customer">Waiting for Customer</option>
                    <option value="resolved">Resolved</option>
                    <option value="closed">Closed</option>
                  </Select>
                ) : (
                  <div><Badge>{ticket.status.replace('_', ' ').toUpperCase()}</Badge></div>
                )}
              </div>

              <div className="space-y-1">
                <span className="text-sm text-muted-foreground font-medium">Priority</span>
                <div><Badge variant={ticket.priority === 'urgent' ? 'destructive' : 'default'}>{ticket.priority.toUpperCase()}</Badge></div>
              </div>

              <div className="space-y-1">
                <span className="text-sm text-muted-foreground font-medium">Category</span>
                <div><span className="text-sm capitalize">{ticket.category}</span></div>
              </div>

              <div className="space-y-1">
                <span className="text-sm text-muted-foreground font-medium">Assigned To</span>
                <div className="flex flex-col gap-2">
                  <span className="text-sm">{ticket.assigned_to ? ticket.assigned_to.name : 'Unassigned'}</span>
                  {user?.role === 'agent' && !ticket.assigned_to && (
                    <Button variant="outline" size="sm" onClick={handleAssignToMe} disabled={assignMutation.isPending}>
                      Assign to Me
                    </Button>
                  )}
                </div>
              </div>

              <div className="space-y-1 pt-2 border-t border-border">
                <span className="text-xs text-muted-foreground">Last updated: {formatDate(ticket.updated_at)}</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <Modal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        title="Edit Ticket"
        description="Update the ticket details below."
      >
        <form onSubmit={handleSubmit(onEditSubmit)} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="title">Title</Label>
            <Input id="title" {...register('title')} error={!!errors.title} />
            {errors.title && <p className="text-sm text-destructive">{errors.title.message}</p>}
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="category">Category</Label>
            <Select id="category" {...register('category')} error={!!errors.category}>
              <option value="hardware">Hardware</option>
              <option value="software">Software</option>
              <option value="network">Network</option>
              <option value="access">Access</option>
              <option value="other">Other</option>
            </Select>
            {errors.category && <p className="text-sm text-destructive">{errors.category.message}</p>}
          </div>

          <div className="space-y-2">
            <Label htmlFor="priority">Priority</Label>
            <Select id="priority" {...register('priority')} error={!!errors.priority}>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </Select>
            {errors.priority && <p className="text-sm text-destructive">{errors.priority.message}</p>}
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea id="description" rows={4} {...register('description')} error={!!errors.description} />
            {errors.description && <p className="text-sm text-destructive">{errors.description.message}</p>}
          </div>

          <div className="flex justify-end gap-2 pt-4">
            <Button type="button" variant="outline" onClick={() => setIsEditModalOpen(false)}>Cancel</Button>
            <Button type="submit" disabled={updateMutation.isPending}>
              {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
            </Button>
          </div>
        </form>
      </Modal>

      <Modal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        title="Delete Ticket"
        description="Are you sure you want to delete this ticket? This action cannot be undone."
      >
        <div className="flex justify-end gap-2 pt-4">
          <Button variant="outline" onClick={() => setIsDeleteModalOpen(false)}>Cancel</Button>
          <Button 
            variant="destructive" 
            onClick={() => deleteMutation.mutate()} 
            disabled={deleteMutation.isPending}
          >
            {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
          </Button>
        </div>
      </Modal>
    </div>
  );
}
