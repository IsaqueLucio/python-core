
import { ShieldAlert } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { useNavigate } from 'react-router-dom';

export default function ForbiddenPage() {
  const navigate = useNavigate();
  
  return (
    <div className="flex h-[80vh] flex-col items-center justify-center text-center">
      <div className="rounded-full bg-destructive/10 p-6 mb-4">
        <ShieldAlert className="h-12 w-12 text-destructive" />
      </div>
      <h1 className="text-3xl font-bold tracking-tight mb-2">Access Denied</h1>
      <p className="text-muted-foreground mb-6 max-w-[400px]">
        You do not have permission to access this page. If you believe this is a mistake, please contact an administrator.
      </p>
      <Button onClick={() => navigate('/dashboard')}>
        Return to Dashboard
      </Button>
    </div>
  );
}
