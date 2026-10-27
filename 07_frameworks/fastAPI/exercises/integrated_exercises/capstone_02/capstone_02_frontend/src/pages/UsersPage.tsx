import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getUsers, updateUser } from '../api/users';
import { getApiErrorMessage } from '../api/errors';
import { Loading } from '../components/feedback/Loading';
import { useToast } from '../components/feedback/ToastContext';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { Select } from '../components/ui/Select';
import { Badge } from '../components/ui/Badge';
import { Modal } from '../components/ui/Modal';
import { Label } from '../components/ui/Label';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '../components/ui/Table';
import type { User, UserRole } from '../types/domain';

export default function UsersPage() {
  const [page, setPage] = useState(1);
  const [searchInput, setSearchInput] = useState('');
  
  const [filters, setFilters] = useState({
    search: '',
    role: '',
    isActive: ''
  });

  const { success, error } = useToast();
  const queryClient = useQueryClient();

  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [editRole, setEditRole] = useState<UserRole>('customer');
  const [editActive, setEditActive] = useState<boolean>(true);

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
    queryKey: ['users', page, filters],
    queryFn: () => getUsers({
      page,
      page_size: 10,
      search: filters.search || undefined,
      role: filters.role || undefined,
      is_active: filters.isActive === 'true' ? true : filters.isActive === 'false' ? false : undefined
    })
  });

  const mutation = useMutation({
    mutationFn: ({ id, data }: { id: number, data: Partial<User> }) => updateUser(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      success('User updated successfully');
      setEditingUser(null);
    },
    onError: (err: unknown) => {
      error(getApiErrorMessage(err));
    }
  });

  const handleEditClick = (user: User) => {
    setEditingUser(user);
    setEditRole(user.role);
    setEditActive(user.is_active);
  };

  const handleSave = () => {
    if (!editingUser) return;
    mutation.mutate({
      id: editingUser.id,
      data: {
        role: editRole,
        is_active: editActive
      }
    });
  };

  const clearFilters = () => {
    setSearchInput('');
    setFilters({ search: '', role: '', isActive: '' });
    setPage(1);
  };

  const formatDate = (isoStr: string) => {
    return new Intl.DateTimeFormat("en-US", {
      dateStyle: "medium",
      timeStyle: "short"
    }).format(new Date(isoStr));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Users</h1>
        <p className="text-muted-foreground">
          Manage system users and their roles.
        </p>
      </div>

      <Card className="p-4">
        <div className="flex flex-col sm:flex-row gap-4 mb-4">
          <Input
            placeholder="Search by name or email..."
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            className="sm:w-64"
          />
          <Select 
            value={filters.role}
            onChange={(e) => updateFilter('role', e.target.value)}
            className="sm:w-48"
          >
            <option value="">All Roles</option>
            <option value="customer">Customer</option>
            <option value="agent">Support Agent</option>
            <option value="admin">Administrator</option>
          </Select>
          <Select 
            value={filters.isActive}
            onChange={(e) => updateFilter('isActive', e.target.value)}
            className="sm:w-48"
          >
            <option value="">All Statuses</option>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </Select>
          {(filters.search || filters.role || filters.isActive) && (
            <Button variant="ghost" onClick={clearFilters}>Clear Filters</Button>
          )}
        </div>

        {isLoading ? (
          <div className="py-12"><Loading /></div>
        ) : isError ? (
          <div className="py-12 text-center text-destructive">Failed to load users.</div>
        ) : !data || data.items.length === 0 ? (
          <div className="py-12 text-center text-muted-foreground">No users found.</div>
        ) : (
          <>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Joined</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.items.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell className="font-medium">{user.name}</TableCell>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>
                      {user.role === 'admin' ? (
                        <Badge variant="destructive">Admin</Badge>
                      ) : user.role === 'agent' ? (
                        <Badge variant="secondary">Agent</Badge>
                      ) : (
                        <Badge variant="outline">Customer</Badge>
                      )}
                    </TableCell>
                    <TableCell>
                      {user.is_active ? (
                        <Badge variant="success">Active</Badge>
                      ) : (
                        <Badge variant="secondary">Inactive</Badge>
                      )}
                    </TableCell>
                    <TableCell>{formatDate(user.created_at)}</TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm" onClick={() => handleEditClick(user)}>
                        Edit
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>

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

      <Modal
        isOpen={!!editingUser}
        onClose={() => setEditingUser(null)}
        title="Edit User"
        description="Change user role or active status."
      >
        {editingUser && (
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label>Name</Label>
              <Input value={editingUser.name} disabled />
            </div>
            <div className="space-y-2">
              <Label>Role</Label>
              <Select value={editRole} onChange={(e) => setEditRole(e.target.value as UserRole)}>
                <option value="customer">Customer</option>
                <option value="agent">Support Agent</option>
                <option value="admin">Administrator</option>
              </Select>
            </div>
            <div className="space-y-2 flex flex-col">
              <Label>Status</Label>
              <Select value={editActive ? "true" : "false"} onChange={(e) => setEditActive(e.target.value === "true")}>
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </Select>
            </div>
            <div className="flex justify-end gap-2 pt-4">
              <Button variant="outline" onClick={() => setEditingUser(null)}>Cancel</Button>
              <Button onClick={handleSave} disabled={mutation.isPending}>
                {mutation.isPending ? "Saving..." : "Save Changes"}
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
